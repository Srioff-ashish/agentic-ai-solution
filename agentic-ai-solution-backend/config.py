"""Configuration for the backend"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # API Configuration
    API_TITLE = "Agentic AI Solution Backend"
    API_VERSION = "0.1.0"
    API_DESCRIPTION = "FastAPI backend with LangGraph agents"
    
    # Services
    MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:9000")
    INFRASTRUCTURE_SERVICE_URL = os.getenv("INFRASTRUCTURE_SERVICE_URL", "http://localhost:8000")
    INQUIRY_SERVICE_URL = os.getenv("INQUIRY_SERVICE_URL", "http://localhost:8000")
    DOCUMENT_SERVICE_URL = os.getenv("DOCUMENT_SERVICE_URL", "http://localhost:8000")
    
    # LLM Configuration
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic").lower()
    
    # Anthropic (Claude)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
    
    # Google Gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL", "gemini-2.0-flash")
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    # Default model name (for backward compatibility)
    MODEL_NAME = os.getenv("MODEL_NAME", ANTHROPIC_MODEL)
    
    # Agent Configuration
    MAX_ITERATIONS = 10
    TIMEOUT = 30
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
