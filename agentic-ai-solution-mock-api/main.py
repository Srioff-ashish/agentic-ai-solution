from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.infrastructure_service import router as infra_router
from app.routes.inquiry_service import router as inquiry_router
from app.routes.document_service import router as document_router

app = FastAPI(
    title="Agentic AI Solution - Mock API",
    description="Mock API services for Agentic AI Solution",
    version="0.1.0",
)

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
app.include_router(inquiry_router, prefix="/api/v1/inquiries", tags=["Inquiries"])
app.include_router(document_router, prefix="/api/v1/documents", tags=["Documents"])


@app.get("/health")
async def health_check():
    """Overall health check endpoint"""
    return {
        "status": "healthy",
        "services": {
            "infrastructure": "running",
            "inquiries": "running",
            "documents": "running",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
