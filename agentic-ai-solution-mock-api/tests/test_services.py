"""Example usage and integration tests for mock services"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestInfrastructureService:
    """Infrastructure service tests"""

    def test_health_check(self):
        """Test infrastructure health endpoint"""
        response = client.get("/api/v1/infra/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_index(self):
        """Test creating a search index"""
        response = client.post(
            "/api/v1/infra/indices",
            params={"name": "test-index", "settings": {"replicas": 1}},
        )
        assert response.status_code == 200
        assert response.json()["name"] == "test-index"

    def test_list_indices(self):
        """Test listing indices"""
        client.post("/api/v1/infra/indices", params={"name": "index1"})
        client.post("/api/v1/infra/indices", params={"name": "index2"})

        response = client.get("/api/v1/infra/indices")
        assert response.status_code == 200
        assert len(response.json()) >= 2

    def test_index_document(self):
        """Test indexing a document"""
        # Create index
        index_resp = client.post("/api/v1/infra/indices", params={"name": "docs"})
        index_id = index_resp.json()["index_id"]

        # Index document
        response = client.post(
            f"/api/v1/infra/indices/{index_id}/documents",
            params={
                "content": "This is a test document",
                "metadata": {"author": "test_user"},
            },
        )
        assert response.status_code == 200
        assert response.json()["content"] == "This is a test document"

    def test_search_documents(self):
        """Test searching documents"""
        # Create index
        index_resp = client.post("/api/v1/infra/indices", params={"name": "search"})
        index_id = index_resp.json()["index_id"]

        # Index documents
        client.post(
            f"/api/v1/infra/indices/{index_id}/documents",
            params={"content": "Python programming language"},
        )
        client.post(
            f"/api/v1/infra/indices/{index_id}/documents",
            params={"content": "Java programming language"},
        )

        # Search
        response = client.post(
            f"/api/v1/infra/indices/{index_id}/search",
            params={"query": "Python"},
        )
        assert response.status_code == 200
        assert response.json()["total"] == 1


class TestInquiryService:
    """Inquiry service tests"""

    def test_health_check(self):
        """Test inquiry service health"""
        response = client.get("/api/v1/inquiries/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_create_inquiry(self):
        """Test creating an inquiry"""
        response = client.post(
            "/api/v1/inquiries/",
            json={
                "title": "Cannot login",
                "description": "I'm unable to login to my account",
                "customer_id": "customer123",
                "priority": "high",
            },
        )
        assert response.status_code == 200
        assert response.json()["title"] == "Cannot login"

    def test_list_inquiries(self):
        """Test listing inquiries"""
        client.post(
            "/api/v1/inquiries/",
            json={
                "title": "Issue 1",
                "description": "Test",
                "customer_id": "cust1",
            },
        )
        client.post(
            "/api/v1/inquiries/",
            json={
                "title": "Issue 2",
                "description": "Test",
                "customer_id": "cust2",
            },
        )

        response = client.get("/api/v1/inquiries/")
        assert response.status_code == 200
        assert response.json()["total"] >= 2

    def test_add_response(self):
        """Test adding response to inquiry"""
        # Create inquiry
        inq_resp = client.post(
            "/api/v1/inquiries/",
            json={
                "title": "Test",
                "description": "Test inquiry",
                "customer_id": "test_cust",
            },
        )
        inquiry_id = inq_resp.json()["inquiry_id"]

        # Add response
        response = client.post(
            f"/api/v1/inquiries/{inquiry_id}/responses",
            params={
                "content": "We're looking into this",
                "responder_id": "support_team",
            },
        )
        assert response.status_code == 200
        assert response.json()["content"] == "We're looking into this"


class TestDocumentService:
    """Document service tests"""

    def test_health_check(self):
        """Test document service health"""
        response = client.get("/api/v1/documents/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_upload_document(self):
        """Test uploading a document"""
        response = client.post(
            "/api/v1/documents/upload",
            params={
                "filename": "report.pdf",
                "doc_type": "pdf",
                "file_size": 1024000,
                "upload_by": "user123",
                "tags": ["report", "2024"],
            },
        )
        assert response.status_code == 200
        assert response.json()["filename"] == "report.pdf"

    def test_list_documents(self):
        """Test listing documents"""
        client.post(
            "/api/v1/documents/upload",
            params={
                "filename": "doc1.pdf",
                "doc_type": "pdf",
                "file_size": 1024,
                "upload_by": "user1",
            },
        )
        client.post(
            "/api/v1/documents/upload",
            params={
                "filename": "doc2.txt",
                "doc_type": "text",
                "file_size": 512,
                "upload_by": "user2",
            },
        )

        response = client.get("/api/v1/documents/")
        assert response.status_code == 200
        assert response.json()["total"] >= 2

    def test_document_versioning(self):
        """Test document versioning"""
        # Upload document
        doc_resp = client.post(
            "/api/v1/documents/upload",
            params={
                "filename": "document.txt",
                "doc_type": "text",
                "file_size": 1024,
                "upload_by": "user123",
            },
        )
        doc_id = doc_resp.json()["doc_id"]

        # Create new version
        response = client.post(
            f"/api/v1/documents/{doc_id}/versions",
            params={
                "new_filename": "document_v2.txt",
                "new_file_size": 2048,
                "created_by": "user123",
                "change_description": "Updated content",
            },
        )
        assert response.status_code == 200
        assert response.json()["version_number"] == 2

        # Get versions
        versions_resp = client.get(f"/api/v1/documents/{doc_id}/versions")
        assert len(versions_resp.json()) == 2

    def test_document_preview(self):
        """Test getting document preview"""
        doc_resp = client.post(
            "/api/v1/documents/upload",
            params={
                "filename": "presentation.pdf",
                "doc_type": "pdf",
                "file_size": 5242880,  # 5MB
                "upload_by": "user123",
            },
        )
        doc_id = doc_resp.json()["doc_id"]

        response = client.get(f"/api/v1/documents/{doc_id}/preview")
        assert response.status_code == 200
        preview = response.json()
        assert preview["doc_id"] == doc_id
        assert preview["page_count"] is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
