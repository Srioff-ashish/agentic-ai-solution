"""MCP Server for Payment and Transaction Inquiry using FastMCP"""
import json
import logging
import os
import httpx
from typing import Optional
from functools import wraps

from fastmcp import FastMCP

from api_client import get_client

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-server")

# Backend URL for log forwarding
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:9001")

def forward_log(level: str, message: str):
    """Forward log to backend aggregator"""
    try:
        httpx.post(
            f"{BACKEND_URL}/logs/external",
            params={"module": "mcp", "level": level, "message": message},
            timeout=1.0
        )
    except:
        pass  # Don't fail if backend is not available

def log_tool_call(func):
    """Decorator to log MCP tool calls"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        logger.info(f"═══════════════════════════════════════════════════════════════")
        logger.info(f"🔧 MCP TOOL CALLED: {tool_name}")
        logger.info(f"   Args: {kwargs}")
        forward_log("INFO", f"🔧 MCP TOOL CALLED: {tool_name} | Args: {kwargs}")
        
        try:
            result = func(*args, **kwargs)
            result_preview = result[:150] + "..." if len(result) > 150 else result
            logger.info(f"   ✅ Success: {result_preview}")
            forward_log("INFO", f"✅ MCP TOOL SUCCESS: {tool_name}")
            return result
        except Exception as e:
            logger.error(f"   ❌ Error: {str(e)}")
            forward_log("ERROR", f"❌ MCP TOOL ERROR: {tool_name} | {str(e)}")
            raise
    return wrapper

# Initialize FastMCP server
mcp = FastMCP(
    name="payment-inquiry-mcp",
    instructions="""
    This MCP server provides tools for querying payment and transaction data.
    
    Available capabilities:
    - List and search payments by various criteria (payment ID, message ID, IBAN, status, channel, product)
    - List and search transactions by various criteria (transaction ID, payment ID, end-to-end ID, amount, currency)
    - Get detailed payment information including associated transactions
    - Get payment/transaction statistics
    
    Payment statuses: RCVD (Received), ACTC (Accepted Technical), ACSC (Completed), IAUT (In Authorization), RJCT (Rejected)
    Transaction statuses: ACTC (Accepted Technical), ACSC (Completed), RJCT (Rejected)
    """
)

logger.info("═══════════════════════════════════════════════════════════════")
logger.info("🚀 MCP Server Starting...")
logger.info(f"   Backend URL: {BACKEND_URL}")
logger.info("═══════════════════════════════════════════════════════════════")


# ============== Health & Stats Tools ==============

@mcp.tool()
@log_tool_call
def health_check() -> str:
    """Check overall API health status"""
    client = get_client()
    result = client.health_check()
    return json.dumps(result, indent=2)


@mcp.tool()
@log_tool_call
def get_inquiry_stats() -> str:
    """Get payment and transaction statistics including status breakdown"""
    client = get_client()
    result = client.get_stats()
    return json.dumps(result, indent=2)


# ============== Payment Tools ==============

@mcp.tool()
@log_tool_call
def list_payments(limit: int = 10, offset: int = 0) -> str:
    """
    List all payments with pagination.
    
    Args:
        limit: Maximum number of results (1-100, default: 10)
        offset: Number of records to skip (default: 0)
    
    Returns:
        JSON with total count and list of payment records
    """
    client = get_client()
    result = client.list_payments(limit=limit, offset=offset)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def search_payments(
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
) -> str:
    """
    Search payments with various filters.
    
    Args:
        pmt_id: Payment ID to search for
        msg_id: Message ID to search for
        iban: Originator IBAN to filter by
        status: Payment status (RCVD, ACTC, ACSC, IAUT, RJCT)
        channel: Channel name (e.g., MOBP, MINGZ, MMINGP)
        product: Product name (e.g., INST, SEPA-CT)
        date_from: Start date filter (ISO format)
        date_to: End date filter (ISO format)
        limit: Maximum results (default: 10)
        offset: Records to skip (default: 0)
    
    Returns:
        JSON with matching payment records
    """
    client = get_client()
    result = client.search_payments(
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
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_payment(pmt_id: str) -> str:
    """
    Get payment details by payment ID.
    
    Args:
        pmt_id: The payment ID (UUID format)
    
    Returns:
        JSON with full payment details including status history and audit log
    """
    client = get_client()
    result = client.get_payment(pmt_id)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_payment_with_transactions(pmt_id: str) -> str:
    """
    Get payment along with all associated transactions.
    
    Args:
        pmt_id: The payment ID (UUID format)
    
    Returns:
        JSON with payment details and list of related transactions
    """
    client = get_client()
    result = client.get_payment_full(pmt_id)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_payment_by_message_id(msg_id: str) -> str:
    """
    Get payment by message ID.
    
    Args:
        msg_id: The message ID (UUID format)
    
    Returns:
        JSON with payment details
    """
    client = get_client()
    result = client.get_payment_by_message(msg_id)
    return json.dumps(result, indent=2, default=str)


# ============== Transaction Tools ==============

@mcp.tool()
@log_tool_call
def list_transactions(limit: int = 10, offset: int = 0) -> str:
    """
    List all transactions with pagination.
    
    Args:
        limit: Maximum number of results (1-100, default: 10)
        offset: Number of records to skip (default: 0)
    
    Returns:
        JSON with total count and list of transaction records
    """
    client = get_client()
    result = client.list_transactions(limit=limit, offset=offset)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def search_transactions(
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
) -> str:
    """
    Search transactions with various filters.
    
    Args:
        tx_id: Transaction ID to search for
        pmt_id: Payment ID to filter by
        end_to_end_id: End-to-end ID to search for
        iban: IBAN (originator or counterparty) to filter by
        status: Transaction status (ACTC, ACSC, RJCT)
        channel: Channel name (e.g., MOBP, MINGZ, MMINGP)
        product: Product name (e.g., INST, SEPA-CT)
        amount_min: Minimum transaction amount
        amount_max: Maximum transaction amount
        currency: Currency code (e.g., EUR)
        date_from: Start date filter (ISO format)
        date_to: End date filter (ISO format)
        limit: Maximum results (default: 10)
        offset: Records to skip (default: 0)
    
    Returns:
        JSON with matching transaction records
    """
    client = get_client()
    result = client.search_transactions(
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
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_transaction(tx_id: str) -> str:
    """
    Get transaction details by transaction ID.
    
    Args:
        tx_id: The transaction ID (UUID format)
    
    Returns:
        JSON with full transaction details including amount, counterparty, and status history
    """
    client = get_client()
    result = client.get_transaction(tx_id)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_transactions_by_payment(pmt_id: str) -> str:
    """
    Get all transactions associated with a payment.
    
    Args:
        pmt_id: The payment ID (UUID format)
    
    Returns:
        JSON with list of transactions for the payment
    """
    client = get_client()
    result = client.get_transactions_by_payment(pmt_id)
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
@log_tool_call
def get_transaction_by_end_to_end_id(e2e_id: str) -> str:
    """
    Get transaction by end-to-end ID.
    
    Args:
        e2e_id: The end-to-end ID
    
    Returns:
        JSON with transaction details
    """
    client = get_client()
    result = client.get_transaction_by_e2e(e2e_id)
    return json.dumps(result, indent=2, default=str)


# ============== Run Server ==============

# Create main FastAPI app
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from typing import Optional as Opt

app = FastAPI(
    title="Payment Inquiry MCP Server",
    description="MCP Server with REST API for Payment and Transaction Inquiry",
    version="0.2.0"
)

# Mount MCP protocol endpoint
mcp_app = mcp.http_app(path="/mcp")
app.mount("/mcp-proto", mcp_app)


# ============== REST API Endpoints (for simple HTTP access) ==============
# These endpoints allow direct HTTP calls to MCP tools without MCP protocol

rest_router = APIRouter(prefix="/api", tags=["REST API"])


class SearchPaymentsRequest(BaseModel):
    payment_id: Opt[str] = None
    debtor_iban: Opt[str] = None
    creditor_iban: Opt[str] = None
    status: Opt[str] = None
    channel: Opt[str] = None
    product: Opt[str] = None
    limit: int = 10


class SearchTransactionsRequest(BaseModel):
    transaction_id: Opt[str] = None
    payment_id: Opt[str] = None
    status: Opt[str] = None
    min_amount: Opt[float] = None
    max_amount: Opt[float] = None
    currency: Opt[str] = None
    limit: int = 10


@rest_router.get("/health")
def api_health():
    """REST endpoint for health check"""
    client = get_client()
    return client.health_check()


@rest_router.get("/stats")
def api_stats():
    """REST endpoint for stats"""
    client = get_client()
    return client.get_stats()


@rest_router.get("/payments")
def api_list_payments(limit: int = 10, offset: int = 0):
    """REST endpoint to list payments"""
    client = get_client()
    return client.list_payments(limit, offset)


@rest_router.post("/payments/search")
def api_search_payments(req: SearchPaymentsRequest):
    """REST endpoint to search payments"""
    try:
        client = get_client()
        return client.search_payments(
            pmt_id=req.payment_id,
            iban=req.debtor_iban or req.creditor_iban,  # Map to api_client's iban param
            status=req.status,
            channel=req.channel,
            product=req.product,
            limit=req.limit
        )
    except Exception as e:
        import traceback
        print(f"Search payments error: {e}")
        traceback.print_exc()
        raise


@rest_router.get("/payments/{payment_id}")
def api_get_payment(payment_id: str):
    """REST endpoint to get a payment"""
    client = get_client()
    return client.get_payment(payment_id)


@rest_router.get("/payments/{payment_id}/full")
def api_get_payment_with_transactions(payment_id: str):
    """REST endpoint to get payment with transactions"""
    client = get_client()
    return client.get_payment_with_transactions(payment_id)


@rest_router.get("/payments/by-message/{message_id}")
def api_get_payment_by_message_id(message_id: str):
    """REST endpoint to get payment by message ID"""
    client = get_client()
    return client.get_payment_by_message_id(message_id)


@rest_router.get("/transactions")
def api_list_transactions(limit: int = 10, offset: int = 0):
    """REST endpoint to list transactions"""
    client = get_client()
    return client.list_transactions(limit, offset)


@rest_router.post("/transactions/search")
def api_search_transactions(req: SearchTransactionsRequest):
    """REST endpoint to search transactions"""
    client = get_client()
    return client.search_transactions(
        transaction_id=req.transaction_id,
        payment_id=req.payment_id,
        status=req.status,
        min_amount=req.min_amount,
        max_amount=req.max_amount,
        currency=req.currency,
        limit=req.limit
    )


@rest_router.get("/transactions/{transaction_id}")
def api_get_transaction(transaction_id: str):
    """REST endpoint to get a transaction"""
    client = get_client()
    return client.get_transaction(transaction_id)


@rest_router.get("/transactions/by-payment/{payment_id}")
def api_get_transactions_by_payment(payment_id: str):
    """REST endpoint to get transactions by payment"""
    client = get_client()
    return client.get_transactions_by_payment(payment_id)


@rest_router.get("/transactions/by-e2e/{e2e_id}")
def api_get_transaction_by_e2e(e2e_id: str):
    """REST endpoint to get transaction by end-to-end ID"""
    client = get_client()
    return client.get_transaction_by_e2e(e2e_id)


# Add REST router to the app
app.include_router(rest_router)


if __name__ == "__main__":
    import uvicorn
    import sys
    # Default port 8002 to avoid conflict with Mock API (8001)
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8002
    uvicorn.run(app, host="0.0.0.0", port=port)
