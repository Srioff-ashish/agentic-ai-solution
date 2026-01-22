# Agentic AI Solution - MCP Server

MCP (Model Context Protocol) server that exposes the mock API services (Infrastructure, Inquiry, Document) to LLMs and other MCP clients.

## Overview

This MCP server acts as a bridge between:
- **LLM/Client side**: Claude, other LLMs, or MCP client applications
- **Backend services**: FastAPI mock services running on `http://localhost:8000`

The server exposes **22+ tools** covering:
- Infrastructure Service: Index management, document indexing, full-text search
- Inquiry Service: Ticket management, response handling, status tracking
- Document Service: Document upload, versioning, preview generation

## Prerequisites

- Python 3.13+
- Poetry 2.3.1+
- FastAPI mock API server running on `http://localhost:8000`

## Installation

```bash
# Install dependencies using Poetry
poetry install --no-root
```

## Usage

### Running the MCP Server

```bash
# Start the MCP server
poetry run python main.py
```

The server will start and listen on stdin/stdout for MCP protocol messages.

### Connecting from Claude Desktop

Add to your Claude `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "agentic-ai-solution": {
      "command": "poetry",
      "args": ["run", "python", "main.py"],
      "cwd": "c:\\Users\\ashish_srivastava\\Downloads\\agentic-ai-solution\\agentic-ai-solution-mcp"
    }
  }
}
```

## Available Tools

### Infrastructure Service (5 tools)

- **infra_list_indices**: List all search indices
- **infra_create_index**: Create a new search index
- **infra_get_index**: Get details of a search index
- **infra_index_document**: Index a document in a search index
- **infra_search_documents**: Search documents with full-text query

### Inquiry Service (6 tools)

- **inquiry_list**: List inquiries with optional filters (status, priority)
- **inquiry_create**: Create a new support ticket/inquiry
- **inquiry_get**: Get details of a specific inquiry
- **inquiry_add_response**: Add a response to an inquiry
- **inquiry_update_status**: Update inquiry status (open, in_progress, resolved, closed)
- **inquiry_search**: Search inquiries by title or description

### Document Service (6 tools)

- **document_list**: List documents with optional filters
- **document_upload**: Upload a document with metadata
- **document_get**: Get document details
- **document_preview**: Get document preview
- **document_get_versions**: Get all versions of a document
- **document_create_version**: Create a new version of a document

## Example Tool Calls

### Search Products by Name

```
Tool: infra_search_documents
Arguments:
  index_id: "products"
  query: "iPhone"
  limit: 10
```

### Create a Support Ticket

```
Tool: inquiry_create
Arguments:
  title: "Cannot login to account"
  description: "I'm unable to login to my account with my credentials"
  customer_id: "cust_001"
  priority: "high"
  tags: ["login", "account"]
```

### Upload a Document

```
Tool: document_upload
Arguments:
  filename: "Q4_Report.xlsx"
  doc_type: "spreadsheet"
  file_size: 524288
  upload_by: "user_001"
  metadata: {"year": 2024, "quarter": "Q4"}
  tags: ["financial", "report"]
```

## Architecture

```
┌─────────────────────────────┐
│  LLM / MCP Client           │
│ (Claude, etc)               │
└──────────────┬──────────────┘
               │ MCP Protocol (stdin/stdout)
               │
┌──────────────▼──────────────┐
│  MCP Server (main.py)       │
│  ├─ Tool Definitions        │
│  └─ Tool Handlers           │
└──────────────┬──────────────┘
               │ HTTP Requests
               │
┌──────────────▼──────────────┐
│  API Client (api_client.py) │
│  Wraps HTTP Calls           │
└──────────────┬──────────────┘
               │ HTTP
               │
┌──────────────▼──────────────┐
│  FastAPI Mock Services      │
│  - Infrastructure Service   │
│  - Inquiry Service          │
│  - Document Service         │
└─────────────────────────────┘
```

## File Structure

```
agentic-ai-solution-mcp/
├── main.py                 # MCP server with tool definitions and handlers
├── api_client.py          # HTTP client wrapper for API calls
├── pyproject.toml         # Poetry configuration (Python 3.13)
└── README.md             # This file
```

## Configuration

### API Base URL

The MCP server connects to the FastAPI backend at `http://localhost:8000` by default.

To change the base URL, edit `api_client.py`:

```python
api_client = APIClient(base_url="http://your-api-url:port")
```

## Error Handling

All tools return error messages on failure:
- Connection errors (API unreachable)
- Invalid parameters
- Resource not found errors
- API validation errors

## Performance

- Tools execute synchronously with ~200-500ms latency
- Supports batch operations (bulk document upload, search with pagination)
- Response sizes: Small (< 1KB) for create operations, up to 50KB for list operations

## Development

### Adding New Tools

1. Add tool definition in `main.py` under the appropriate service section
2. Add handler logic in `handle_call_tool()` function
3. Add corresponding method in `api_client.py` if needed

### Testing

```bash
# Test imports
poetry run python -c "from main import server, api_client; print('OK')"

# Run with debug logging
PYTHONUNBUFFERED=1 poetry run python main.py
```

## Dependencies

- **mcp** (0.9.1+): Model Context Protocol library
- **httpx** (0.27.0+): HTTP client for API calls
- **pydantic** (2.7.0+): Data validation

## License

Part of the Agentic AI Solution project.

## Support

For issues:
1. Verify FastAPI mock API is running on port 8000
2. Check Python 3.13+ is installed
3. Run `poetry install --no-root` to ensure dependencies
