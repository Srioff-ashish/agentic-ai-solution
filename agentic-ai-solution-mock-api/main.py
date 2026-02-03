import logging
import os
import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.routes.infrastructure_service import router as infra_router
from app.routes.inquiry_service import router as inquiry_router
from app.routes.document_service import router as document_router

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mock-api")

# Backend URL for log forwarding
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9001")

def forward_log(level: str, message: str):
    """Forward log to backend aggregator"""
    try:
        httpx.post(
            f"{BACKEND_URL}/logs/external",
            params={"module": "mock-api", "level": level, "message": message},
            timeout=1.0
        )
    except:
        pass  # Don't fail if backend is not available

app = FastAPI(
    title="Agentic AI Solution - Mock API",
    description="Mock API services for Payment and Transaction Inquiries",
    version="0.2.0",
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"📥 {request.method} {request.url.path}")
    forward_log("INFO", f"📥 {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"📤 {request.method} {request.url.path} -> {response.status_code}")
    forward_log("INFO", f"📤 {request.method} {request.url.path} -> {response.status_code}")
    return response

logger.info("═══════════════════════════════════════════════════════════════")
logger.info("🚀 Mock API Server Starting...")
logger.info(f"   Backend URL: {BACKEND_URL}")
logger.info("═══════════════════════════════════════════════════════════════")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(infra_router, prefix="/api/v1/infra", tags=["Infrastructure"])
app.include_router(inquiry_router, prefix="/api/v1/inquiry", tags=["Payment Inquiry"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Documents"])


@app.get("/health")
async def health_check():
    """Overall health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "infrastructure": "running",
            "payment_inquiry": "running",
            "documents": "running",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
