# Agentic AI Solution - FastAPI Backend

FastAPI backend with LangGraph agents that orchestrate requests to three different services via MCP (Model Context Protocol).

## Architecture

```
UI (Frontend)
    ↓ (HTTP Requests)
FastAPI Backend (Port 9000)
├─ Orchestrator
│  ├─ Infrastructure Agent (LangGraph)
│  ├─ Inquiry Agent (LangGraph)
│  └─ Document Agent (LangGraph)
    ↓ (HTTP Requests)
MCP Services (Port 8000)
├─ Infrastructure Service (Search/Index)
├─ Inquiry Service (Support Tickets)
└─ Document Service (File Management)
```

## Features

- **FastAPI**: Modern async Python web framework
- **Multi-LLM Support**: Use Anthropic Claude, Google Gemini, or OpenAI GPT-4o
- **Orchestration**: Automatic routing to appropriate service/agent
- **Error Handling**: Comprehensive error handling and logging
- **Async/Await**: Full async support for scalability
- **CORS**: Enabled for frontend integration
- **Configurable**: Easy switching between LLM providers via environment variables

## Prerequisites

- Python 3.11+
- Poetry 2.3.1+
- At least one LLM provider API key:
  - **Anthropic**: For Claude 3.5 Sonnet
  - **Google**: For Gemini 2.0 Flash
  - **OpenAI**: For GPT-4o
- FastAPI mock services running on port 8000

## Installation

```bash
# Install core dependencies only
poetry install --no-root

# Or install with all LLM providers
poetry install --all-extras --no-root

# Or install with specific provider(s)
poetry install --extras google --no-root      # Google Gemini
poetry install --extras openai --no-root      # OpenAI
poetry install --extras all-llms --no-root    # All providers

# Create .env file
cp .env.example .env

# Edit .env and set your desired LLM_PROVIDER and API key(s)
```

## Configuration

### LLM Provider Selection

Set the `LLM_PROVIDER` environment variable to choose your LLM:

```bash
# Use Anthropic Claude (default)
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Or use Google Gemini
LLM_PROVIDER=google
GOOGLE_API_KEY=AIzaSy...
GOOGLE_MODEL=gemini-2.0-flash

# Or use OpenAI GPT-4o
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o
```

### Supported LLM Providers

| Provider | Model | Model Name | Speed | Cost |
|----------|-------|-----------|-------|------|
| Anthropic | Claude 3.5 Sonnet | `claude-3-5-sonnet-20241022` | Fast | $$$ |
| Google | Gemini 2.0 Flash | `gemini-2.0-flash` | Very Fast | $$ |
| OpenAI | GPT-4o | `gpt-4o` | Fast | $$$$ |

### Getting API Keys

1. **Anthropic**: https://console.anthropic.com/
2. **Google**: https://ai.google.dev/
3. **OpenAI**: https://platform.openai.com/

## Running the Backend

```bash
# Start the backend server
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 9000
```

The API will be available at:
- `http://localhost:9000` - Main API
- `http://localhost:9000/docs` - Swagger UI
- `http://localhost:9000/redoc` - ReDoc

## API Endpoints

### Health Check
```bash
GET /health
```

### Main Orchestration
```bash
POST /orchestrate
{
  "query": "Search for iPhone in products",
  "user_id": "user_001",
  "params": {}
}
```

### Chat Interface
```bash
POST /chat
{
  "message": "Search for iPhone",
  "conversation_history": [],
  "user_id": "user_001"
}
```

### Service-Specific Queries
```bash
POST /infrastructure/query
POST /inquiry/query
POST /document/query
```

## Request/Response Models

### OrchestratorRequest
```json
{
  "query": "Your request",
  "service": "infrastructure|inquiry|document",
  "params": {},
  "user_id": "user_id",
  "context": {}
}
```

### OrchestratorResponse
```json
{
  "query": "Your request",
  "service_type": "infrastructure",
  "agent_response": {
    "agent_type": "infrastructure",
    "action": "search",
    "result": {},
    "reasoning": "Why this action was taken",
    "tool_calls": [],
    "success": true
  },
  "final_result": {},
  "status": "success",
  "message": "Query processed"
}
```

## Configuration

Edit `.env` file to configure:
- `ANTHROPIC_API_KEY` - Your Claude API key
- `MODEL_NAME` - LLM model to use
- `SERVICE_URLs` - Backend service endpoints
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)

## Architecture Details

### Orchestrator
Routes requests to appropriate service based on query analysis.

### Agents (LangGraph)
Each service has an agent that:
1. **Analyzes** the query to determine action
2. **Plans** the execution strategy
3. **Executes** the necessary tools/MCP calls
4. **Processes** and formats the result

### MCP Client
Communicates with the FastAPI mock services.

## Example Usage

### Search Products
```python
import httpx

response = httpx.post(
    "http://localhost:9000/orchestrate",
    json={
        "query": "Search for iPhone in products",
        "user_id": "user_001"
    }
)
print(response.json())
```

### Chat Interface
```python
response = httpx.post(
    "http://localhost:9000/chat",
    json={
        "message": "Create a support ticket for login issues",
        "user_id": "user_001"
    }
)
print(response.json())
```

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200 OK` - Request successful
- `400 Bad Request` - Invalid parameters
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Services not initialized

## Logging

Logs are output to console with configurable level.

## Development

### Adding New Agents

1. Create agent class in `agents.py`
2. Implement `run()` method
3. Add routing logic in `orchestrator.py`

### Adding New Endpoints

1. Add route in `main.py`
2. Define request/response models in `models.py`
3. Implement handler logic

## Testing

The API can be tested using:
- Swagger UI: `http://localhost:9000/docs`
- ReDoc: `http://localhost:9000/redoc`
- cURL, Postman, or your preferred HTTP client

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.13+

# Reinstall dependencies
poetry install --no-root
```

### Services not responding
- Verify mock API is running on port 8000
- Check firewall settings
- Verify ANTHROPIC_API_KEY is set

### LLM errors
- Verify Anthropic API key is correct
- Check internet connection
- Verify API quota

## Dependencies

- **fastapi** (0.110.0) - Web framework
- **uvicorn** (0.27.0) - ASGI server
- **pydantic** (2.7.0) - Data validation
- **langgraph** (0.2.0) - Agent framework
- **langchain** (0.2.0) - LLM utilities
- **langchain-anthropic** (0.1.0) - Claude integration
- **httpx** (0.27.0) - HTTP client
- **python-dotenv** (1.0.0) - Environment variables

## Status

✅ Backend API implemented
✅ Orchestrator with service routing
✅ Infrastructure agent (LangGraph)
⏳ Inquiry agent (to be implemented)
⏳ Document agent (to be implemented)
⏳ UI integration (to be completed)

## Next Steps

1. Run backend: `poetry run uvicorn main:app --reload --port 9000`
2. Test endpoints in Swagger UI
3. Integrate UI with backend
4. Implement remaining agents

---

**Created**: 2024
**Python**: 3.13+
**Framework**: FastAPI + LangGraph
