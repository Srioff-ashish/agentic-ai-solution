"""Inquiry Service Routes - Payment and Transaction Inquiry API"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from app.models import (
    PaymentSearchQuery,
    TransactionSearchQuery,
    PaymentSearchResult,
    TransactionSearchResult,
)
from app.services.inquiry_service import inquiry_service

router = APIRouter()


# ============== Health Check ==============

@router.get("/health")
async def health_check():
    """Check inquiry service health"""
    stats = inquiry_service.get_stats()
    return {
        "status": "healthy",
        "service": "payment-inquiry",
        "payments_count": stats["total_payments"],
        "transactions_count": stats["total_transactions"],
    }


@router.get("/stats")
async def get_stats():
    """Get payment and transaction statistics"""
    return inquiry_service.get_stats()


# ============== Payment Endpoints ==============

@router.get("/payments", response_model=PaymentSearchResult)
async def list_payments(
    limit: int = Query(default=10, ge=1, le=100, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset"),
):
    """List all payments with pagination"""
    return inquiry_service.list_all_payments(limit=limit, offset=offset)


@router.get("/payments/search", response_model=PaymentSearchResult)
async def search_payments(
    pmt_id: Optional[str] = Query(default=None, description="Payment ID"),
    msg_id: Optional[str] = Query(default=None, description="Message ID"),
    iban: Optional[str] = Query(default=None, description="Originator IBAN"),
    status: Optional[str] = Query(default=None, description="Payment status (RCVD, ACTC, ACSC, IAUT, RJCT)"),
    channel: Optional[str] = Query(default=None, description="Channel name"),
    product: Optional[str] = Query(default=None, description="Product name"),
    date_from: Optional[str] = Query(default=None, description="Start date filter (ISO format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (ISO format)"),
    limit: int = Query(default=10, ge=1, le=100, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset"),
):
    """Search payments with various filters"""
    query = PaymentSearchQuery(
        pmt_id=pmt_id,
        msg_id=msg_id,
        iban=iban,
        status=status,
        channel=channel,
        product=product,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return inquiry_service.search_payments(query)


@router.get("/payments/{pmt_id}")
async def get_payment(pmt_id: str):
    """Get payment by payment ID"""
    payment = inquiry_service.get_payment(pmt_id)
    if not payment:
        raise HTTPException(status_code=404, detail=f"Payment not found: {pmt_id}")
    return payment


@router.get("/payments/{pmt_id}/full")
async def get_payment_with_transactions(pmt_id: str):
    """Get payment along with all associated transactions"""
    result = inquiry_service.get_payment_with_transactions(pmt_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Payment not found: {pmt_id}")
    return result


@router.get("/payments/by-message/{msg_id}")
async def get_payment_by_message_id(msg_id: str):
    """Get payment by message ID"""
    payment = inquiry_service.get_payment_by_msg_id(msg_id)
    if not payment:
        raise HTTPException(status_code=404, detail=f"Payment not found for message: {msg_id}")
    return payment


# ============== Transaction Endpoints ==============

@router.get("/transactions", response_model=TransactionSearchResult)
async def list_transactions(
    limit: int = Query(default=10, ge=1, le=100, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset"),
):
    """List all transactions with pagination"""
    return inquiry_service.list_all_transactions(limit=limit, offset=offset)


@router.get("/transactions/search", response_model=TransactionSearchResult)
async def search_transactions(
    tx_id: Optional[str] = Query(default=None, description="Transaction ID"),
    pmt_id: Optional[str] = Query(default=None, description="Payment ID"),
    end_to_end_id: Optional[str] = Query(default=None, description="End-to-end ID"),
    iban: Optional[str] = Query(default=None, description="IBAN (originator or counterparty)"),
    status: Optional[str] = Query(default=None, description="Transaction status (ACTC, ACSC, RJCT)"),
    channel: Optional[str] = Query(default=None, description="Channel name"),
    product: Optional[str] = Query(default=None, description="Product name"),
    amount_min: Optional[float] = Query(default=None, description="Minimum amount"),
    amount_max: Optional[float] = Query(default=None, description="Maximum amount"),
    currency: Optional[str] = Query(default=None, description="Currency (e.g., EUR)"),
    date_from: Optional[str] = Query(default=None, description="Start date filter (ISO format)"),
    date_to: Optional[str] = Query(default=None, description="End date filter (ISO format)"),
    limit: int = Query(default=10, ge=1, le=100, description="Max results"),
    offset: int = Query(default=0, ge=0, description="Offset"),
):
    """Search transactions with various filters"""
    query = TransactionSearchQuery(
        tx_id=tx_id,
        pmt_id=pmt_id,
        end_to_end_id=end_to_end_id,
        iban=iban,
        status=status,
        channel=channel,
        product=product,
        amount_min=amount_min,
        amount_max=amount_max,
        currency=currency,
        date_from=date_from,
        date_to=date_to,
        limit=limit,
        offset=offset,
    )
    return inquiry_service.search_transactions(query)


@router.get("/transactions/{tx_id}")
async def get_transaction(tx_id: str):
    """Get transaction by transaction ID"""
    transaction = inquiry_service.get_transaction(tx_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction not found: {tx_id}")
    return transaction


@router.get("/transactions/by-payment/{pmt_id}")
async def get_transactions_by_payment(pmt_id: str):
    """Get all transactions for a payment ID"""
    transactions = inquiry_service.get_transaction_by_pmt_id(pmt_id)
    return {
        "pmt_id": pmt_id,
        "count": len(transactions),
        "transactions": transactions
    }


@router.get("/transactions/by-e2e/{e2e_id}")
async def get_transaction_by_end_to_end_id(e2e_id: str):
    """Get transaction by end-to-end ID"""
    transaction = inquiry_service.get_transaction_by_end_to_end_id(e2e_id)
    if not transaction:
        raise HTTPException(status_code=404, detail=f"Transaction not found for E2E ID: {e2e_id}")
    return transaction

