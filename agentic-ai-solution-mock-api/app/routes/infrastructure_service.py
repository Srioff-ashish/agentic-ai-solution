"""Infrastructure Service Routes"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Body

from app.models import SearchIndex, SearchQuery, SearchResult
from app.services.infrastructure_service import infra_service

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check infrastructure service health"""
    return {
        "status": "healthy",
        "service": "infrastructure",
        "indices_count": len(infra_service.indices),
    }


@router.post("/indices", response_model=SearchIndex)
async def create_index(
    name: str,
    settings: Optional[dict] = None,
):
    """Create a new search index"""
    index = infra_service.create_index(name, settings)
    return index


@router.get("/indices", response_model=list[SearchIndex])
async def list_indices():
    """List all search indices"""
    return infra_service.list_indices()


@router.get("/indices/{index_id}", response_model=SearchIndex)
async def get_index(index_id: str):
    """Get index details"""
    index = infra_service.get_index(index_id)
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")
    return index


@router.delete("/indices/{index_id}")
async def delete_index(index_id: str):
    """Delete a search index"""
    if not infra_service.delete_index(index_id):
        raise HTTPException(status_code=404, detail="Index not found")
    return {"message": "Index deleted successfully"}


@router.post("/indices/{index_id}/documents")
async def index_document(
    index_id: str,
    content: str,
    metadata: Optional[dict] = None,
):
    """Index a document in the search index"""
    document = infra_service.index_document(index_id, content, metadata)
    if not document:
        raise HTTPException(status_code=404, detail="Index not found")
    return document


@router.get("/indices/{index_id}/documents/{doc_id}")
async def get_document(index_id: str, doc_id: str):
    """Get document from index"""
    document = infra_service.get_document(index_id, doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/indices/{index_id}/documents/{doc_id}")
async def delete_document(index_id: str, doc_id: str):
    """Delete document from index"""
    if not infra_service.delete_document(index_id, doc_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted successfully"}


@router.post("/indices/{index_id}/search", response_model=dict)
async def search_documents(
    index_id: str,
    query: str,
    limit: int = 10,
    offset: int = 0,
    filters: Optional[dict] = None,
):
    """Search documents in index"""
    index = infra_service.get_index(index_id)
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")

    search_query = SearchQuery(
        query=query,
        limit=limit,
        offset=offset,
        filters=filters,
    )

    results, total = infra_service.search(index_id, search_query)

    return {
        "query": query,
        "total": total,
        "count": len(results),
        "offset": offset,
        "limit": limit,
        "results": results,
    }


@router.post("/indices/{index_id}/bulk")
async def bulk_index(
    index_id: str,
    documents: list[dict] = Body(...),
):
    """Bulk index multiple documents"""
    index = infra_service.get_index(index_id)
    if not index:
        raise HTTPException(status_code=404, detail="Index not found")

    indexed_docs = []
    for doc in documents:
        content = doc.get("content", "")
        metadata = doc.get("metadata", {})
        indexed_doc = infra_service.index_document(index_id, content, metadata)
        if indexed_doc:
            indexed_docs.append(indexed_doc)

    return {
        "total": len(documents),
        "indexed": len(indexed_docs),
        "documents": indexed_docs,
    }
