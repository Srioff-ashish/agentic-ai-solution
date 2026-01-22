"""Document Service Routes"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Body

from app.models import (
    Document,
    DocumentType,
    DocumentVersion,
    DocumentPreview,
)
from app.services.document_service import document_service

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check document service health"""
    return {
        "status": "healthy",
        "service": "documents",
        "documents_count": len(document_service.documents),
    }


@router.post("/upload", response_model=Document)
async def upload_document(
    filename: str,
    doc_type: DocumentType,
    file_size: int,
    upload_by: str,
    metadata: Optional[dict] = None,
    tags: Optional[list[str]] = None,
):
    """Upload a new document"""
    document = document_service.upload_document(
        filename=filename,
        doc_type=doc_type,
        file_size=file_size,
        upload_by=upload_by,
        metadata=metadata,
        tags=tags,
    )
    return document


@router.get("/", response_model=dict)
async def list_documents(
    doc_type: Optional[DocumentType] = None,
    upload_by: Optional[str] = None,
    tags: Optional[list[str]] = None,
    skip: int = 0,
    limit: int = 20,
):
    """List documents with filters"""
    documents, total = document_service.list_documents(
        doc_type=doc_type,
        upload_by=upload_by,
        tags=tags,
        skip=skip,
        limit=limit,
    )
    return {
        "total": total,
        "count": len(documents),
        "skip": skip,
        "limit": limit,
        "documents": documents,
    }


@router.get("/{doc_id}", response_model=Document)
async def get_document(doc_id: str):
    """Get document metadata"""
    document = document_service.get_document(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.put("/{doc_id}", response_model=Document)
async def update_document(
    doc_id: str,
    filename: Optional[str] = None,
    metadata: Optional[dict] = None,
    tags: Optional[list[str]] = None,
):
    """Update document metadata"""
    document = document_service.update_document(
        doc_id,
        filename=filename,
        metadata=metadata,
        tags=tags,
    )
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{doc_id}")
async def delete_document(doc_id: str):
    """Delete document"""
    if not document_service.delete_document(doc_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.post("/{doc_id}/versions", response_model=DocumentVersion)
async def create_version(
    doc_id: str,
    new_filename: str,
    new_file_size: int,
    created_by: str,
    change_description: Optional[str] = None,
):
    """Create new version of document"""
    version = document_service.create_version(
        doc_id,
        new_filename=new_filename,
        new_file_size=new_file_size,
        created_by=created_by,
        change_description=change_description,
    )
    if not version:
        raise HTTPException(status_code=404, detail="Document not found")
    return version


@router.get("/{doc_id}/versions", response_model=list[DocumentVersion])
async def get_versions(doc_id: str):
    """Get all versions of document"""
    versions = document_service.get_versions(doc_id)
    if versions is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return versions


@router.get("/{doc_id}/versions/{version_number}", response_model=DocumentVersion)
async def get_version(doc_id: str, version_number: int):
    """Get specific version of document"""
    version = document_service.get_version(doc_id, version_number)
    if not version:
        raise HTTPException(status_code=404, detail="Document version not found")
    return version


@router.get("/{doc_id}/preview", response_model=DocumentPreview)
async def get_preview(doc_id: str):
    """Get document preview"""
    preview = document_service.get_preview(doc_id)
    if not preview:
        raise HTTPException(status_code=404, detail="Document not found")
    return preview


@router.post("/bulk-upload")
async def bulk_upload(
    documents: list[dict] = Body(...),
):
    """Bulk upload multiple documents"""
    uploaded = []
    for doc in documents:
        filename = doc.get("filename", "unknown")
        doc_type = doc.get("doc_type", DocumentType.TEXT)
        file_size = doc.get("file_size", 1024)
        upload_by = doc.get("upload_by", "system")
        metadata = doc.get("metadata", {})
        tags = doc.get("tags", [])

        uploaded_doc = document_service.upload_document(
            filename=filename,
            doc_type=doc_type,
            file_size=file_size,
            upload_by=upload_by,
            metadata=metadata,
            tags=tags,
        )
        uploaded.append(uploaded_doc)

    return {
        "total": len(documents),
        "uploaded": len(uploaded),
        "documents": uploaded,
    }


@router.get("/{doc_id}/download")
async def download_document(doc_id: str):
    """Get document download info"""
    document = document_service.get_document(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "doc_id": doc_id,
        "filename": document.filename,
        "file_size": document.file_size,
        "doc_type": document.doc_type,
        "download_url": f"/api/v1/documents/{doc_id}/file",
        "expires_in": 3600,  # 1 hour
    }
