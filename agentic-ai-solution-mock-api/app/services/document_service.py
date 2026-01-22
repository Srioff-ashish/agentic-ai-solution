"""Mock Document Service"""
import uuid
from datetime import datetime
from typing import Dict, Optional

from app.models import (
    Document,
    DocumentType,
    DocumentVersion,
    DocumentPreview,
)


class DocumentService:
    """Mock document management service"""

    def __init__(self):
        self.documents: Dict[str, Document] = {}
        self.versions: Dict[str, list[DocumentVersion]] = {}
        self._populate_mock_data()

    def _populate_mock_data(self):
        """Populate with mock documents"""
        mock_docs = [
            {
                "filename": "Product_Specifications.pdf",
                "doc_type": DocumentType.PDF,
                "file_size": 2048000,
                "upload_by": "admin@company.com",
                "metadata": {"department": "Product", "version": "1.0"},
                "tags": ["specifications", "product", "technical"],
            },
            {
                "filename": "Q4_2024_Financial_Report.xlsx",
                "doc_type": DocumentType.SPREADSHEET,
                "file_size": 512000,
                "upload_by": "finance@company.com",
                "metadata": {"department": "Finance", "quarter": "Q4", "year": 2024},
                "tags": ["financial", "report", "confidential"],
            },
            {
                "filename": "User_Guide.pdf",
                "doc_type": DocumentType.PDF,
                "file_size": 3145728,
                "upload_by": "documentation@company.com",
                "metadata": {"department": "Documentation", "version": "2.1"},
                "tags": ["guide", "user", "documentation"],
            },
            {
                "filename": "Marketing_Campaign_Presentation.pptx",
                "doc_type": DocumentType.PRESENTATION,
                "file_size": 5242880,
                "upload_by": "marketing@company.com",
                "metadata": {"department": "Marketing", "campaign": "2025_Spring"},
                "tags": ["marketing", "campaign", "presentation"],
            },
            {
                "filename": "API_Documentation.md",
                "doc_type": DocumentType.TEXT,
                "file_size": 256000,
                "upload_by": "dev@company.com",
                "metadata": {"department": "Development", "api_version": "2.0"},
                "tags": ["api", "documentation", "development"],
            },
            {
                "filename": "Company_Logo.png",
                "doc_type": DocumentType.IMAGE,
                "file_size": 1024000,
                "upload_by": "branding@company.com",
                "metadata": {"department": "Branding", "format": "PNG"},
                "tags": ["logo", "branding", "image"],
            },
            {
                "filename": "Database_Backup_2024.tar.gz",
                "doc_type": DocumentType.ARCHIVE,
                "file_size": 1073741824,  # 1GB
                "upload_by": "devops@company.com",
                "metadata": {"department": "DevOps", "date": "2024-12-31"},
                "tags": ["backup", "database", "archive"],
            },
        ]

        for doc_data in mock_docs:
            doc_id = str(uuid.uuid4())
            document = Document(
                doc_id=doc_id,
                filename=doc_data["filename"],
                doc_type=doc_data["doc_type"],
                file_size=doc_data["file_size"],
                upload_by=doc_data["upload_by"],
                metadata=doc_data["metadata"],
                tags=doc_data["tags"],
                version=1,
            )
            self.documents[doc_id] = document

            # Initialize version tracking
            version = DocumentVersion(
                version_id=str(uuid.uuid4()),
                doc_id=doc_id,
                version_number=1,
                filename=doc_data["filename"],
                file_size=doc_data["file_size"],
                created_by=doc_data["upload_by"],
                change_description="Initial upload",
            )
            self.versions[doc_id] = [version]

    def upload_document(
        self,
        filename: str,
        doc_type: DocumentType,
        file_size: int,
        upload_by: str,
        metadata: Optional[dict] = None,
        tags: Optional[list[str]] = None,
    ) -> Document:
        """Upload a new document"""
        doc_id = str(uuid.uuid4())
        document = Document(
            doc_id=doc_id,
            filename=filename,
            doc_type=doc_type,
            file_size=file_size,
            upload_by=upload_by,
            metadata=metadata or {},
            tags=tags or [],
            version=1,
        )
        self.documents[doc_id] = document
        
        # Initialize version tracking
        version = DocumentVersion(
            version_id=str(uuid.uuid4()),
            doc_id=doc_id,
            version_number=1,
            filename=filename,
            file_size=file_size,
            created_by=upload_by,
            change_description="Initial upload",
        )
        self.versions[doc_id] = [version]
        
        return document

    def get_document(self, doc_id: str) -> Optional[Document]:
        """Get document metadata"""
        return self.documents.get(doc_id)

    def list_documents(
        self,
        doc_type: Optional[DocumentType] = None,
        upload_by: Optional[str] = None,
        tags: Optional[list[str]] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Document], int]:
        """List documents with filters"""
        filtered = []

        for document in self.documents.values():
            if not document.is_active:
                continue
            if doc_type and document.doc_type != doc_type:
                continue
            if upload_by and document.upload_by != upload_by:
                continue
            if tags:
                # Check if any of the requested tags match
                if not any(tag in document.tags for tag in tags):
                    continue

            filtered.append(document)

        # Sort by created_at descending
        filtered.sort(key=lambda x: x.created_at, reverse=True)

        total = len(filtered)
        paginated = filtered[skip : skip + limit]

        return paginated, total

    def update_document(
        self,
        doc_id: str,
        filename: Optional[str] = None,
        metadata: Optional[dict] = None,
        tags: Optional[list[str]] = None,
    ) -> Optional[Document]:
        """Update document metadata"""
        document = self.documents.get(doc_id)
        if not document:
            return None

        if filename is not None:
            document.filename = filename
        if metadata is not None:
            document.metadata.update(metadata)
        if tags is not None:
            document.tags = tags

        document.updated_at = datetime.utcnow()
        return document

    def delete_document(self, doc_id: str) -> bool:
        """Soft delete document"""
        document = self.documents.get(doc_id)
        if not document:
            return False

        document.is_active = False
        document.updated_at = datetime.utcnow()
        return True

    def create_version(
        self,
        doc_id: str,
        new_filename: str,
        new_file_size: int,
        created_by: str,
        change_description: Optional[str] = None,
    ) -> Optional[DocumentVersion]:
        """Create a new version of document"""
        document = self.documents.get(doc_id)
        if not document:
            return None

        # Get current versions
        doc_versions = self.versions.get(doc_id, [])
        new_version_number = len(doc_versions) + 1

        version = DocumentVersion(
            version_id=str(uuid.uuid4()),
            doc_id=doc_id,
            version_number=new_version_number,
            filename=new_filename,
            file_size=new_file_size,
            created_by=created_by,
            change_description=change_description,
        )

        if doc_id not in self.versions:
            self.versions[doc_id] = []

        self.versions[doc_id].append(version)

        # Update document
        document.version = new_version_number
        document.filename = new_filename
        document.file_size = new_file_size
        document.updated_at = datetime.utcnow()

        return version

    def get_versions(self, doc_id: str) -> Optional[list[DocumentVersion]]:
        """Get all versions of document"""
        if doc_id not in self.documents:
            return None
        return self.versions.get(doc_id, [])

    def get_version(self, doc_id: str, version_number: int) -> Optional[DocumentVersion]:
        """Get specific version of document"""
        versions = self.get_versions(doc_id)
        if not versions:
            return None
        
        for version in versions:
            if version.version_number == version_number:
                return version
        return None

    def get_preview(self, doc_id: str) -> Optional[DocumentPreview]:
        """Get document preview"""
        document = self.documents.get(doc_id)
        if not document:
            return None

        # Generate mock preview based on document type
        content_preview = self._generate_preview(document)

        preview = DocumentPreview(
            doc_id=doc_id,
            filename=document.filename,
            content_preview=content_preview,
            page_count=self._estimate_pages(document),
            thumbnail_url=f"/api/v1/documents/{doc_id}/thumbnail",
        )

        return preview

    @staticmethod
    def _generate_preview(document: Document) -> str:
        """Generate preview based on document type"""
        previews = {
            DocumentType.PDF: "PDF Document - [Preview of PDF content]",
            DocumentType.TEXT: "Text content preview...",
            DocumentType.IMAGE: "Image - [Image data]",
            DocumentType.SPREADSHEET: "Spreadsheet - [Table data]",
            DocumentType.PRESENTATION: "Presentation - [Slide content]",
            DocumentType.ARCHIVE: "Archive File - [Compressed contents]",
        }
        return previews.get(document.doc_type, "Document preview")

    @staticmethod
    def _estimate_pages(document: Document) -> Optional[int]:
        """Estimate page count based on file size and type"""
        if document.doc_type in [DocumentType.PDF, DocumentType.PRESENTATION]:
            # Rough estimation: average 100KB per page
            return max(1, document.file_size // 102400)
        return None


# Global service instance
document_service = DocumentService()
