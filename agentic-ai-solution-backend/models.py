"""Pydantic models for API requests and responses"""

from pydantic import BaseModel, Field
from typing import Any, Optional


# Request Models
class InfrastructureRequest(BaseModel):
    """Request for infrastructure service operations"""
    operation: str = Field(..., description="Operation type: list_indices, create_index, search, etc.")
    params: dict[str, Any] = Field(default_factory=dict, description="Operation parameters")
    user_id: Optional[str] = None


class InquiryRequest(BaseModel):
    """Request for inquiry service operations"""
    operation: str = Field(..., description="Operation type: create, list, search, etc.")
    params: dict[str, Any] = Field(default_factory=dict, description="Operation parameters")
    user_id: Optional[str] = None


class DocumentRequest(BaseModel):
    """Request for document service operations"""
    operation: str = Field(..., description="Operation type: upload, list, search, etc.")
    params: dict[str, Any] = Field(default_factory=dict, description="Operation parameters")
    user_id: Optional[str] = None


class OrchestratorRequest(BaseModel):
    """Main request to orchestrator"""
    query: str = Field(..., description="User query or request")
    service: Optional[str] = None  # Optional: can be inferred by orchestrator
    params: dict[str, Any] = Field(default_factory=dict, description="Additional parameters")
    user_id: Optional[str] = None
    context: dict[str, Any] = Field(default_factory=dict, description="Additional context")


# Response Models
class ToolResult(BaseModel):
    """Result from a tool/MCP call"""
    tool_name: str
    status: str  # success, error, partial
    data: Any = None
    error: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Response from an agent"""
    agent_type: str  # infrastructure, inquiry, document
    action: str
    result: Any = None
    reasoning: str
    tool_calls: list[ToolResult] = Field(default_factory=list)
    success: bool


class OrchestratorResponse(BaseModel):
    """Final response from orchestrator"""
    query: str
    service_type: str  # Which service handled the request
    agent_response: AgentResponse
    final_result: Any = None
    status: str  # success, partial, error
    message: str


# Chat/Conversation Models for UI
class ChatMessage(BaseModel):
    """Message in conversation"""
    role: str  # user, assistant
    content: str
    timestamp: Optional[str] = None


class ConversationRequest(BaseModel):
    """Request with conversation context"""
    message: str
    conversation_history: list[ChatMessage] = Field(default_factory=list)
    user_id: Optional[str] = None
    session_id: Optional[str] = None


class ConversationResponse(BaseModel):
    """Response with conversation context"""
    message: str
    service_type: str
    action: str
    result: Any = None
    thinking: Optional[str] = None
    success: bool


# Health Check
class HealthResponse(BaseModel):
    """Health check response"""
    status: str  # healthy, degraded, unhealthy
    services: dict[str, str]  # infrastructure, inquiry, document health status
    timestamp: str
