# UI-Backend Integration Guide

## Overview
The frontend UI (Vite + React) is now fully integrated with the FastAPI backend running on port 9000.

## Architecture

```
User Browser (http://localhost:3000)
    ↓
React App (Vite Dev Server)
    ↓
API Service Layer (services/api.js)
    ↓
Backend FastAPI (http://localhost:9000)
    ↓
Orchestrator + Agents
    ↓
LLM Provider (Anthropic/Google/OpenAI)
```

## What's Been Configured

### 1. **Vite Configuration** (`vite.config.js`)
- UI runs on port 3000
- API proxy configured for development (can call `/api/*` endpoints)
- Backend URL set to `http://localhost:9000`

### 2. **API Service Layer** (`src/services/api.js`)
- Centralized API client using axios
- Methods for all backend endpoints:
  - `healthCheck()` - Verify backend is running
  - `chat(query)` - Send message to chat endpoint
  - `orchestrate(query)` - Route query to appropriate agent
  - `queryInfrastructure(query)` - Infrastructure agent
  - `queryInquiry(query)` - Inquiry agent
  - `queryDocument(query)` - Document agent
- Session management for tracking conversations
- Error handling with `handleApiError()`

### 3. **UI Components Updated**

#### ConversationUI.jsx
- Replaced mock API calls with actual backend calls
- Now calls `apiService.orchestrate(query)` for user messages
- Improved error handling and display

#### MessageBubble.jsx
- Added error state styling
- Error messages show with warning icon and red styling

### 4. **Environment Configuration**
- `.env` file created with `VITE_API_URL=http://localhost:9000`
- `.env.example` provided as template

## Running the Full Stack

### Terminal 1: Backend (Port 9000)
```powershell
cd c:\Users\ashish_srivastava\Downloads\agentic-ai-solution\agentic-ai-solution-backend
python -c "from main import app; from uvicorn import run; run(app, host='0.0.0.0', port=9000, log_level='info')"
```

**Status**: ✅ Already Running (Process ID: 14304)

### Terminal 2: Frontend (Port 3000)
```powershell
cd c:\Users\ashish_srivastava\Downloads\agentic-ai-solution\agentic-ai-solution-ui
npm run dev
```

**Status**: ✅ Already Running

## Testing the Integration

### 1. Access the UI
```
http://localhost:3000
```

### 2. Send a Test Message
Try typing in the conversation box:
- "What is cloud architecture?"
- "Tell me about microservices"
- "Explain DevOps best practices"

### 3. Monitor Responses
- Messages go to the orchestrator
- Orchestrator routes to appropriate agent (Infrastructure/Inquiry/Document)
- Agent queries the LLM (Anthropic Claude)
- Response appears in the chat

### 4. Backend API Documentation
Access Swagger UI for API testing:
```
http://localhost:9000/docs
```

## Key Features

✅ **Multi-LLM Support**
- Backend configured with Anthropic (default)
- Can switch to Google Gemini or OpenAI via environment variable
- UI automatically adapts to responses

✅ **Session Management**
- Each browser session gets unique session_id
- Stored in sessionStorage
- Enables multi-conversation tracking

✅ **Error Handling**
- Connection errors display helpful messages
- Backend errors shown in chat
- Graceful fallback if backend is down

✅ **CORS Enabled**
- Backend allows requests from all origins (development)
- Can be restricted in production

## API Endpoints Being Used

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend status |
| `/orchestrate` | POST | Main endpoint for queries |
| `/chat` | POST | Chat interface |
| `/infrastructure/query` | POST | Infrastructure queries |
| `/inquiry/query` | POST | Inquiry questions |
| `/document/query` | POST | Document queries |

## Request/Response Format

### Request
```json
{
  "query": "What is cloud architecture?"
}
```

### Response
```json
{
  "response": "Cloud architecture is...",
  "service_type": "infrastructure",
  "llm_provider": "anthropic"
}
```

## Troubleshooting

### Issue: "No response from server"
**Solution**: Make sure backend is running on port 9000
```powershell
# Check if backend is running
Get-NetTCPConnection -LocalPort 9000 -ErrorAction SilentlyContinue
```

### Issue: CORS Error
**Solution**: Backend CORS is enabled. Clear browser cache or try incognito mode.

### Issue: UI loads but no response
**Solution**: Check browser console (F12) for detailed errors. Verify:
- Backend is responding: `http://localhost:9000/health`
- API URL in .env is correct
- LLM API key is valid

### Issue: Backend error "ModuleNotFoundError"
**Solution**: Ensure dependencies are installed:
```powershell
cd agentic-ai-solution-backend
pip install -r requirements.txt
```

## Development Workflow

1. **Modify UI**: Changes auto-reload in browser
2. **Modify Backend**: Restart backend (not auto-reload in this setup)
3. **Test API**: Use Swagger UI at `http://localhost:9000/docs`
4. **Check Logs**: Monitor terminal output from both servers

## Building for Production

### Frontend Build
```powershell
cd agentic-ai-solution-ui
npm run build
```
Creates optimized build in `dist/` folder

### Backend Production
```powershell
# Use production ASGI server (gunicorn, etc.)
# Configure real LLM API keys
# Set CORS to specific origins
```

## Next Steps

1. ✅ UI connected to backend
2. ✅ API calls working
3. ⏳ Start MCP services on port 8000 (optional - for full agent integration)
4. ⏳ Test with different LLM providers (Google, OpenAI)
5. ⏳ Deploy to production environment

## Environment Variables Summary

### Frontend (.env)
```
VITE_API_URL=http://localhost:9000
VITE_ENV=development
```

### Backend (.env)
```
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-v0-...
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

## Support

For issues:
1. Check terminal logs for error messages
2. Use Swagger UI to test endpoints directly
3. Check browser console (F12) for frontend errors
4. Verify environment variables are set correctly

---

**Last Updated**: 2026-01-22
**Status**: ✅ Fully Integrated and Running
