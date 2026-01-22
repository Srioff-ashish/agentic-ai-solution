"""FastAPI main application"""

import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import Config
from models import (
    OrchestratorRequest, OrchestratorResponse, ConversationRequest, 
    ConversationResponse, HealthResponse
)
from mcp_client import MCPClient
from orchestrator import ServiceRouter
from langgraph_agents import invoke_agent_graph

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Global instances
mcp_client: MCPClient = None
service_router: ServiceRouter = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown"""
    global mcp_client, service_router
    
    # Startup
    logger.info("Starting up...")
    mcp_client = MCPClient(base_url=Config.INFRASTRUCTURE_SERVICE_URL)
    service_router = ServiceRouter(mcp_client)
    logger.info("Backend services initialized")
    
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
        # Check if MCP client is available
        infrastructure_healthy = await mcp_client.health_check() if mcp_client else False
        
        services = {
            "mcp": "healthy" if infrastructure_healthy else "unhealthy",
            "backend": "healthy",
            "orchestrator": "healthy"
        }
        
        overall_status = "healthy" if infrastructure_healthy else "degraded"
        
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
                "mcp": "unhealthy",
                "backend": "healthy",
                "orchestrator": "healthy"
            },
            timestamp=""
        )


# Main Orchestrator Endpoints
@app.post("/orchestrate", response_model=OrchestratorResponse, tags=["Orchestration"])
async def orchestrate(request: OrchestratorRequest):
    """Main orchestration endpoint - uses LangGraph agent workflow"""
    try:
        logger.info(f"Orchestrating request: {request.query}")
        
        # Invoke LangGraph agent graph
        result = await invoke_agent_graph(request.query, mcp_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type=result.get("service_type", ""),
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", "")
        )
    
    except Exception as e:
        logger.error(f"Orchestration error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ConversationResponse, tags=["Chat"])
async def chat(request: ConversationRequest):
    """Chat endpoint for conversation-based interaction"""
    try:
        # Invoke LangGraph agent graph
        result = await invoke_agent_graph(request.message, mcp_client)
        
        # Convert to conversation response
        return ConversationResponse(
            message=result.get("response", ""),
            service_type=result.get("service_type", ""),
            action="respond",
            result=result.get("analysis", {}),
            thinking=result.get("reasoning", ""),
            success=True
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Service-specific Endpoints
@app.post("/infrastructure/query", response_model=OrchestratorResponse, tags=["Infrastructure"])
async def infrastructure_query(request: OrchestratorRequest):
    """Query infrastructure service"""
    try:
        logger.info(f"Infrastructure query: {request.query}")
        result = await invoke_agent_graph(request.query, mcp_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type="infrastructure",
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", "")
        )
    except Exception as e:
        logger.error(f"Infrastructure query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/inquiry/query", response_model=OrchestratorResponse, tags=["Inquiry"])
async def inquiry_query(request: OrchestratorRequest):
    """Query inquiry service"""
    try:
        logger.info(f"Inquiry query: {request.query}")
        result = await invoke_agent_graph(request.query, mcp_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type="inquiry",
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", "")
        )
    except Exception as e:
        logger.error(f"Inquiry query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/document/query", response_model=OrchestratorResponse, tags=["Document"])
async def document_query(request: OrchestratorRequest):
    """Query document service"""
    try:
        logger.info(f"Document query: {request.query}")
        result = await invoke_agent_graph(request.query, mcp_client)
        
        return OrchestratorResponse(
            response=result.get("response", ""),
            service_type="document",
            llm_provider=result.get("llm_provider", ""),
            query=result.get("query", "")
        )
    except Exception as e:
        logger.error(f"Document query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API Documentation
@app.get("/", tags=["Info"])
async def root():
    """API Root - Returns documentation"""
    return {
        "name": "Agentic AI Solution Backend",
        "version": "0.1.0",
        "description": "FastAPI backend with LangGraph agents orchestrating MCP services",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "orchestrate": "/orchestrate (POST)",
            "chat": "/chat (POST)",
            "infrastructure": "/infrastructure/query (POST)",
            "inquiry": "/inquiry/query (POST)",
            "document": "/document/query (POST)"
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
