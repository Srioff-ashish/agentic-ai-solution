"""MCP Client for communicating with MCP server"""

import httpx
import json
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)


class MCPClient:
    """Client to call MCP tools via HTTP interface (for debugging/testing)
    
    In production, this would communicate with the actual MCP server.
    For now, this provides a bridge to test tool availability.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)
    
    async def health_check(self) -> bool:
        """Check if MCP server is healthy"""
        try:
            response = await self.client.get("/health")
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
    
    # Infrastructure Service Tools
    async def infra_list_indices(self) -> dict[str, Any]:
        """List all search indices"""
        try:
            response = await self.client.get("/infrastructure/indices")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def infra_search_documents(self, index_id: str, query: str, limit: int = 10) -> dict[str, Any]:
        """Search documents in an index"""
        try:
            response = await self.client.post(
                "/infrastructure/search",
                json={"index_id": index_id, "query": query, "limit": limit}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def infra_create_index(self, name: str, settings: Optional[dict] = None) -> dict[str, Any]:
        """Create a new search index"""
        try:
            response = await self.client.post(
                "/infrastructure/indices",
                json={"name": name, "settings": settings or {}}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def infra_get_index(self, index_id: str) -> dict[str, Any]:
        """Get index details"""
        try:
            response = await self.client.get(f"/infrastructure/indices/{index_id}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def infra_index_document(self, index_id: str, content: str, metadata: Optional[dict] = None) -> dict[str, Any]:
        """Index a document"""
        try:
            response = await self.client.post(
                "/infrastructure/index",
                json={"index_id": index_id, "content": content, "metadata": metadata or {}}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    # Inquiry Service Tools
    async def inquiry_list(self, status: Optional[str] = None, priority: Optional[str] = None) -> dict[str, Any]:
        """List inquiries"""
        try:
            params = {}
            if status:
                params["status"] = status
            if priority:
                params["priority"] = priority
            response = await self.client.get("/inquiry/inquiries", params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def inquiry_create(self, title: str, description: str, customer_id: str, priority: str = "medium", tags: Optional[list] = None) -> dict[str, Any]:
        """Create an inquiry"""
        try:
            response = await self.client.post(
                "/inquiry/inquiries",
                json={
                    "title": title,
                    "description": description,
                    "customer_id": customer_id,
                    "priority": priority,
                    "tags": tags or []
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def inquiry_get(self, inquiry_id: str) -> dict[str, Any]:
        """Get inquiry details"""
        try:
            response = await self.client.get(f"/inquiry/inquiries/{inquiry_id}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def inquiry_search(self, query: str) -> dict[str, Any]:
        """Search inquiries"""
        try:
            response = await self.client.get("/inquiry/search", params={"query": query})
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def inquiry_add_response(self, inquiry_id: str, content: str, responder_id: str, is_internal: bool = False) -> dict[str, Any]:
        """Add response to inquiry"""
        try:
            response = await self.client.post(
                f"/inquiry/inquiries/{inquiry_id}/responses",
                json={"content": content, "responder_id": responder_id, "is_internal": is_internal}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def inquiry_update_status(self, inquiry_id: str, status: str) -> dict[str, Any]:
        """Update inquiry status"""
        try:
            response = await self.client.patch(
                f"/inquiry/inquiries/{inquiry_id}",
                json={"status": status}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    # Document Service Tools
    async def document_list(self, doc_type: Optional[str] = None) -> dict[str, Any]:
        """List documents"""
        try:
            params = {}
            if doc_type:
                params["doc_type"] = doc_type
            response = await self.client.get("/documents/documents", params=params)
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def document_upload(self, filename: str, doc_type: str, file_size: int, upload_by: str, metadata: Optional[dict] = None, tags: Optional[list] = None) -> dict[str, Any]:
        """Upload a document"""
        try:
            response = await self.client.post(
                "/documents/documents",
                json={
                    "filename": filename,
                    "doc_type": doc_type,
                    "file_size": file_size,
                    "upload_by": upload_by,
                    "metadata": metadata or {},
                    "tags": tags or []
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def document_get(self, doc_id: str) -> dict[str, Any]:
        """Get document details"""
        try:
            response = await self.client.get(f"/documents/documents/{doc_id}")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def document_get_versions(self, doc_id: str) -> dict[str, Any]:
        """Get document versions"""
        try:
            response = await self.client.get(f"/documents/documents/{doc_id}/versions")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def document_get_preview(self, doc_id: str) -> dict[str, Any]:
        """Get document preview"""
        try:
            response = await self.client.get(f"/documents/documents/{doc_id}/preview")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def document_create_version(self, doc_id: str, new_filename: str, new_file_size: int, created_by: str, change_description: Optional[str] = None) -> dict[str, Any]:
        """Create document version"""
        try:
            response = await self.client.post(
                f"/documents/documents/{doc_id}/versions",
                json={
                    "new_filename": new_filename,
                    "new_file_size": new_file_size,
                    "created_by": created_by,
                    "change_description": change_description or ""
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
