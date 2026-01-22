"""Orchestrator for routing requests to appropriate agents"""

import json
import logging
from typing import Any, Optional

from mcp_client import MCPClient
from agents import InfrastructureAgent, get_llm_client, AgentState
from config import Config
from models import OrchestratorRequest, OrchestratorResponse, AgentResponse, ToolResult

logger = logging.getLogger(__name__)


class ServiceRouter:
    """Routes requests to appropriate service"""
    
    def __init__(self, mcp_client: MCPClient):
        self.mcp_client = mcp_client
        self.llm = get_llm_client()
        
        # Initialize agents
        self.infrastructure_agent = InfrastructureAgent(mcp_client)
    
    async def route_request(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Route request to appropriate service"""
        
        # Determine service if not provided
        service = request.service
        if not service:
            service = await self._detect_service(request.query)
        
        logger.info(f"Routing request to service: {service}")
        
        # Route to appropriate agent
        if service == "infrastructure":
            return await self._handle_infrastructure(request)
        elif service == "inquiry":
            return await self._handle_inquiry(request)
        elif service == "document":
            return await self._handle_document(request)
        else:
            return OrchestratorResponse(
                query=request.query,
                service_type="unknown",
                agent_response=AgentResponse(
                    agent_type="unknown",
                    action="error",
                    reasoning="Could not determine service",
                    success=False
                ),
                status="error",
                message=f"Unknown service: {service}"
            )
    
    async def _detect_service(self, query: str) -> str:
        """Detect which service the query is for"""
        system_prompt = """You are a service router. Analyze the user query and determine which service it belongs to:
        
- "infrastructure" for: search, indexing, indices, documents, products, users, orders
- "inquiry" for: support, ticket, issue, problem, complaint, request, help
- "document" for: document, file, upload, version, download, attachment

Respond with only the service name: infrastructure, inquiry, or document"""
        
        try:
            # Use the LLM client's analyze_query method
            action, params, reasoning = await self.llm.analyze_query(
                query, 
                system_prompt
            )
            
            # Extract service name from action if present
            service = action.strip().lower() if action else "infrastructure"
            
            # Validate response
            if service in ["infrastructure", "inquiry", "document"]:
                return service
            else:
                # Default to infrastructure if unsure
                return "infrastructure"
        
        except Exception as e:
            logger.error(f"Error detecting service: {e}")
            return "infrastructure"
    
    async def _handle_infrastructure(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Handle infrastructure service request"""
        try:
            agent_state = await self.infrastructure_agent.run(
                query=request.query,
                user_id=request.user_id,
                context=request.context
            )
            
            # Convert agent state to response
            agent_response = AgentResponse(
                agent_type="infrastructure",
                action=agent_state.action or "unknown",
                result=agent_state.result,
                reasoning=agent_state.reasoning,
                tool_calls=[
                    ToolResult(
                        tool_name=call.get("tool", "unknown"),
                        status="executed",
                        data=None,
                        metadata={"params": call.get("params", {})}
                    )
                    for call in agent_state.tool_calls
                ],
                success=agent_state.success
            )
            
            return OrchestratorResponse(
                query=request.query,
                service_type="infrastructure",
                agent_response=agent_response,
                final_result=agent_state.result,
                status="success" if agent_state.success else "error",
                message=agent_state.error or "Infrastructure request completed"
            )
        
        except Exception as e:
            logger.error(f"Error handling infrastructure request: {e}")
            return OrchestratorResponse(
                query=request.query,
                service_type="infrastructure",
                agent_response=AgentResponse(
                    agent_type="infrastructure",
                    action="error",
                    reasoning=str(e),
                    success=False
                ),
                status="error",
                message=str(e)
            )
    
    async def _handle_inquiry(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Handle inquiry service request (placeholder for now)"""
        # Similar to infrastructure, but routes to inquiry_agent
        # For now, returning a structured response
        
        return OrchestratorResponse(
            query=request.query,
            service_type="inquiry",
            agent_response=AgentResponse(
                agent_type="inquiry",
                action="process",
                reasoning="Inquiry agent would process this",
                success=False  # Not implemented yet
            ),
            status="pending",
            message="Inquiry agent not yet implemented"
        )
    
    async def _handle_document(self, request: OrchestratorRequest) -> OrchestratorResponse:
        """Handle document service request (placeholder for now)"""
        # Similar to infrastructure, but routes to document_agent
        # For now, returning a structured response
        
        return OrchestratorResponse(
            query=request.query,
            service_type="document",
            agent_response=AgentResponse(
                agent_type="document",
                action="process",
                reasoning="Document agent would process this",
                success=False  # Not implemented yet
            ),
            status="pending",
            message="Document agent not yet implemented"
        )
