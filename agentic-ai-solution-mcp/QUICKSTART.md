# Quick Start Guide - MCP Server

## 1️⃣ Prerequisites

Ensure the **FastAPI mock API server** is running on `http://localhost:8000`:

```bash
cd agentic-ai-solution-backend
poetry run python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 2️⃣ Start the MCP Server

```bash
cd agentic-ai-solution-mcp
poetry run python main.py
```

The server starts listening on stdin/stdout for MCP protocol messages.

## 3️⃣ Connect from Claude Desktop

Edit `~/.config/Claude/claude_desktop_config.json`:

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

Then restart Claude Desktop.

## 4️⃣ Test with Claude

In Claude, try:

> "Search for 'iPhone' in the products index"

Claude will call:
```
Tool: infra_search_documents
Arguments: {
  "index_id": "products",
  "query": "iPhone"
}
```

## 📚 Available Tools

### Quick Reference

**Search & Index:**
- `infra_search_documents` - Search products, users, orders
- `infra_list_indices` - See available indices

**Support Tickets:**
- `inquiry_list` - View all support tickets
- `inquiry_create` - Create new ticket
- `inquiry_search` - Find tickets by keyword

**Documents:**
- `document_list` - View documents
- `document_upload` - Upload new document
- `document_get_versions` - View document history

## 🔍 Example Conversations

### Example 1: Search Products
> "Search for iPhone in our products"

```
infra_search_documents(
  index_id="products",
  query="iPhone",
  limit=10
)
```

### Example 2: Create Support Ticket
> "I need to create a support ticket about login issues"

```
inquiry_create(
  title="Cannot login to account",
  description="User reports inability to login",
  customer_id="cust_001",
  priority="high",
  tags=["login", "account"]
)
```

### Example 3: Upload Document
> "Upload a Q4 report as an Excel file"

```
document_upload(
  filename="Q4_Report.xlsx",
  doc_type="spreadsheet",
  file_size=524288,
  upload_by="user_001",
  tags=["financial", "report"]
)
```

## ✅ Verification Checklist

- [ ] FastAPI server running on :8000
- [ ] MCP server starts without errors
- [ ] Claude Desktop restarted
- [ ] Tools visible in Claude
- [ ] Can call tools successfully

## 🐛 Troubleshooting

### MCP server won't start
```bash
# Check Python version
python --version  # Should be 3.13+

# Check dependencies
poetry install --no-root

# Run with error output
poetry run python main.py 2>&1
```

### Tools not visible in Claude
1. Check `claude_desktop_config.json` path
2. Verify MCP server starts without errors
3. Restart Claude Desktop
4. Check Claude logs for MCP connection errors

### API calls fail
1. Verify FastAPI server is running: `http://localhost:8000/docs`
2. Check firewall/network issues
3. Verify correct index_id/inquiry_id values

## 📖 Full Documentation

See `README.md` for complete tool documentation.

## 🚀 What's Next

Once MCP server is working:
1. Use Claude to interact with the services naturally
2. Create complex workflows combining multiple tools
3. Develop the UI (agentic-ai-solution-ui) to show results
4. Integrate with the backend API as needed
