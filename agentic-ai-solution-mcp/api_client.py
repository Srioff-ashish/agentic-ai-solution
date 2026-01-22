"""MCP Client for mock API services"""
import json
from typing import Any, Optional

import httpx
from pydantic import BaseModel


class APIClient:
    """Client for interacting with mock API services"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=10.0)

    def close(self):
        """Close the client"""
        self.client.close()

    # Infrastructure Service Methods
    def create_index(self, name: str, settings: Optional[dict] = None) -> dict:
        """Create a new search index"""
        response = self.client.post(
            "/api/v1/infra/indices",
            params={"name": name, **({"settings": json.dumps(settings)} if settings else {})},
        )
        response.raise_for_status()
        return response.json()

    def list_indices(self) -> list:
        """List all search indices"""
        response = self.client.get("/api/v1/infra/indices")
        response.raise_for_status()
        return response.json()

    def get_index(self, index_id: str) -> dict:
        """Get index details"""
        response = self.client.get(f"/api/v1/infra/indices/{index_id}")
        response.raise_for_status()
        return response.json()

    def index_document(
        self, index_id: str, content: str, metadata: Optional[dict] = None
    ) -> dict:
        """Index a document"""
        response = self.client.post(
            f"/api/v1/infra/indices/{index_id}/documents",
            params={"content": content, **({"metadata": json.dumps(metadata)} if metadata else {})},
        )
        response.raise_for_status()
        return response.json()

    def search_documents(
        self, index_id: str, query: str, limit: int = 10, offset: int = 0
    ) -> dict:
        """Search documents in index"""
        response = self.client.post(
            f"/api/v1/infra/indices/{index_id}/search",
            params={"query": query, "limit": limit, "offset": offset},
        )
        response.raise_for_status()
        return response.json()

    # Inquiry Service Methods
    def create_inquiry(
        self, title: str, description: str, customer_id: str, priority: str = "medium", tags: Optional[list] = None
    ) -> dict:
        """Create a new inquiry"""
        payload = {
            "title": title,
            "description": description,
            "customer_id": customer_id,
            "priority": priority,
            "tags": tags or [],
        }
        response = self.client.post("/api/v1/inquiries/", json=payload)
        response.raise_for_status()
        return response.json()

    def list_inquiries(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict:
        """List inquiries with filters"""
        params = {"skip": skip, "limit": limit}
        if status:
            params["status"] = status
        if priority:
            params["priority"] = priority
        response = self.client.get("/api/v1/inquiries/", params=params)
        response.raise_for_status()
        return response.json()

    def get_inquiry(self, inquiry_id: str) -> dict:
        """Get inquiry details"""
        response = self.client.get(f"/api/v1/inquiries/{inquiry_id}")
        response.raise_for_status()
        return response.json()

    def add_inquiry_response(
        self, inquiry_id: str, content: str, responder_id: str, is_internal: bool = False
    ) -> dict:
        """Add response to inquiry"""
        response = self.client.post(
            f"/api/v1/inquiries/{inquiry_id}/responses",
            params={"content": content, "responder_id": responder_id, "is_internal": is_internal},
        )
        response.raise_for_status()
        return response.json()

    def update_inquiry_status(self, inquiry_id: str, status: str) -> dict:
        """Update inquiry status"""
        response = self.client.put(
            f"/api/v1/inquiries/{inquiry_id}/status", params={"status": status}
        )
        response.raise_for_status()
        return response.json()

    def search_inquiries(self, query: str, skip: int = 0, limit: int = 20) -> dict:
        """Search inquiries"""
        response = self.client.get(
            "/api/v1/inquiries/search", params={"query": query, "skip": skip, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

    # Document Service Methods
    def upload_document(
        self,
        filename: str,
        doc_type: str,
        file_size: int,
        upload_by: str,
        metadata: Optional[dict] = None,
        tags: Optional[list] = None,
    ) -> dict:
        """Upload a document"""
        params = {
            "filename": filename,
            "doc_type": doc_type,
            "file_size": file_size,
            "upload_by": upload_by,
        }
        if metadata:
            params["metadata"] = json.dumps(metadata)
        if tags:
            params["tags"] = json.dumps(tags)
        response = self.client.post("/api/v1/documents/upload", params=params)
        response.raise_for_status()
        return response.json()

    def list_documents(
        self,
        doc_type: Optional[str] = None,
        upload_by: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict:
        """List documents"""
        params = {"skip": skip, "limit": limit}
        if doc_type:
            params["doc_type"] = doc_type
        if upload_by:
            params["upload_by"] = upload_by
        response = self.client.get("/api/v1/documents/", params=params)
        response.raise_for_status()
        return response.json()

    def get_document(self, doc_id: str) -> dict:
        """Get document details"""
        response = self.client.get(f"/api/v1/documents/{doc_id}")
        response.raise_for_status()
        return response.json()

    def get_document_versions(self, doc_id: str) -> list:
        """Get document versions"""
        response = self.client.get(f"/api/v1/documents/{doc_id}/versions")
        response.raise_for_status()
        return response.json()

    def get_document_preview(self, doc_id: str) -> dict:
        """Get document preview"""
        response = self.client.get(f"/api/v1/documents/{doc_id}/preview")
        response.raise_for_status()
        return response.json()

    def create_document_version(
        self,
        doc_id: str,
        new_filename: str,
        new_file_size: int,
        created_by: str,
        change_description: Optional[str] = None,
    ) -> dict:
        """Create document version"""
        params = {
            "new_filename": new_filename,
            "new_file_size": new_file_size,
            "created_by": created_by,
        }
        if change_description:
            params["change_description"] = change_description
        response = self.client.post(f"/api/v1/documents/{doc_id}/versions", params=params)
        response.raise_for_status()
        return response.json()

    def health_check(self) -> dict:
        """Check overall health"""
        response = self.client.get("/health")
        response.raise_for_status()
        return response.json()
