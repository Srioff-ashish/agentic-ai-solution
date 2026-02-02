"""Orchestrator for routing requests through LangGraph agent workflow

This module provides a simple interface to the LangGraph agentic backend.
The orchestrator routes queries to appropriate agents (Inquiry, General)
and integrates with the MCP server for payment inquiry tools.
"""

import logging
from typing import Any, Optional

from mcp_client import MCPPaymentClient
from langgraph_agents import invoke_agent_graph, set_mcp_client
from config import Config
from models import OrchestratorRequest, OrchestratorResponse, AgentResponse, ToolResult

logger = logging.getLogger(__name__)


class AgenticOrchestrator:
    """
    Orchestrator that uses LangGraph workflow with MCP tools.
    
    Routes queries to:
    - Inquiry Agent: For payment/transaction lookups (uses MCP server)
    - General Agent: For other questions
    """
    
    def __init__(self, mcp_client: Optional[MCPPaymentClient] = None):
        """
        Initialize orchestrator with MCP client.
        
        Args:
            mcp_client: MCPPaymentClient for MCP server communication
        """
        self.mcp_client = mcp_client or MCPPaymentClient()
        logger.info(f"Orchestrator initialized with LLM provider: {Config.LLM_PROVIDER}")
    
    async def process_query(self, query: str, user_id: Optional[str] = None) -> dict[str, Any]:
        """
        Process a query through the LangGraph agent workflow.
        
        Args:
            query: User query string
            user_id: Optional user identifier
        
        Returns:
            Response dict with response text, service type, and metadata
        """
        logger.info(f"Processing query: {query[:100]}...")
        
        # Invoke the LangGraph workflow
        result = await invoke_agent_graph(
            query=query,
            mcp_client=self.mcp_client
        )
        
        logger.info(f"Query processed by {result.get('service_type')} agent")
        return result
    
    async def route_request(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """
        Route a request through the agent workflow.
        
        Args:
            request: OrchestratorRequest with query and context
        
        Returns:
            OrchestratorResponse with agent response and metadata
        """
        try:
            result = await self.process_query(
                query=request.query,
                user_id=request.user_id
            )
            
            # Convert tool_results to ToolResult objects
            tool_calls = []
            for tr in result.get("tool_results", []):
                tool_calls.append(ToolResult(
                    tool_name=tr.get("tool", "unknown"),
                    status="executed",
                    data=tr.get("result"),
                    metadata={"args": tr.get("args", {})}
                ))
            
            agent_response = AgentResponse(
                agent_type=result.get("service_type", "unknown"),
                action="process",
                result=result.get("response", ""),
                reasoning=f"Processed by {result.get('service_type')} agent",
                tool_calls=tool_calls,
                success=result.get("success", False)
            )
            
            return OrchestratorResponse(
                query=request.query,
                service_type=result.get("service_type", "unknown"),
                agent_response=agent_response,
                final_result=result.get("response", ""),
                status="success" if result.get("success") else "error",
                message=result.get("error") or "Query processed successfully"
            )
        
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return OrchestratorResponse(
                query=request.query,
                service_type="error",
                agent_response=AgentResponse(
                    agent_type="error",
                    action="error",
                    reasoning=str(e),
                    success=False
                ),
                status="error",
                message=str(e)
            )


# Backwards compatibility alias
ServiceRouter = AgenticOrchestrator
