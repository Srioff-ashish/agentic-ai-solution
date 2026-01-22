"""Mock Inquiry Service"""
import uuid
from datetime import datetime
from typing import Dict, Optional

from app.models import (
    Inquiry,
    InquiryStatus,
    InquiryPriority,
    InquiryResponse,
    CreateInquiryRequest,
)


class InquiryService:
    """Mock inquiry management service"""

    def __init__(self):
        self.inquiries: Dict[str, Inquiry] = {}
        self.responses: Dict[str, list[InquiryResponse]] = {}
        self._populate_mock_data()

    def _populate_mock_data(self):
        """Populate with mock inquiry data"""
        mock_inquiries = [
            {
                "title": "Unable to login to account",
                "description": "I've been trying to log in for the past hour but keep getting an error message",
                "customer_id": "CUST001",
                "priority": InquiryPriority.HIGH,
                "status": InquiryStatus.IN_PROGRESS,
                "assigned_to": "support_agent_01",
                "tags": ["login", "account", "urgent"],
            },
            {
                "title": "Refund request for order #ORD001",
                "description": "The product arrived damaged. I would like to return it and get a full refund",
                "customer_id": "CUST002",
                "priority": InquiryPriority.HIGH,
                "status": InquiryStatus.OPEN,
                "assigned_to": None,
                "tags": ["refund", "damaged", "return"],
            },
            {
                "title": "Shipping address update needed",
                "description": "I need to update my shipping address for a pending order",
                "customer_id": "CUST003",
                "priority": InquiryPriority.MEDIUM,
                "status": InquiryStatus.OPEN,
                "assigned_to": None,
                "tags": ["shipping", "address"],
            },
            {
                "title": "Question about product features",
                "description": "Can you provide more details about the battery life of the product?",
                "customer_id": "CUST004",
                "priority": InquiryPriority.LOW,
                "status": InquiryStatus.RESOLVED,
                "assigned_to": "support_agent_02",
                "tags": ["product", "features", "info"],
            },
        ]

        for inq in mock_inquiries:
            inquiry_id = str(uuid.uuid4())
            inquiry = Inquiry(
                inquiry_id=inquiry_id,
                title=inq["title"],
                description=inq["description"],
                customer_id=inq["customer_id"],
                priority=inq["priority"],
                status=inq["status"],
                assigned_to=inq["assigned_to"],
                tags=inq["tags"],
            )
            self.inquiries[inquiry_id] = inquiry
            self.responses[inquiry_id] = []

        # Add sample responses to some inquiries
        for idx, inquiry_id in enumerate(list(self.inquiries.keys())[:2]):
            if idx == 0:
                response1 = InquiryResponse(
                    response_id=str(uuid.uuid4()),
                    inquiry_id=inquiry_id,
                    content="Thank you for reporting this issue. We're investigating the login error.",
                    responder_id="support_agent_01",
                    is_internal=False,
                )
                self.responses[inquiry_id].append(response1)
                
                response2 = InquiryResponse(
                    response_id=str(uuid.uuid4()),
                    inquiry_id=inquiry_id,
                    content="Issue identified: Server maintenance in progress. Should be resolved within 30 mins.",
                    responder_id="support_agent_01",
                    is_internal=True,
                )
                self.responses[inquiry_id].append(response2)

    def create_inquiry(self, request: CreateInquiryRequest) -> Inquiry:
        """Create a new inquiry"""
        inquiry_id = str(uuid.uuid4())
        inquiry = Inquiry(
            inquiry_id=inquiry_id,
            title=request.title,
            description=request.description,
            status=InquiryStatus.OPEN,
            priority=request.priority,
            customer_id=request.customer_id,
            tags=request.tags,
        )
        self.inquiries[inquiry_id] = inquiry
        self.responses[inquiry_id] = []
        return inquiry

    def get_inquiry(self, inquiry_id: str) -> Optional[Inquiry]:
        """Get inquiry details"""
        return self.inquiries.get(inquiry_id)

    def list_inquiries(
        self,
        status: Optional[InquiryStatus] = None,
        priority: Optional[InquiryPriority] = None,
        customer_id: Optional[str] = None,
        assigned_to: Optional[str] = None,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Inquiry], int]:
        """List inquiries with filters"""
        filtered = []

        for inquiry in self.inquiries.values():
            if status and inquiry.status != status:
                continue
            if priority and inquiry.priority != priority:
                continue
            if customer_id and inquiry.customer_id != customer_id:
                continue
            if assigned_to and inquiry.assigned_to != assigned_to:
                continue

            filtered.append(inquiry)

        # Sort by created_at descending
        filtered.sort(key=lambda x: x.created_at, reverse=True)

        total = len(filtered)
        paginated = filtered[skip : skip + limit]

        return paginated, total

    def update_inquiry(
        self,
        inquiry_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[InquiryPriority] = None,
        assigned_to: Optional[str] = None,
        tags: Optional[list[str]] = None,
    ) -> Optional[Inquiry]:
        """Update inquiry"""
        inquiry = self.inquiries.get(inquiry_id)
        if not inquiry:
            return None

        if title is not None:
            inquiry.title = title
        if description is not None:
            inquiry.description = description
        if priority is not None:
            inquiry.priority = priority
        if assigned_to is not None:
            inquiry.assigned_to = assigned_to
        if tags is not None:
            inquiry.tags = tags

        inquiry.updated_at = datetime.utcnow()
        return inquiry

    def update_status(
        self, inquiry_id: str, status: InquiryStatus
    ) -> Optional[Inquiry]:
        """Update inquiry status"""
        inquiry = self.inquiries.get(inquiry_id)
        if not inquiry:
            return None

        inquiry.status = status
        inquiry.updated_at = datetime.utcnow()

        if status == InquiryStatus.RESOLVED:
            inquiry.resolved_at = datetime.utcnow()

        return inquiry

    def add_response(
        self,
        inquiry_id: str,
        content: str,
        responder_id: str,
        is_internal: bool = False,
    ) -> Optional[InquiryResponse]:
        """Add response to inquiry"""
        if inquiry_id not in self.inquiries:
            return None

        response_id = str(uuid.uuid4())
        response = InquiryResponse(
            response_id=response_id,
            inquiry_id=inquiry_id,
            content=content,
            responder_id=responder_id,
            is_internal=is_internal,
        )

        self.responses[inquiry_id].append(response)

        # Update inquiry timestamp
        inquiry = self.inquiries[inquiry_id]
        inquiry.updated_at = datetime.utcnow()

        return response

    def get_responses(self, inquiry_id: str) -> Optional[list[InquiryResponse]]:
        """Get responses for inquiry"""
        if inquiry_id not in self.inquiries:
            return None
        return self.responses.get(inquiry_id, [])

    def delete_inquiry(self, inquiry_id: str) -> bool:
        """Delete inquiry"""
        if inquiry_id in self.inquiries:
            del self.inquiries[inquiry_id]
            if inquiry_id in self.responses:
                del self.responses[inquiry_id]
            return True
        return False


# Global service instance
inquiry_service = InquiryService()
