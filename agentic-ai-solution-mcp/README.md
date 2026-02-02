# Agentic AI Solution - MCP Server

MCP (Model Context Protocol) server using **FastMCP** that exposes Payment and Transaction Inquiry services to LLMs and MCP clients.

## Overview

This MCP server acts as a bridge between:
- **LLM/Client side**: Claude, other LLMs, or MCP client applications
- **Backend services**: FastAPI mock services running on `http://localhost:8000`

The server exposes **11 tools** for:
- Payment Inquiry: Search, list, and retrieve payment details
- Transaction Inquiry: Search, list, and retrieve transaction details
- Statistics: Get payment/transaction status breakdowns

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
# Start the MCP server (stdio mode)
poetry run python main.py

# Or use fastmcp directly
poetry run fastmcp run main.py
```

### Connecting from Claude Desktop

Add to your Claude `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "payment-inquiry": {
      "command": "poetry",
      "args": ["run", "python", "main.py"],
      "cwd": "c:\\Users\\ashish_srivastava\\Downloads\\agentic-ai-solution\\agentic-ai-solution-mcp"
    }
  }
}
```

## Available Tools

### Health & Statistics (2 tools)

| Tool | Description |
|------|-------------|
| `health_check` | Check overall API health status |
| `get_inquiry_stats` | Get payment and transaction statistics with status breakdown |

### Payment Tools (5 tools)

| Tool | Description |
|------|-------------|
| `list_payments` | List all payments with pagination |
| `search_payments` | Search payments by ID, message ID, IBAN, status, channel, product, date range |
| `get_payment` | Get payment details by payment ID |
| `get_payment_with_transactions` | Get payment with all associated transactions |
| `get_payment_by_message_id` | Get payment by message ID |

### Transaction Tools (4 tools)

| Tool | Description |
|------|-------------|
| `list_transactions` | List all transactions with pagination |
| `search_transactions` | Search by ID, payment ID, E2E ID, IBAN, status, amount, currency, date range |
| `get_transaction` | Get transaction details by transaction ID |
| `get_transactions_by_payment` | Get all transactions for a payment |
| `get_transaction_by_end_to_end_id` | Get transaction by end-to-end ID |

## Status Codes

### Payment Statuses
- `RCVD` - Received
- `ACTC` - Accepted Technical Validation
- `ACCP` - Accepted Customer Profile  
- `ACSP` - Accepted Settlement in Process
- `ACSC` - Accepted Settlement Completed
- `IAUT` - In Authorization
- `RJCT` - Rejected

### Transaction Statuses
- `ACTC` - Accepted Technical Validation
- `ACSC` - Accepted Settlement Completed
- `RJCT` - Rejected

## Example Tool Calls

### Get Payment Statistics

```
Tool: get_inquiry_stats
Arguments: {}
```

### Search Rejected Payments

```
Tool: search_payments
Arguments:
  status: "RJCT"
  limit: 10
```

### Get Payment with Transactions

```
Tool: get_payment_with_transactions
Arguments:
  pmt_id: "d145a790-8ef1-4776-8e98-92dad80f0a9d"
```

### Search Transactions by IBAN

```
Tool: search_transactions
Arguments:
  iban: "NL19INGB0588118729"
  limit: 20
```

### Search Transactions by Amount Range

```
Tool: search_transactions
Arguments:
  amount_min: 0.01
  amount_max: 100.00
  currency: "EUR"
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
│  FastMCP Server (main.py)   │
│  ├─ @mcp.tool() decorators  │
│  └─ Tool functions          │
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
│  - Payment Inquiry API      │
│  - /api/v1/inquiry/*        │
└─────────────────────────────┘
```

## File Structure

```
agentic-ai-solution-mcp/
├── main.py                 # FastMCP server with tool definitions
├── api_client.py          # HTTP client wrapper for API calls
├── pyproject.toml         # Poetry configuration
└── README.md              # This file
```

## Configuration

### API Base URL

The MCP server connects to the FastAPI backend at `http://localhost:8000` by default.

To change the base URL, update the `get_client()` call in `api_client.py`:

```python
def get_client(base_url: str = "http://your-api-url:port") -> APIClient:
```

## Error Handling

All tools return error messages on failure:
- Connection errors (API unreachable)
- Invalid parameters
- Resource not found errors (404)
- API validation errors

## Development

### Adding New Tools

With FastMCP, simply add a new decorated function:

```python
@mcp.tool()
def my_new_tool(param1: str, param2: int = 10) -> str:
    """
    Tool description here.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 10)
    
    Returns:
        JSON response
    """
    client = get_client()
    result = client.some_method(param1, param2)
    return json.dumps(result, indent=2)
```

### Testing

```bash
# Test imports
poetry run python -c "from main import mcp; print('OK')"

# List available tools
poetry run fastmcp dev main.py

# Run server
poetry run python main.py
```

## Dependencies

- **fastmcp** (2.3.4+): FastMCP library for easy MCP server creation
- **httpx** (0.27.0+): HTTP client for API calls
- **pydantic** (2.7.0+): Data validation

## License

Part of the Agentic AI Solution project.
