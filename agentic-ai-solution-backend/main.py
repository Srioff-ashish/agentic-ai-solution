"""FastAPI main application - Agentic Backend with LangGraph and Vertex AI"""

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import Config
from models import (
    OrchestratorRequest, OrchestratorResponse, ConversationRequest, 
    ConversationResponse, HealthResponse
)
from mcp_client import MCPPaymentClient
from orchestrator import AgenticOrchestrator
from langgraph_agents import invoke_agent_graph

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Global instances
mcp_client: MCPPaymentClient = None
orchestrator: AgenticOrchestrator = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global mcp_client, orchestrator
    
    # Startup
    logger.info("Starting up Agentic AI Backend...")
    logger.info(f"LLM Provider: {Config.LLM_PROVIDER}")
    logger.info(f"Mock API URL: {Config.MOCK_API_URL}")
    logger.info(f"MCP Server URL: {Config.MCP_SERVER_URL}")
    
    # Initialize MCP client (lazy connection - will connect on first request)
    mcp_client = MCPPaymentClient()
    
    orchestrator = AgenticOrchestrator(mcp_client)
    logger.info("Backend services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    if mcp_client:
        await mcp_client.close()
    logger.info("Backend services shut down")


# Create FastAPI app
app = FastAPI(
    title=Config.API_TITLE,
    description=Config.API_DESCRIPTION,
    version=Config.API_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health Check Endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    try:
        logger.info(f"Health check called. mcp_client: {mcp_client}, type: {type(mcp_client)}")
        
        # Check if MCP client can reach MCP server -> Mock API
        mcp_health = {}
        mcp_healthy = False
        
        if mcp_client:
            try:
                logger.info(f"Calling MCP health check at {mcp_client.base_url}")
                mcp_health = await mcp_client.health_check()
                mcp_healthy = "error" not in mcp_health and mcp_health.get("status") == "healthy"
                logger.info(f"MCP health check result: {mcp_health}, healthy: {mcp_healthy}")
            except Exception as mcp_err:
                logger.error(f"MCP health check failed: {mcp_err}", exc_info=True)
        else:
            logger.warning("MCP client not initialized")
        
        services = {
            "mcp_server": "healthy" if mcp_healthy else "unhealthy",
            "backend": "healthy",
            "orchestrator": "healthy",
            "llm_provider": Config.LLM_PROVIDER,
        }
        
        overall_status = "healthy" if mcp_healthy else "degraded"
        
        return HealthResponse(
            status=overall_status,
            services=services,
            timestamp=""
        )
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return HealthResponse(
            status="unhealthy",
            services={
                "mcp_server": "unhealthy",
                "backend": "healthy",
                "orchestrator": "healthy",
                "llm_provider": Config.LLM_PROVIDER
            },
            timestamp=""
        )


# Main Orchestrator Endpoints
@app.post("/orchestrate", response_model=OrchestratorResponse, tags=["Orchestration"])
async def orchestrate(request: OrchestratorRequest):
    """Main orchestration endpoint - uses LangGraph agent workflow with MCP tools"""
    try:
        logger.info(f"Orchestrating request: {request.query}")
        
        # Invoke LangGraph agent graph with MCP client
        result = await invoke_agent_graph(request.query, mcp_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type=result.get("service_type", ""),
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", ""),
            tool_results=result.get("tool_results", [])
        )
    
    except Exception as e:
        logger.error(f"Orchestration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ConversationResponse, tags=["Chat"])
async def chat(request: ConversationRequest):
    """Chat endpoint for conversation-based interaction"""
    try:
        # Invoke LangGraph agent graph with MCP client
        result = await invoke_agent_graph(request.message, mcp_client)
        
        # Convert to conversation response
        return ConversationResponse(
            message=result.get("response", ""),
            service_type=result.get("service_type", ""),
            action="respond",
            result=result.get("tool_results", []),
            thinking=f"Processed by {result.get('service_type')} agent",
            success=result.get("success", False)
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Payment Inquiry Endpoint (primary service)
@app.post("/inquiry/query", response_model=OrchestratorResponse, tags=["Inquiry"])
async def inquiry_query(request: OrchestratorRequest):
    """Query payment inquiry service - uses MCP tools for payment/transaction lookup"""
    try:
        logger.info(f"Inquiry query: {request.query}")
        result = await invoke_agent_graph(request.query, payment_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type="inquiry",
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", ""),
            tool_results=result.get("tool_results", [])
        )
    except Exception as e:
        logger.error(f"Inquiry query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API Documentation
@app.get("/", tags=["Info"])
async def root():
    """API Root - Returns documentation"""
    return {
        "name": "Agentic AI Solution Backend",
        "version": "0.2.0",
        "description": "LangGraph-based agentic backend with Vertex AI and MCP tools",
        "llm_provider": Config.LLM_PROVIDER,
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "orchestrate": "/orchestrate (POST) - Main agent workflow",
            "chat": "/chat (POST) - Chat interface",
            "inquiry": "/inquiry/query (POST) - Payment inquiry"
        },
        "agents": {
            "inquiry": "Payment/Transaction lookup using MCP tools",
            "general": "General questions"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9000,
        reload=Config.DEBUG
    )
