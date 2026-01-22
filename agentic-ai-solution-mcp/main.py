"""MCP Server implementation for mock API services"""
import asyncio
import json
import mcp.server.stdio

from mcp.server import Server, InitializationOptions, NotificationOptions
from mcp.types import Tool, TextContent

from api_client import APIClient

# Initialize API client
api_client = APIClient(base_url="http://localhost:8000")

# Create the server instance
server = Server("agentic-ai-solution-mcp")


# Define tools for Infrastructure Service
infrastructure_tools = [
    Tool(
        name="infra_list_indices",
        description="List all search indices in the infrastructure service",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    ),
    Tool(
        name="infra_create_index",
        description="Create a new search index",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Index name"},
                "settings": {
                    "type": "object",
                    "description": "Index settings (e.g., replicas, shards)",
                },
            },
            "required": ["name"],
        },
    ),
    Tool(
        name="infra_get_index",
        description="Get details of a specific search index",
        inputSchema={
            "type": "object",
            "properties": {
                "index_id": {"type": "string", "description": "Index ID"},
            },
            "required": ["index_id"],
        },
    ),
    Tool(
        name="infra_index_document",
        description="Index a document in a search index",
        inputSchema={
            "type": "object",
            "properties": {
                "index_id": {"type": "string", "description": "Index ID"},
                "content": {"type": "string", "description": "Document content"},
                "metadata": {
                    "type": "object",
                    "description": "Document metadata",
                },
            },
            "required": ["index_id", "content"],
        },
    ),
    Tool(
        name="infra_search_documents",
        description="Search documents in an index",
        inputSchema={
            "type": "object",
            "properties": {
                "index_id": {"type": "string", "description": "Index ID"},
                "query": {"type": "string", "description": "Search query"},
                "limit": {
                    "type": "integer",
                    "description": "Max results (default: 10)",
                    "default": 10,
                },
                "offset": {
                    "type": "integer",
                    "description": "Result offset (default: 0)",
                    "default": 0,
                },
            },
            "required": ["index_id", "query"],
        },
    ),
]

# Define tools for Inquiry Service
inquiry_tools = [
    Tool(
        name="inquiry_list",
        description="List inquiries with optional filters",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {
                    "type": "string",
                    "description": "Filter by status (open, in_progress, resolved, closed)",
                },
                "priority": {
                    "type": "string",
                    "description": "Filter by priority (low, medium, high, critical)",
                },
                "skip": {
                    "type": "integer",
                    "description": "Skip count (default: 0)",
                    "default": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Limit count (default: 20)",
                    "default": 20,
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="inquiry_create",
        description="Create a new inquiry",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {"type": "string", "description": "Inquiry title"},
                "description": {"type": "string", "description": "Detailed description"},
                "customer_id": {"type": "string", "description": "Customer/User ID"},
                "priority": {
                    "type": "string",
                    "description": "Priority (default: medium)",
                    "default": "medium",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Tags for categorization",
                },
            },
            "required": ["title", "description", "customer_id"],
        },
    ),
    Tool(
        name="inquiry_get",
        description="Get inquiry details",
        inputSchema={
            "type": "object",
            "properties": {
                "inquiry_id": {"type": "string", "description": "Inquiry ID"},
            },
            "required": ["inquiry_id"],
        },
    ),
    Tool(
        name="inquiry_add_response",
        description="Add response to an inquiry",
        inputSchema={
            "type": "object",
            "properties": {
                "inquiry_id": {"type": "string", "description": "Inquiry ID"},
                "content": {"type": "string", "description": "Response content"},
                "responder_id": {"type": "string", "description": "Responder ID"},
                "is_internal": {
                    "type": "boolean",
                    "description": "Is internal response (default: false)",
                    "default": False,
                },
            },
            "required": ["inquiry_id", "content", "responder_id"],
        },
    ),
    Tool(
        name="inquiry_update_status",
        description="Update inquiry status",
        inputSchema={
            "type": "object",
            "properties": {
                "inquiry_id": {"type": "string", "description": "Inquiry ID"},
                "status": {
                    "type": "string",
                    "description": "New status (open, in_progress, resolved, closed)",
                },
            },
            "required": ["inquiry_id", "status"],
        },
    ),
    Tool(
        name="inquiry_search",
        description="Search inquiries by title or description",
        inputSchema={
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "skip": {
                    "type": "integer",
                    "description": "Skip count (default: 0)",
                    "default": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Limit count (default: 20)",
                    "default": 20,
                },
            },
            "required": ["query"],
        },
    ),
]

# Define tools for Document Service
document_tools = [
    Tool(
        name="document_list",
        description="List documents with optional filters",
        inputSchema={
            "type": "object",
            "properties": {
                "doc_type": {
                    "type": "string",
                    "description": "Filter by type (pdf, text, image, spreadsheet, presentation, archive)",
                },
                "upload_by": {"type": "string", "description": "Filter by uploader"},
                "skip": {
                    "type": "integer",
                    "description": "Skip count (default: 0)",
                    "default": 0,
                },
                "limit": {
                    "type": "integer",
                    "description": "Limit count (default: 20)",
                    "default": 20,
                },
            },
            "required": [],
        },
    ),
    Tool(
        name="document_upload",
        description="Upload a document",
        inputSchema={
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "Original filename"},
                "doc_type": {
                    "type": "string",
                    "description": "Document type (pdf, text, image, spreadsheet, presentation, archive)",
                },
                "file_size": {"type": "integer", "description": "File size in bytes"},
                "upload_by": {"type": "string", "description": "User ID uploading"},
                "metadata": {
                    "type": "object",
                    "description": "Custom metadata",
                },
                "tags": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Document tags",
                },
            },
            "required": ["filename", "doc_type", "file_size", "upload_by"],
        },
    ),
    Tool(
        name="document_get",
        description="Get document details",
        inputSchema={
            "type": "object",
            "properties": {
                "doc_id": {"type": "string", "description": "Document ID"},
            },
            "required": ["doc_id"],
        },
    ),
    Tool(
        name="document_preview",
        description="Get document preview",
        inputSchema={
            "type": "object",
            "properties": {
                "doc_id": {"type": "string", "description": "Document ID"},
            },
            "required": ["doc_id"],
        },
    ),
    Tool(
        name="document_get_versions",
        description="Get document versions",
        inputSchema={
            "type": "object",
            "properties": {
                "doc_id": {"type": "string", "description": "Document ID"},
            },
            "required": ["doc_id"],
        },
    ),
    Tool(
        name="document_create_version",
        description="Create document version",
        inputSchema={
            "type": "object",
            "properties": {
                "doc_id": {"type": "string", "description": "Document ID"},
                "new_filename": {"type": "string", "description": "New filename"},
                "new_file_size": {"type": "integer", "description": "New file size in bytes"},
                "created_by": {"type": "string", "description": "User ID creating version"},
                "change_description": {
                    "type": "string",
                    "description": "Description of changes",
                },
            },
            "required": ["doc_id", "new_filename", "new_file_size", "created_by"],
        },
    ),
]


# Tool implementations
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available tools"""
    return infrastructure_tools + inquiry_tools + document_tools


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""
    try:
        if name == "infra_list_indices":
            result = api_client.list_indices()
        elif name == "infra_create_index":
            result = api_client.create_index(
                arguments["name"],
                arguments.get("settings"),
            )
        elif name == "infra_get_index":
            result = api_client.get_index(arguments["index_id"])
        elif name == "infra_index_document":
            result = api_client.index_document(
                arguments["index_id"],
                arguments["content"],
                arguments.get("metadata"),
            )
        elif name == "infra_search_documents":
            result = api_client.search_documents(
                arguments["index_id"],
                arguments["query"],
                arguments.get("limit", 10),
                arguments.get("offset", 0),
            )
        elif name == "inquiry_list":
            result = api_client.list_inquiries(
                arguments.get("status"),
                arguments.get("priority"),
                arguments.get("skip", 0),
                arguments.get("limit", 20),
            )
        elif name == "inquiry_create":
            result = api_client.create_inquiry(
                arguments["title"],
                arguments["description"],
                arguments["customer_id"],
                arguments.get("priority", "medium"),
                arguments.get("tags"),
            )
        elif name == "inquiry_get":
            result = api_client.get_inquiry(arguments["inquiry_id"])
        elif name == "inquiry_add_response":
            result = api_client.add_inquiry_response(
                arguments["inquiry_id"],
                arguments["content"],
                arguments["responder_id"],
                arguments.get("is_internal", False),
            )
        elif name == "inquiry_update_status":
            result = api_client.update_inquiry_status(
                arguments["inquiry_id"],
                arguments["status"],
            )
        elif name == "inquiry_search":
            result = api_client.search_inquiries(
                arguments["query"],
                arguments.get("skip", 0),
                arguments.get("limit", 20),
            )
        elif name == "document_list":
            result = api_client.list_documents(
                arguments.get("doc_type"),
                arguments.get("upload_by"),
                arguments.get("skip", 0),
                arguments.get("limit", 20),
            )
        elif name == "document_upload":
            result = api_client.upload_document(
                arguments["filename"],
                arguments["doc_type"],
                arguments["file_size"],
                arguments["upload_by"],
                arguments.get("metadata"),
                arguments.get("tags"),
            )
        elif name == "document_get":
            result = api_client.get_document(arguments["doc_id"])
        elif name == "document_preview":
            result = api_client.get_document_preview(arguments["doc_id"])
        elif name == "document_get_versions":
            result = api_client.get_document_versions(arguments["doc_id"])
        elif name == "document_create_version":
            result = api_client.create_document_version(
                arguments["doc_id"],
                arguments["new_filename"],
                arguments["new_file_size"],
                arguments["created_by"],
                arguments.get("change_description"),
            )
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Main entry point"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="agentic-ai-solution-mcp",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


if __name__ == "__main__":
    asyncio.run(main())
