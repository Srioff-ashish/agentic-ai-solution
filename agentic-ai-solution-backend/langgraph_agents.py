"""LangGraph-based agentic backend with FastAPI integration"""

import json
import logging
from typing import Any, Optional, TypedDict
from enum import Enum

from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, BaseMessage
from langchain_core.language_models import BaseChatModel
from langchain_anthropic import ChatAnthropic
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None
    
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None

from pydantic import BaseModel, Field

from config import Config
from mcp_client import MCPClient

logger = logging.getLogger(__name__)


# ============================================================================
# Mock LLM for Testing
# ============================================================================

class MockLLM(BaseChatModel):
    """Mock LLM that returns canned responses for testing"""
    
    model_name: str = Field(default="mock-model")
    
    def _generate(self, messages, **kwargs):
        """Generate mock responses based on input"""
        from langchain_core.outputs.llm_result import LLMResult
        from langchain_core.outputs.generation import Generation
        
        # Extract user message
        user_msg = next((m.content for m in messages if isinstance(m, HumanMessage)), "")
        
        # Return appropriate mock response
        if "architecture" in user_msg.lower() or "design" in user_msg.lower():
            response = """For REST API design, consider:
            
1. **Resource-Oriented Design**: Use nouns for endpoints (/users, /products)
2. **HTTP Methods**: GET (retrieve), POST (create), PUT/PATCH (update), DELETE (remove)
3. **Status Codes**: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error)
4. **Versioning**: Use URL paths (/v1/users) or headers
5. **Authentication**: Implement JWT or OAuth 2.0
6. **Rate Limiting**: Prevent abuse with throttling
7. **Documentation**: Use OpenAPI/Swagger
8. **Pagination**: Support limit/offset or cursor-based pagination

Example endpoint: GET /api/v1/users?page=1&limit=10"""
        elif "question" in user_msg.lower() or "what" in user_msg.lower():
            response = """This is a helpful mock response to your question. In a production environment, this would be handled by a real LLM provider like Anthropic, Google, or OpenAI."""
        elif "document" in user_msg.lower():
            response = """# API Documentation

## Overview
This API provides endpoints for managing resources.

## Endpoints
- GET /api/users - List all users
- POST /api/users - Create a new user
- GET /api/users/{id} - Get user details
- PUT /api/users/{id} - Update user
- DELETE /api/users/{id} - Delete user

## Authentication
Use Bearer token in Authorization header.

## Rate Limiting
10,000 requests per hour."""
        else:
            response = f"""Mock response to: "{user_msg}"
            
This is a demonstration response from the LangGraph agentic backend. The LangGraph architecture is successfully running with proper state management and agent routing."""
        
        return LLMResult(generations=[[Generation(text=response)]])
    
    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "mock"
    
    def _invoke(self, input, **kwargs):
        """Invoke the mock LLM"""
        messages = input if isinstance(input, list) else [input]
        result = self._generate(messages, **kwargs)
        return AIMessage(content=result.generations[0][0].text)
    
    def invoke(self, input, **kwargs):
        """Invoke the mock LLM"""
        return self._invoke(input, **kwargs)


# ============================================================================
# State Management
# ============================================================================

class AgentState(TypedDict):
    """State passed through the agentic workflow"""
    query: str
    service_type: str
    reasoning: str
    analysis: dict[str, Any]
    response: str
    messages: list
    mcp_client: Optional[MCPClient]


class ServiceType(str, Enum):
    """Available service types"""
    INFRASTRUCTURE = "infrastructure"
    INQUIRY = "inquiry"
    DOCUMENT = "document"


# ============================================================================
# LLM Configuration
# ============================================================================

def get_llm():
    """Get LLM based on config"""
    provider = Config.LLM_PROVIDER
    
    if provider == "anthropic":
        return ChatAnthropic(
            model=Config.ANTHROPIC_MODEL,
            api_key=Config.ANTHROPIC_API_KEY,
            temperature=0.7
        )
    elif provider == "google":
        if ChatGoogleGenerativeAI is None:
            raise ImportError("langchain-google-genai not installed. Run: pip install langchain-google-genai")
        return ChatGoogleGenerativeAI(
            model=Config.GOOGLE_MODEL,
            api_key=Config.GOOGLE_API_KEY,
            temperature=0.7
        )
    elif provider == "openai":
        if ChatOpenAI is None:
            raise ImportError("langchain-openai not installed. Run: pip install langchain-openai")
        return ChatOpenAI(
            model=Config.OPENAI_MODEL,
            api_key=Config.OPENAI_API_KEY,
            temperature=0.7
        )
    elif provider == "mock":
        logger.warning("Using mock LLM for demonstration. Configure a real provider for production.")
        return MockLLM()
    else:
        raise ValueError(f"Provider {provider} not supported")


# ============================================================================
# Service Detection Node
# ============================================================================

def detect_service(state: AgentState) -> AgentState:
    """Detect which service should handle this query"""
    logger.info("Node: Detecting service type")
    
    query_lower = state["query"].lower()
    
    # Infrastructure keywords
    infra_keywords = [
        "architecture", "microservices", "cloud", "deployment",
        "scalable", "containerization", "kubernetes", "docker",
        "infrastructure", "system design", "distributed"
    ]
    
    # Inquiry keywords
    inquiry_keywords = [
        "practice", "best", "security", "api", "iac",
        "pipeline", "automation", "advantage", "pattern",
        "approach", "methodology", "devops", "ci/cd"
    ]
    
    # Document keywords
    document_keywords = [
        "documentation", "document", "generate", "guide",
        "create", "template", "technical", "write", "outline", "design document"
    ]
    
    # Determine service
    if any(keyword in query_lower for keyword in infra_keywords):
        service = ServiceType.INFRASTRUCTURE.value
    elif any(keyword in query_lower for keyword in document_keywords):
        service = ServiceType.DOCUMENT.value
    elif any(keyword in query_lower for keyword in inquiry_keywords):
        service = ServiceType.INQUIRY.value
    else:
        # Default to inquiry for general questions
        service = ServiceType.INQUIRY.value
    
    logger.info(f"Service detected: {service}")
    
    state["service_type"] = service
    return state


# ============================================================================
# Infrastructure Agent
# ============================================================================

def infrastructure_agent(state: AgentState) -> AgentState:
    """Handle infrastructure and architecture questions"""
    logger.info("Node: Infrastructure Agent")
    
    llm = get_llm()
    
    system_prompt = """You are an expert in system architecture and infrastructure design.
    
    Answer questions about:
    - Microservices architecture
    - Cloud computing and deployment models
    - Scalable system design
    - Containerization and orchestration
    - Infrastructure patterns
    
    Provide detailed, technical, and practical answers."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    response = llm.invoke(messages)
    
    state["response"] = response.content
    state["messages"].append({"role": "assistant", "content": response.content})
    
    logger.info(f"Infrastructure Agent response: {response.content[:100]}...")
    
    return state


# ============================================================================
# Inquiry Agent
# ============================================================================

def inquiry_agent(state: AgentState) -> AgentState:
    """Handle general information and inquiry questions"""
    logger.info("Node: Inquiry Agent")
    
    llm = get_llm()
    
    system_prompt = """You are an expert advisor in software engineering and technology practices.
    
    Answer questions about:
    - Best practices and industry standards
    - DevOps and continuous integration
    - Security and compliance
    - Design patterns and methodologies
    - API design and architecture patterns
    - Cloud native technologies
    
    Provide practical, actionable advice based on industry best practices."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    response = llm.invoke(messages)
    
    state["response"] = response.content
    state["messages"].append({"role": "assistant", "content": response.content})
    
    logger.info(f"Inquiry Agent response: {response.content[:100]}...")
    
    return state


# ============================================================================
# Document Agent
# ============================================================================

def document_agent(state: AgentState) -> AgentState:
    """Handle documentation and technical writing tasks"""
    logger.info("Node: Document Agent")
    
    llm = get_llm()
    
    system_prompt = """You are an expert technical writer and documentation specialist.
    
    Help with:
    - API documentation
    - Technical design documents
    - Architecture decision records
    - Deployment guides
    - Troubleshooting guides
    - System documentation
    
    Create clear, well-structured, and comprehensive documentation."""
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["query"])
    ]
    
    response = llm.invoke(messages)
    
    state["response"] = response.content
    state["messages"].append({"role": "assistant", "content": response.content})
    
    logger.info(f"Document Agent response: {response.content[:100]}...")
    
    return state


# ============================================================================
# Routing Node
# ============================================================================

def route_to_agent(state: AgentState) -> str:
    """Route to the appropriate agent based on service type"""
    service = state.get("service_type", ServiceType.INQUIRY.value)
    logger.info(f"Routing to: {service}_agent")
    return f"{service}_agent"


# ============================================================================
# Build LangGraph Workflow
# ============================================================================

def build_agent_graph():
    """Build the LangGraph agent workflow"""
    
    # Create state graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("detect_service", detect_service)
    workflow.add_node("infrastructure_agent", infrastructure_agent)
    workflow.add_node("inquiry_agent", inquiry_agent)
    workflow.add_node("document_agent", document_agent)
    
    # Add edges
    workflow.add_edge(START, "detect_service")
    
    # Conditional routing based on service type
    workflow.add_conditional_edges(
        "detect_service",
        route_to_agent,
        {
            "infrastructure_agent": "infrastructure_agent",
            "inquiry_agent": "inquiry_agent",
            "document_agent": "document_agent"
        }
    )
    
    # All agents end
    workflow.add_edge("infrastructure_agent", END)
    workflow.add_edge("inquiry_agent", END)
    workflow.add_edge("document_agent", END)
    
    # Compile graph
    graph = workflow.compile()
    
    return graph


# ============================================================================
# Invoke Graph
# ============================================================================

async def invoke_agent_graph(query: str, mcp_client: Optional[MCPClient] = None) -> dict[str, Any]:
    """
    Invoke the agent graph with a query
    
    Args:
        query: User query
        mcp_client: Optional MCP client for service integration
    
    Returns:
        Response with service type, response, and metadata
    """
    
    logger.info(f"Invoking agent graph with query: {query}")
    
    # Create initial state
    initial_state: AgentState = {
        "query": query,
        "service_type": "",
        "reasoning": "",
        "analysis": {},
        "response": "",
        "messages": [{"role": "user", "content": query}],
        "mcp_client": mcp_client
    }
    
    # Build and invoke graph
    graph = build_agent_graph()
    
    # Invoke synchronously (LangGraph handles async internally)
    final_state = graph.invoke(initial_state)
    
    return {
        "response": final_state.get("response", ""),
        "service_type": final_state.get("service_type", ""),
        "query": final_state.get("query", ""),
        "llm_provider": Config.LLM_PROVIDER
    }
