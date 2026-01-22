"""Data models for mock services"""
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class IndexStatus(str, Enum):
    """Search index status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    CREATING = "creating"
    DELETING = "deleting"


class SearchIndex(BaseModel):
    """Search index model"""
    index_id: str = Field(..., description="Unique index identifier")
    name: str = Field(..., description="Index name")
    status: IndexStatus = Field(default=IndexStatus.ACTIVE, description="Index status")
    document_count: int = Field(default=0, description="Number of indexed documents")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    settings: dict = Field(default_factory=dict, description="Index settings")


class IndexedDocument(BaseModel):
    """Document in search index"""
    doc_id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    metadata: dict = Field(default_factory=dict, description="Document metadata")
    indexed_at: datetime = Field(default_factory=datetime.utcnow, description="Indexing timestamp")


class SearchQuery(BaseModel):
    """Search query model"""
    query: str = Field(..., description="Search query text")
    limit: int = Field(default=10, description="Max results", ge=1, le=100)
    offset: int = Field(default=0, description="Result offset", ge=0)
    filters: Optional[dict] = Field(default=None, description="Additional filters")


class SearchResult(BaseModel):
    """Search result model"""
    doc_id: str = Field(..., description="Document ID")
    content: str = Field(..., description="Document content")
    score: float = Field(..., description="Relevance score")
    metadata: dict = Field(default_factory=dict, description="Document metadata")


class InquiryStatus(str, Enum):
    """Inquiry status"""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class InquiryPriority(str, Enum):
    """Inquiry priority"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Inquiry(BaseModel):
    """Inquiry model"""
    inquiry_id: str = Field(..., description="Unique inquiry identifier")
    title: str = Field(..., description="Inquiry title")
    description: str = Field(..., description="Detailed description")
    status: InquiryStatus = Field(default=InquiryStatus.OPEN, description="Inquiry status")
    priority: InquiryPriority = Field(default=InquiryPriority.MEDIUM, description="Priority level")
    customer_id: str = Field(..., description="Customer/User ID")
    assigned_to: Optional[str] = Field(default=None, description="Assigned staff member")
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    resolved_at: Optional[datetime] = Field(default=None, description="Resolution timestamp")


class InquiryResponse(BaseModel):
    """Response to inquiry"""
    response_id: str = Field(..., description="Unique response identifier")
    inquiry_id: str = Field(..., description="Parent inquiry ID")
    content: str = Field(..., description="Response content")
    responder_id: str = Field(..., description="ID of person giving response")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    is_internal: bool = Field(default=False, description="Whether response is internal")


class CreateInquiryRequest(BaseModel):
    """Request to create inquiry"""
    title: str = Field(..., description="Inquiry title")
    description: str = Field(..., description="Detailed description")
    customer_id: str = Field(..., description="Customer/User ID")
    priority: InquiryPriority = Field(default=InquiryPriority.MEDIUM, description="Priority level")
    tags: list[str] = Field(default_factory=list, description="Tags")


class DocumentType(str, Enum):
    """Document type"""
    PDF = "pdf"
    TEXT = "text"
    IMAGE = "image"
    SPREADSHEET = "spreadsheet"
    PRESENTATION = "presentation"
    ARCHIVE = "archive"


class Document(BaseModel):
    """Document model"""
    doc_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    doc_type: DocumentType = Field(..., description="Document type")
    file_size: int = Field(..., description="File size in bytes")
    upload_by: str = Field(..., description="User ID who uploaded")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    tags: list[str] = Field(default_factory=list, description="Document tags")
    metadata: dict = Field(default_factory=dict, description="Custom metadata")
    version: int = Field(default=1, description="Document version number")
    is_active: bool = Field(default=True, description="Whether document is active")


class DocumentVersion(BaseModel):
    """Document version"""
    version_id: str = Field(..., description="Version identifier")
    doc_id: str = Field(..., description="Document ID")
    version_number: int = Field(..., description="Version number")
    filename: str = Field(..., description="Filename for this version")
    file_size: int = Field(..., description="File size in bytes")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    created_by: str = Field(..., description="User who created version")
    change_description: Optional[str] = Field(default=None, description="Changes in this version")


class DocumentPreview(BaseModel):
    """Document preview"""
    doc_id: str = Field(..., description="Document ID")
    filename: str = Field(..., description="Filename")
    content_preview: str = Field(..., description="Preview of document content")
    page_count: Optional[int] = Field(default=None, description="Number of pages")
    thumbnail_url: Optional[str] = Field(default=None, description="Thumbnail URL")
