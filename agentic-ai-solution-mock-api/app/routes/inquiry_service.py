"""Inquiry Service Routes"""
from typing import Optional

from fastapi import APIRouter, HTTPException

from app.models import (
    Inquiry,
    InquiryStatus,
    InquiryPriority,
    InquiryResponse,
    CreateInquiryRequest,
)
from app.services.inquiry_service import inquiry_service

router = APIRouter()


@router.get("/health")
async def health_check():
    """Check inquiry service health"""
    return {
        "status": "healthy",
        "service": "inquiries",
        "inquiries_count": len(inquiry_service.inquiries),
    }


@router.post("/", response_model=Inquiry)
async def create_inquiry(request: CreateInquiryRequest):
    """Create a new inquiry"""
    inquiry = inquiry_service.create_inquiry(request)
    return inquiry


@router.get("/", response_model=dict)
async def list_inquiries(
    status: Optional[InquiryStatus] = None,
    priority: Optional[InquiryPriority] = None,
    customer_id: Optional[str] = None,
    assigned_to: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
):
    """List inquiries with filters"""
    inquiries, total = inquiry_service.list_inquiries(
        status=status,
        priority=priority,
        customer_id=customer_id,
        assigned_to=assigned_to,
        skip=skip,
        limit=limit,
    )
    return {
        "total": total,
        "count": len(inquiries),
        "skip": skip,
        "limit": limit,
        "inquiries": inquiries,
    }


@router.get("/{inquiry_id}", response_model=Inquiry)
async def get_inquiry(inquiry_id: str):
    """Get inquiry details"""
    inquiry = inquiry_service.get_inquiry(inquiry_id)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry


@router.put("/{inquiry_id}", response_model=Inquiry)
async def update_inquiry(
    inquiry_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[InquiryPriority] = None,
    assigned_to: Optional[str] = None,
    tags: Optional[list[str]] = None,
):
    """Update inquiry"""
    inquiry = inquiry_service.update_inquiry(
        inquiry_id,
        title=title,
        description=description,
        priority=priority,
        assigned_to=assigned_to,
        tags=tags,
    )
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry


@router.put("/{inquiry_id}/status", response_model=Inquiry)
async def update_status(
    inquiry_id: str,
    status: InquiryStatus,
):
    """Update inquiry status"""
    inquiry = inquiry_service.update_status(inquiry_id, status)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return inquiry


@router.post("/{inquiry_id}/responses", response_model=InquiryResponse)
async def add_response(
    inquiry_id: str,
    content: str,
    responder_id: str,
    is_internal: bool = False,
):
    """Add response to inquiry"""
    response = inquiry_service.add_response(
        inquiry_id,
        content=content,
        responder_id=responder_id,
        is_internal=is_internal,
    )
    if not response:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return response


@router.get("/{inquiry_id}/responses", response_model=list[InquiryResponse])
async def get_responses(inquiry_id: str):
    """Get responses for inquiry"""
    responses = inquiry_service.get_responses(inquiry_id)
    if responses is None:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return responses


@router.delete("/{inquiry_id}")
async def delete_inquiry(inquiry_id: str):
    """Delete inquiry"""
    if not inquiry_service.delete_inquiry(inquiry_id):
        raise HTTPException(status_code=404, detail="Inquiry not found")
    return {"message": "Inquiry deleted successfully"}


@router.get("/search", response_model=dict)
async def search_inquiries(
    query: str,
    skip: int = 0,
    limit: int = 20,
):
    """Search inquiries by title and description"""
    query_lower = query.lower()
    results = []

    for inquiry in inquiry_service.inquiries.values():
        if (
            query_lower in inquiry.title.lower()
            or query_lower in inquiry.description.lower()
        ):
            results.append(inquiry)

    # Sort by created_at descending
    results.sort(key=lambda x: x.created_at, reverse=True)

    total = len(results)
    paginated = results[skip : skip + limit]

    return {
        "query": query,
        "total": total,
        "count": len(paginated),
        "skip": skip,
        "limit": limit,
        "results": paginated,
    }
