"""Configuration for the backend"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # API Configuration
    API_TITLE = "OMaaP Agentic AI Backend"
    API_VERSION = "0.2.0"
    API_DESCRIPTION = "FastAPI backend with LangGraph agents and MCP integration"
    
    # Services
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8002")
    MOCK_API_URL = os.getenv("MOCK_API_URL", "http://localhost:8001")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "vertexai").lower()
    
    # Google Vertex AI
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    VERTEX_AI_MODEL = os.getenv("VERTEX_AI_MODEL", "gemini-2.0-flash-001")
    
    # Fallback: Google Gemini API (for testing without Vertex AI setup)
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    # Anthropic (Claude) - fallback
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # OpenAI - fallback
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Agent Configuration
    MAX_ITERATIONS = 10
    TIMEOUT = 30
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

