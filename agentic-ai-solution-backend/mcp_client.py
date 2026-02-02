"""MCP Client for Payment Inquiry using REST API

This client communicates with the MCP Server (payment-inquiry-mcp) which
in turn communicates with the Mock Payment API.

Architecture:
  Backend → MCP Client (REST) → MCP Server (FastMCP + REST) → Mock API

The MCP server exposes both MCP protocol (/mcp) and REST endpoints (/api).
This client uses the REST endpoints for simpler integration.
"""

import httpx
from typing import Any, Optional
import logging

from config import Config

logger = logging.getLogger(__name__)


class MCPPaymentClient:
    """MCP Client that connects to the Payment Inquiry MCP Server via REST API
    
    Uses simple HTTP/REST calls to access MCP server tools.
    The MCP server exposes REST endpoints alongside the MCP protocol.
    """
    
    def __init__(self, mcp_server_url: str = None):
        """Initialize MCP client
        
        Args:
            mcp_server_url: Base URL of the MCP server (default from config)
        """
        self.base_url = mcp_server_url or Config.MCP_SERVER_URL
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=30.0)
        self._connected = False
        self._tools_cache = [
            "health_check", "get_inquiry_stats", "list_payments", 
            "search_payments", "get_payment", "get_payment_with_transactions",
            "get_payment_by_message_id", "list_transactions", "get_transaction",
            "search_transactions", "get_transactions_by_payment", 
            "get_transaction_by_end_to_end_id"
        ]
        logger.info(f"MCPPaymentClient initialized with server URL: {self.base_url}")
    
    async def connect(self) -> bool:
        """Verify connection to the MCP server by calling health endpoint"""
        try:
            result = await self.health_check()
            if "error" not in result:
                self._connected = True
                logger.info(f"Connected to MCP server. Status: {result.get('status', 'unknown')}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            return False
    
    async def close(self):
        """Close the HTTP client"""
        try:
            await self._client.aclose()
            self._connected = False
            logger.info("MCP client closed")
        except Exception as e:
            logger.error(f"Error closing MCP client: {e}")
    
    def is_connected(self) -> bool:
        """Check if connected to MCP server"""
        return self._connected
    
    def get_available_tools(self) -> list[str]:
        """Get list of available MCP tools"""
        return self._tools_cache.copy()
    
    async def _get(self, path: str, params: dict = None) -> dict[str, Any]:
        """Make GET request to MCP server"""
        try:
            logger.debug(f"Making GET request to {self.base_url}{path}")
            response = await self._client.get(path, params=params)
            response.raise_for_status()
            result = response.json()
            logger.debug(f"GET {path} response: {result}")
            return result
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error on GET {path}: {e.response.status_code} - {e.response.text}")
            return {"error": f"HTTP error: {e.response.status_code}", "detail": e.response.text}
        except httpx.ConnectError as e:
            logger.error(f"Connection error on GET {path}: {e}")
            return {"error": f"Connection error: {e}"}
        except Exception as e:
            logger.error(f"Unexpected error on GET {path}: {type(e).__name__}: {e}")
            return {"error": str(e)}
    
    async def _post(self, path: str, data: dict = None) -> dict[str, Any]:
        """Make POST request to MCP server"""
        try:
            response = await self._client.post(path, json=data or {})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}", "detail": e.response.text}
        except Exception as e:
            return {"error": str(e)}

    # ============== Health & Stats ==============
    
    async def health_check(self) -> dict[str, Any]:
        """Check MCP server and API health"""
        return await self._get("/api/health")
    
    async def get_stats(self) -> dict[str, Any]:
        """Get payment and transaction statistics"""
        return await self._get("/api/stats")
    
    # ============== Payment Methods ==============
    
    async def list_payments(self, limit: int = 10, offset: int = 0) -> dict[str, Any]:
        """List all payments with pagination"""
        return await self._get("/api/payments", {"limit": limit, "offset": offset})
    
    async def search_payments(
        self,
        payment_id: str = None,
        debtor_iban: str = None,
        creditor_iban: str = None,
        status: str = None,
        channel: str = None,
        product: str = None,
        limit: int = 10
    ) -> dict[str, Any]:
        """Search payments by various criteria"""
        data = {"limit": limit}
        if payment_id:
            data["payment_id"] = payment_id
        if debtor_iban:
            data["debtor_iban"] = debtor_iban
        if creditor_iban:
            data["creditor_iban"] = creditor_iban
        if status:
            data["status"] = status
        if channel:
            data["channel"] = channel
        if product:
            data["product"] = product
        return await self._post("/api/payments/search", data)
    
    async def get_payment(self, payment_id: str) -> dict[str, Any]:
        """Get a specific payment by ID"""
        return await self._get(f"/api/payments/{payment_id}")
    
    async def get_payment_with_transactions(self, payment_id: str) -> dict[str, Any]:
        """Get payment with all its transactions"""
        return await self._get(f"/api/payments/{payment_id}/full")
    
    async def get_payment_by_message_id(self, message_id: str) -> dict[str, Any]:
        """Get payment by message ID"""
        return await self._get(f"/api/payments/by-message/{message_id}")
    
    # ============== Transaction Methods ==============
    
    async def list_transactions(self, limit: int = 10, offset: int = 0) -> dict[str, Any]:
        """List all transactions with pagination"""
        return await self._get("/api/transactions", {"limit": limit, "offset": offset})
    
    async def get_transaction(self, transaction_id: str) -> dict[str, Any]:
        """Get a specific transaction by ID"""
        return await self._get(f"/api/transactions/{transaction_id}")
    
    async def search_transactions(
        self,
        transaction_id: str = None,
        payment_id: str = None,
        status: str = None,
        min_amount: float = None,
        max_amount: float = None,
        currency: str = None,
        limit: int = 10
    ) -> dict[str, Any]:
        """Search transactions by various criteria"""
        data = {"limit": limit}
        if transaction_id:
            data["transaction_id"] = transaction_id
        if payment_id:
            data["payment_id"] = payment_id
        if status:
            data["status"] = status
        if min_amount is not None:
            data["min_amount"] = min_amount
        if max_amount is not None:
            data["max_amount"] = max_amount
        if currency:
            data["currency"] = currency
        return await self._post("/api/transactions/search", data)
    
    async def get_transactions_by_payment(self, payment_id: str) -> dict[str, Any]:
        """Get all transactions for a payment"""
        return await self._get(f"/api/transactions/by-payment/{payment_id}")
    
    async def get_transaction_by_e2e_id(self, e2e_id: str) -> dict[str, Any]:
        """Get transaction by end-to-end ID"""
        return await self._get(f"/api/transactions/by-e2e/{e2e_id}")
