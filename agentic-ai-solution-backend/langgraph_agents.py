"""LangGraph-based agentic backend with Vertex AI and MCP integration

This module implements a LangGraph workflow with:
- Orchestrator node for routing queries
- Inquiry Agent with MCP tools for payment/transaction lookup
- Google Vertex AI as the primary LLM
"""

import json
import logging
import asyncio
from typing import Any, Optional, TypedDict, Annotated, Literal
from enum import Enum

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage, ToolMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Optional imports for different LLM providers
try:
    from langchain_google_vertexai import ChatVertexAI
except ImportError:
    ChatVertexAI = None

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None

try:
    from langchain_anthropic import ChatAnthropic
except ImportError:
    ChatAnthropic = None
    
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

from config import Config
from mcp_client import MCPPaymentClient

logger = logging.getLogger(__name__)

# Global MCP client for tools
_mcp_client: Optional[MCPPaymentClient] = None


def set_mcp_client(client: MCPPaymentClient):
    """Set the global MCP client for payment inquiry tools"""
    global _mcp_client
    _mcp_client = client


# ============================================================================
# State Management
# ============================================================================

class AgentState(TypedDict):
    """State passed through the agentic workflow"""
    query: str
    messages: list[BaseMessage]
    service_type: str
    tool_calls: list[dict]
    tool_results: list[dict]
    response: str
    error: Optional[str]


class ServiceType(str, Enum):
    """Available service types"""
    INQUIRY = "inquiry"
    GENERAL = "general"


# ============================================================================
# LLM Configuration - Vertex AI Primary
# ============================================================================

def get_llm() -> BaseChatModel:
    """Get LLM based on config - Vertex AI is primary"""
    provider = Config.LLM_PROVIDER
    
    if provider == "vertexai":
        if ChatVertexAI is None:
            raise ImportError("langchain-google-vertexai not installed. Run: pip install langchain-google-vertexai")
        
        if not Config.GOOGLE_CLOUD_PROJECT:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")
        
        logger.info(f"Using Vertex AI with project: {Config.GOOGLE_CLOUD_PROJECT}")
        return ChatVertexAI(
            model=Config.VERTEX_AI_MODEL,
            project=Config.GOOGLE_CLOUD_PROJECT,
            location=Config.GOOGLE_CLOUD_LOCATION,
            temperature=0.3,
        )
    
    elif provider == "google":
        if ChatGoogleGenerativeAI is None:
            raise ImportError("langchain-google-genai not installed")
        
        if not Config.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        logger.info("Using Google Gemini API")
        return ChatGoogleGenerativeAI(
            model=Config.GOOGLE_MODEL,
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0.3,
        )
    
    elif provider == "anthropic":
        if ChatAnthropic is None:
            raise ImportError("langchain-anthropic not installed")
        
        if not Config.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        
        return ChatAnthropic(
            model=Config.ANTHROPIC_MODEL,
            api_key=Config.ANTHROPIC_API_KEY,
            temperature=0.3,
        )
    
    elif provider == "openai":
        if ChatOpenAI is None:
            raise ImportError("langchain-openai not installed")
        
        if not Config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=0.3,
        )
    
    elif provider == "mock":
        logger.warning("Using mock LLM for testing")
        return MockLLM()
    
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


# ============================================================================
# Mock LLM for Testing
# ============================================================================

class MockLLM(BaseChatModel):
    """Mock LLM for testing without API keys - supports tool calling"""
    
    model_name: str = Field(default="mock-model")
    tools: list = Field(default_factory=list)
    
    def _generate(self, messages, **kwargs):
        from langchain_core.outputs import LLMResult, Generation
        
        user_msg = next((m.content for m in messages if isinstance(m, HumanMessage)), "")
        
        # Check if this is a tool result message (second call)
        has_tool_results = any(isinstance(m, ToolMessage) for m in messages)
        
        if has_tool_results:
            # Second call - format the tool results nicely
            tool_data = next((m.content for m in messages if isinstance(m, ToolMessage)), "")
            try:
                data = json.loads(tool_data)
                if isinstance(data, dict) and "payments" in data:
                    count = len(data.get("payments", []))
                    response = f"Found {count} payments in the system. Here are the details:\n\n{tool_data}"
                elif isinstance(data, dict) and "transactions" in data:
                    count = len(data.get("transactions", []))
                    response = f"Found {count} transactions. Here are the details:\n\n{tool_data}"
                else:
                    response = f"Here are the results:\n\n{tool_data}"
            except:
                response = f"Here are the results:\n\n{tool_data}"
        elif any(word in user_msg.lower() for word in ["payment", "transaction", "iban", "status", "list", "show", "get"]):
            response = "I'll help you look up that payment information."
        else:
            response = f"Mock response to: {user_msg[:100]}..."
        
        return LLMResult(generations=[[Generation(text=response)]])
    
    @property
    def _llm_type(self) -> str:
        return "mock"
    
    def bind_tools(self, tools, **kwargs):
        """Store tools for mock tool calling"""
        self.tools = tools
        return self
    
    def invoke(self, input, **kwargs):
        from langchain_core.messages import AIMessage, ToolCall
        
        messages = input if isinstance(input, list) else [input]
        user_msg = next((m.content for m in messages if isinstance(m, HumanMessage)), "")
        
        # Check if we have tool results already (second invocation)
        has_tool_results = any(isinstance(m, ToolMessage) for m in messages)
        
        if has_tool_results:
            # Generate final response with tool results
            result = self._generate(messages, **kwargs)
            return AIMessage(content=result.generations[0][0].text)
        
        # First invocation - decide if we need tools
        if self.tools and any(word in user_msg.lower() for word in ["payment", "transaction", "list", "show", "get", "search", "find", "stats"]):
            # Determine which tool to call based on query
            tool_name = "list_payments"
            tool_args = {"limit": 10}
            
            if "stats" in user_msg.lower() or "statistic" in user_msg.lower():
                tool_name = "get_payment_stats"
                tool_args = {}
            elif "transaction" in user_msg.lower():
                tool_name = "list_transactions"
                tool_args = {"limit": 10}
            elif "search" in user_msg.lower() or "find" in user_msg.lower():
                if "transaction" in user_msg.lower():
                    tool_name = "search_transactions"
                    tool_args = {}
                else:
                    tool_name = "search_payments"
                    tool_args = {}
            
            # Return AIMessage with tool_calls
            return AIMessage(
                content="",
                tool_calls=[{
                    "id": "mock_tool_call_1",
                    "name": tool_name,
                    "args": tool_args
                }]
            )
        
        # No tools needed
        result = self._generate(messages, **kwargs)
        return AIMessage(content=result.generations[0][0].text)


# ============================================================================
# MCP Tools for Inquiry Agent
# ============================================================================

@tool
async def list_payments(limit: int = 10) -> str:
    """List all payments in the system.
    
    Args:
        limit: Maximum number of payments to return (default 10)
    
    Returns:
        JSON string with payment list
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.list_payments(limit=limit)
    return json.dumps(result, indent=2, default=str)


@tool
async def get_payment(pmt_id: str) -> str:
    """Get details for a specific payment by its ID.
    
    Args:
        pmt_id: The payment ID (UUID format like d145a790-8ef1-4776-8e98-92dad80f0a9d)
    
    Returns:
        JSON string with payment details including status, IBAN, amount, etc.
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.get_payment(pmt_id)
    return json.dumps(result, indent=2, default=str)


@tool
async def search_payments(
    status: Optional[str] = None,
    debtor_iban: Optional[str] = None,
    channel: Optional[str] = None,
    product: Optional[str] = None
) -> str:
    """Search for payments with filters.
    
    Args:
        status: Filter by payment status (RCVD=Received, ACTC=Accepted, ACSC=Completed, IAUT=In Authorization, RJCT=Rejected)
        debtor_iban: Filter by debtor/originator IBAN (e.g., NL19INGB0588118729)
        channel: Filter by channel (MOBP, MINGZ, MMINGP)
        product: Filter by product (INST, SEPA-CT)
    
    Returns:
        JSON string with matching payments
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.search_payments(
        status=status,
        debtor_iban=debtor_iban,
        channel=channel,
        product=product
    )
    return json.dumps(result, indent=2, default=str)


@tool
async def get_payment_with_transactions(pmt_id: str) -> str:
    """Get a payment along with all its transactions.
    
    Args:
        pmt_id: The payment ID
    
    Returns:
        JSON string with payment and embedded transactions
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.get_payment_with_transactions(pmt_id)
    return json.dumps(result, indent=2, default=str)


@tool
async def list_transactions(limit: int = 10) -> str:
    """List all transactions in the system.
    
    Args:
        limit: Maximum number of transactions to return
    
    Returns:
        JSON string with transaction list
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.list_transactions(limit=limit)
    return json.dumps(result, indent=2, default=str)


@tool
async def get_transaction(tx_id: str) -> str:
    """Get details for a specific transaction.
    
    Args:
        tx_id: The transaction ID
    
    Returns:
        JSON string with transaction details
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.get_transaction(tx_id)
    return json.dumps(result, indent=2, default=str)


@tool
async def search_transactions(
    status: Optional[str] = None,
    iban: Optional[str] = None,
    pmt_id: Optional[str] = None,
    amount_min: Optional[float] = None,
    amount_max: Optional[float] = None
) -> str:
    """Search for transactions with filters.
    
    Args:
        status: Filter by status (ACTC, ACSC, RJCT)
        iban: Filter by IBAN (originator or counterparty)
        pmt_id: Filter by parent payment ID
        amount_min: Minimum transaction amount
        amount_max: Maximum transaction amount
    
    Returns:
        JSON string with matching transactions
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    if pmt_id:
        result = await _mcp_client.get_transactions_by_payment(pmt_id)
    else:
        result = await _mcp_client.search_transactions(
            status=status,
            iban=iban,
            amount_min=amount_min,
            amount_max=amount_max
        )
    return json.dumps(result, indent=2, default=str)


@tool
async def get_payment_stats() -> str:
    """Get statistics about payments and transactions.
    
    Returns:
        JSON string with counts by status, channels, products, etc.
    """
    if not _mcp_client:
        return json.dumps({"error": "Payment client not initialized"})
    
    result = await _mcp_client.get_stats()
    return json.dumps(result, indent=2, default=str)


# All inquiry tools
INQUIRY_TOOLS = [
    list_payments,
    get_payment,
    search_payments,
    get_payment_with_transactions,
    list_transactions,
    get_transaction,
    search_transactions,
    get_payment_stats,
]


# ============================================================================
# Service Detection Node (Orchestrator)
# ============================================================================

def detect_service(state: AgentState) -> AgentState:
    """Determine query type and route to appropriate agent"""
    logger.info("Node: Orchestrator - Detecting service type")
    
    query_lower = state["query"].lower()
    
    # Payment/Transaction inquiry keywords
    inquiry_keywords = [
        "payment", "transaction", "pmt", "tx", "iban", "status",
        "rejected", "completed", "pending", "sepa", "inst",
        "transfer", "amount", "find", "search", "list", "get",
        "show", "lookup", "inquiry", "check", "stats", "statistics"
    ]
    
    if any(keyword in query_lower for keyword in inquiry_keywords):
        state["service_type"] = ServiceType.INQUIRY.value
        logger.info("Routed to: Inquiry Agent")
    else:
        state["service_type"] = ServiceType.GENERAL.value
        logger.info("Routed to: General Agent")
    
    return state


# ============================================================================
# Inquiry Agent (with MCP Tools)
# ============================================================================

async def inquiry_agent(state: AgentState) -> AgentState:
    """Handle payment/transaction inquiries using MCP tools"""
    logger.info("Node: Inquiry Agent")
    
    llm = get_llm()
    llm_with_tools = llm.bind_tools(INQUIRY_TOOLS)
    
    system_prompt = """You are a Payment Inquiry Assistant for the OMaaP system.

You help users find information about payments and transactions. You have access to these tools:
- list_payments: List all payments
- get_payment: Get details for a specific payment ID
- search_payments: Search payments by status, IBAN, channel, product
- get_payment_with_transactions: Get payment with all its transactions
- list_transactions: List all transactions
- get_transaction: Get transaction details
- search_transactions: Search transactions by status, IBAN, amount
- get_payment_stats: Get statistics

Payment statuses: RCVD (Received), ACTC (Accepted), ACSC (Completed), IAUT (In Authorization), RJCT (Rejected)
Transaction statuses: ACTC, ACSC, RJCT

When presenting results:
- Format data clearly with key fields highlighted
- Explain status codes in plain language
- If a payment is rejected, explain the reason code

Always use the tools to get real data before responding."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    # First LLM call - may request tools
    response = await asyncio.to_thread(llm_with_tools.invoke, messages)
    
    # Check if tools were called
    if hasattr(response, 'tool_calls') and response.tool_calls:
        logger.info(f"Tool calls requested: {[tc['name'] for tc in response.tool_calls]}")
        
        messages.append(response)
        tool_results = []
        
        # Execute each tool
        for tool_call in response.tool_calls:
            tool_name = tool_call['name']
            tool_args = tool_call['args']
            
            logger.info(f"Executing tool: {tool_name} with args: {tool_args}")
            
            # Find and execute the tool
            tool_fn = next((t for t in INQUIRY_TOOLS if t.name == tool_name), None)
            if tool_fn:
                try:
                    result = await tool_fn.ainvoke(tool_args)
                    tool_results.append({
                        "tool": tool_name,
                        "args": tool_args,
                        "result": result
                    })
                    messages.append(ToolMessage(
                        content=result,
                        tool_call_id=tool_call['id']
                    ))
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    messages.append(ToolMessage(
                        content=json.dumps({"error": str(e)}),
                        tool_call_id=tool_call['id']
                    ))
        
        state["tool_results"] = tool_results
        
        # Second LLM call with tool results
        final_response = await asyncio.to_thread(llm_with_tools.invoke, messages)
        state["response"] = final_response.content
    else:
        state["response"] = response.content
    
    state["messages"] = messages
    logger.info("Inquiry Agent response generated")
    
    return state


# ============================================================================
# General Agent
# ============================================================================

async def general_agent(state: AgentState) -> AgentState:
    """Handle general questions"""
    logger.info("Node: General Agent")
    
    llm = get_llm()
    
    system_prompt = """You are a helpful assistant for the OMaaP system.
    
For questions about payments, transactions, or financial data, suggest the user 
ask more specifically so you can use the inquiry tools.

For other questions, provide helpful general responses."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    response = await asyncio.to_thread(llm.invoke, messages)
    state["response"] = response.content
    state["messages"] = messages
    
    return state


# ============================================================================
# Routing Function
# ============================================================================

def route_to_agent(state: AgentState) -> Literal["inquiry_agent", "general_agent"]:
    """Route to the appropriate agent based on service type"""
    service = state.get("service_type", ServiceType.GENERAL.value)
    if service == ServiceType.INQUIRY.value:
        return "inquiry_agent"
    return "general_agent"


# ============================================================================
# Build LangGraph Workflow
# ============================================================================

def build_agent_graph():
    """Build the LangGraph agent workflow"""
    
    # Create state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("orchestrator", detect_service)
    workflow.add_node("inquiry_agent", inquiry_agent)
    workflow.add_node("general_agent", general_agent)
    
    # Add edges
    workflow.add_edge(START, "orchestrator")
    
    # Conditional routing based on service type
    workflow.add_conditional_edges(
        "orchestrator",
        route_to_agent,
        {
            "inquiry_agent": "inquiry_agent",
            "general_agent": "general_agent"
        }
    )
    
    # All agents end
    workflow.add_edge("inquiry_agent", END)
    workflow.add_edge("general_agent", END)
    
    # Compile graph
    return workflow.compile()


# ============================================================================
# Public Interface
# ============================================================================

async def invoke_agent_graph(
    query: str,
    mcp_client: Optional[MCPPaymentClient] = None
) -> dict[str, Any]:
    """
    Invoke the agent graph with a query.
    
    Args:
        query: User query
        mcp_client: MCP client for payment inquiry tools
    
    Returns:
        Response dict with response text, service type, and metadata
    """
    logger.info(f"Invoking agent graph with query: {query[:100]}...")
    
    # Set up the payment client for tools
    if mcp_client:
        set_mcp_client(mcp_client)
    
    # Create initial state
    initial_state: AgentState = {
        "query": query,
        "messages": [],
        "service_type": "",
        "tool_calls": [],
        "tool_results": [],
        "response": "",
        "error": None
    }
    
    try:
        # Build and invoke graph
        graph = build_agent_graph()
        
        # Use ainvoke for async
        final_state = await graph.ainvoke(initial_state)
        
        return {
            "response": final_state.get("response", ""),
            "service_type": final_state.get("service_type", ""),
            "tool_results": final_state.get("tool_results", []),
            "query": query,
            "llm_provider": Config.LLM_PROVIDER,
            "success": True
        }
    
    except Exception as e:
        logger.error(f"Error in agent graph: {e}")
        return {
            "response": f"I encountered an error processing your request: {str(e)}",
            "service_type": "error",
            "query": query,
            "llm_provider": Config.LLM_PROVIDER,
            "success": False,
            "error": str(e)
        }
