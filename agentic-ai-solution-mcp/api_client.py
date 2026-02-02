"""API Client for Payment and Transaction Inquiry Services"""
import json
from typing import Any, Optional

import httpx


class APIClient:
    """Client for interacting with Payment Inquiry API services"""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.client = httpx.Client(base_url=base_url, timeout=30.0)

    def close(self):
        """Close the client"""
        self.client.close()

    # ============== Health & Stats ==============
    
    def health_check(self) -> dict:
        """Check overall health"""
        response = self.client.get("/health")
        response.raise_for_status()
        return response.json()

    def inquiry_health(self) -> dict:
        """Check inquiry service health"""
        response = self.client.get("/api/v1/inquiry/health")
        response.raise_for_status()
        return response.json()

    def get_stats(self) -> dict:
        """Get payment and transaction statistics"""
        response = self.client.get("/api/v1/inquiry/stats")
        response.raise_for_status()
        return response.json()

    # ============== Payment Methods ==============

    def list_payments(self, limit: int = 10, offset: int = 0) -> dict:
        """List all payments with pagination"""
        response = self.client.get(
            "/api/v1/inquiry/payments",
            params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    def search_payments(
        self,
        pmt_id: Optional[str] = None,
        msg_id: Optional[str] = None,
        iban: Optional[str] = None,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        product: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict:
        """Search payments with filters"""
        params = {"limit": limit, "offset": offset}
        if pmt_id:
            params["pmt_id"] = pmt_id
        if msg_id:
            params["msg_id"] = msg_id
        if iban:
            params["iban"] = iban
        if status:
            params["status"] = status
        if channel:
            params["channel"] = channel
        if product:
            params["product"] = product
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        
        response = self.client.get("/api/v1/inquiry/payments/search", params=params)
        response.raise_for_status()
        return response.json()

    def get_payment(self, pmt_id: str) -> dict:
        """Get payment by payment ID"""
        response = self.client.get(f"/api/v1/inquiry/payments/{pmt_id}")
        response.raise_for_status()
        return response.json()

    def get_payment_full(self, pmt_id: str) -> dict:
        """Get payment with all associated transactions"""
        response = self.client.get(f"/api/v1/inquiry/payments/{pmt_id}/full")
        response.raise_for_status()
        return response.json()

    def get_payment_by_message(self, msg_id: str) -> dict:
        """Get payment by message ID"""
        response = self.client.get(f"/api/v1/inquiry/payments/by-message/{msg_id}")
        response.raise_for_status()
        return response.json()

    # ============== Transaction Methods ==============

    def list_transactions(self, limit: int = 10, offset: int = 0) -> dict:
        """List all transactions with pagination"""
        response = self.client.get(
            "/api/v1/inquiry/transactions",
            params={"limit": limit, "offset": offset}
        )
        response.raise_for_status()
        return response.json()

    def search_transactions(
        self,
        tx_id: Optional[str] = None,
        pmt_id: Optional[str] = None,
        end_to_end_id: Optional[str] = None,
        iban: Optional[str] = None,
        status: Optional[str] = None,
        channel: Optional[str] = None,
        product: Optional[str] = None,
        amount_min: Optional[float] = None,
        amount_max: Optional[float] = None,
        currency: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> dict:
        """Search transactions with filters"""
        params = {"limit": limit, "offset": offset}
        if tx_id:
            params["tx_id"] = tx_id
        if pmt_id:
            params["pmt_id"] = pmt_id
        if end_to_end_id:
            params["end_to_end_id"] = end_to_end_id
        if iban:
            params["iban"] = iban
        if status:
            params["status"] = status
        if channel:
            params["channel"] = channel
        if product:
            params["product"] = product
        if amount_min is not None:
            params["amount_min"] = amount_min
        if amount_max is not None:
            params["amount_max"] = amount_max
        if currency:
            params["currency"] = currency
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        
        response = self.client.get("/api/v1/inquiry/transactions/search", params=params)
        response.raise_for_status()
        return response.json()

    def get_transaction(self, tx_id: str) -> dict:
        """Get transaction by transaction ID"""
        response = self.client.get(f"/api/v1/inquiry/transactions/{tx_id}")
        response.raise_for_status()
        return response.json()

    def get_transactions_by_payment(self, pmt_id: str) -> dict:
        """Get all transactions for a payment ID"""
        response = self.client.get(f"/api/v1/inquiry/transactions/by-payment/{pmt_id}")
        response.raise_for_status()
        return response.json()

    def get_transaction_by_e2e(self, e2e_id: str) -> dict:
        """Get transaction by end-to-end ID"""
        response = self.client.get(f"/api/v1/inquiry/transactions/by-e2e/{e2e_id}")
        response.raise_for_status()
        return response.json()


# Singleton instance
_client: Optional[APIClient] = None


def get_client(base_url: str = "http://localhost:8001") -> APIClient:
    """Get or create API client singleton"""
    global _client
    if _client is None:
        _client = APIClient(base_url=base_url)
    return _client
