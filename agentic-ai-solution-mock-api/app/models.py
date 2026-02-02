"""Data models for mock services - Payment and Transaction Inquiry"""
from datetime import datetime
from enum import Enum
from typing import Any, Optional, List

from pydantic import BaseModel, Field


# ============== Payment Status Codes ==============

class PaymentStatus(str, Enum):
    """Payment status codes (ISO 20022)"""
    RCVD = "RCVD"  # Received
    ACTC = "ACTC"  # Accepted Technical Validation
    ACCP = "ACCP"  # Accepted Customer Profile
    ACSP = "ACSP"  # Accepted Settlement in Process
    ACSC = "ACSC"  # Accepted Settlement Completed
    IAUT = "IAUT"  # In Authorization
    RJCT = "RJCT"  # Rejected


class TransactionStatus(str, Enum):
    """Transaction status codes"""
    ACTC = "ACTC"  # Accepted Technical Validation
    ACSC = "ACSC"  # Accepted Settlement Completed
    RJCT = "RJCT"  # Rejected


# ============== Common Models ==============

class StatusHistoryItem(BaseModel):
    """Status history entry"""
    cd: str = Field(..., description="Status code")
    dtTm: str = Field(..., description="Date and time of status change")
    rsnCd: Optional[str] = Field(default=None, description="Reason code")
    rsn: Optional[str] = Field(default=None, description="Reason details")


class AuditLogEntry(BaseModel):
    """Audit log entry"""
    ref: str = Field(..., description="Reference code")
    log: str = Field(..., description="Log content")
    dtTm: str = Field(..., description="Timestamp")


# ============== Payment Model ==============

class PaymentSource(BaseModel):
    """Payment source data (nested under _source in raw data)"""
    pmt_id: str = Field(..., alias="pmt-id", description="Payment ID")
    pmt_sts: str = Field(..., alias="pmt-sts", description="Payment status")
    pmt_stsDtTm: str = Field(..., alias="pmt-stsDtTm", description="Status timestamp")
    pmt_rsnCd: Optional[str] = Field(default=None, alias="pmt-rsnCd", description="Reason code")
    
    msg_id: str = Field(..., alias="msg-id", description="Message ID")
    tenant: str = Field(..., description="Tenant identifier")
    
    ing_chnl_nm: str = Field(..., alias="ing-chnl-nm", description="Channel name")
    ing_prdct_nm: str = Field(..., alias="ing-prdct-nm", description="Product name")
    ing_rcvd_dtTm: str = Field(..., alias="ing-rcvd-dtTm", description="Received timestamp")
    ing_exctn_dt: str = Field(..., alias="ing-exctn-dt", description="Execution date")
    
    pmtInf_pmtInfId: str = Field(..., alias="pmtInf-pmtInfId", description="Payment Info ID")
    pmtInf_pmtMtd: str = Field(..., alias="pmtInf-pmtMtd", description="Payment method")
    pmtInf_nbOfTxs: int = Field(..., alias="pmtInf-nbOfTxs", description="Number of transactions")
    pmtInf_ctrlSum: str = Field(..., alias="pmtInf-ctrlSum", description="Control sum")
    
    pmtInf_orgtAcct_id_iban: str = Field(..., alias="pmtInf-orgtAcct-id-iban", description="Originator IBAN")
    pmtInf_orgt_nm: str = Field(..., alias="pmtInf-orgt-nm", description="Originator name")
    pmtInf_orgtAgt_finInstnId_BICFI: str = Field(..., alias="pmtInf-orgtAgt-finInstnId-BICFI", description="Originator BIC")
    
    pmtInf_pmtTpInf_svcLvl: str = Field(..., alias="pmtInf-pmtTpInf-svcLvl", description="Service level")
    pmtInf_pmtTpInf_lclInstrm: Optional[str] = Field(default=None, alias="pmtInf-pmtTpInf-lclInstrm", description="Local instrument")
    pmtInf_reqdExctnDt_dt: str = Field(..., alias="pmtInf-reqdExctnDt-dt", description="Requested execution date")
    
    grpHdr_msgId: str = Field(..., alias="grpHdr-msgId", description="Group header message ID")
    grpHdr_creDtTm: str = Field(..., alias="grpHdr-creDtTm", description="Creation datetime")
    grpHdr_nbOfTxs: int = Field(..., alias="grpHdr-nbOfTxs", description="Number of transactions")
    grpHdr_ctrlSum: str = Field(..., alias="grpHdr-ctrlSum", description="Control sum")
    grpHdr_initgPty_nm: str = Field(..., alias="grpHdr-initgPty-nm", description="Initiating party name")
    
    pmt_stsHist: List[StatusHistoryItem] = Field(default_factory=list, alias="pmt-stsHist", description="Status history")
    pmt_adtLog: List[AuditLogEntry] = Field(default_factory=list, alias="pmt-adtLog", description="Audit log")
    
    class Config:
        populate_by_name = True


# ============== Transaction Model ==============

class TransactionSource(BaseModel):
    """Transaction source data (nested under _source in raw data)"""
    tx_id: str = Field(..., alias="tx-id", description="Transaction ID")
    tx_sts: str = Field(..., alias="tx-sts", description="Transaction status")
    tx_stsDtTm: str = Field(..., alias="tx-stsDtTm", description="Status timestamp")
    tx_rsnCd: Optional[str] = Field(default=None, alias="tx-rsnCd", description="Reason code")
    tx_pos: int = Field(default=0, alias="tx-pos", description="Transaction position")
    
    pmt_id: str = Field(..., alias="pmt-id", description="Payment ID")
    msg_id: str = Field(..., alias="msg-id", description="Message ID")
    tenant: str = Field(..., description="Tenant identifier")
    
    ing_chnl_nm: str = Field(..., alias="ing-chnl-nm", description="Channel name")
    ing_prdct_nm: str = Field(..., alias="ing-prdct-nm", description="Product name")
    ing_rcvd_dtTm: str = Field(..., alias="ing-rcvd-dtTm", description="Received timestamp")
    
    pmtInf_pmtInfId: str = Field(..., alias="pmtInf-pmtInfId", description="Payment Info ID")
    pmtInf_pmtMtd: str = Field(..., alias="pmtInf-pmtMtd", description="Payment method")
    pmtInf_nbOfTxs: int = Field(..., alias="pmtInf-nbOfTxs", description="Number of transactions")
    pmtInf_ctrlSum: str = Field(..., alias="pmtInf-ctrlSum", description="Control sum")
    
    pmtInf_orgtAcct_id_iban: str = Field(..., alias="pmtInf-orgtAcct-id-iban", description="Originator IBAN")
    pmtInf_orgt_nm: str = Field(..., alias="pmtInf-orgt-nm", description="Originator name")
    pmtInf_orgtAgt_finInstnId_BICFI: str = Field(..., alias="pmtInf-orgtAgt-finInstnId-BICFI", description="Originator BIC")
    
    pmtInf_pmtTpInf_svcLvl: str = Field(..., alias="pmtInf-pmtTpInf-svcLvl", description="Service level")
    pmtInf_pmtTpInf_lclInstrm: Optional[str] = Field(default=None, alias="pmtInf-pmtTpInf-lclInstrm", description="Local instrument")
    pmtInf_reqdExctnDt_dt: str = Field(..., alias="pmtInf-reqdExctnDt-dt", description="Requested execution date")
    
    grpHdr_msgId: str = Field(..., alias="grpHdr-msgId", description="Group header message ID")
    
    txInf_pmtId_endToEndId: str = Field(..., alias="txInf-pmtId-endToEndId", description="End-to-end ID")
    txInf_pmtId_uetr: str = Field(..., alias="txInf-pmtId-uetr", description="UETR")
    txInf_amt_instdAmt_value: float = Field(..., alias="txInf-amt-instdAmt-value", description="Amount value")
    txInf_amt_instdAmt_ccy: str = Field(..., alias="txInf-amt-instdAmt-ccy", description="Currency")
    txInf_crpty_nm: str = Field(..., alias="txInf-crpty-nm", description="Counterparty name")
    txInf_crptyAcct_id_iban: str = Field(..., alias="txInf-crptyAcct-id-iban", description="Counterparty IBAN")
    txInf_crptyAcct_id_othr_BICFI: str = Field(..., alias="txInf-crptyAcct-id-othr-BICFI", description="Counterparty BIC")
    txInf_rmtInf_ustrd: Optional[str] = Field(default=None, alias="txInf-rmtInf-ustrd", description="Remittance info")
    
    tx_stsHist: List[StatusHistoryItem] = Field(default_factory=list, alias="tx-stsHist", description="Status history")
    tx_adtLog: List[AuditLogEntry] = Field(default_factory=list, alias="tx-adtLog", description="Audit log")
    
    class Config:
        populate_by_name = True


# ============== Search/Query Models ==============

class PaymentSearchQuery(BaseModel):
    """Payment search query"""
    pmt_id: Optional[str] = Field(default=None, description="Payment ID")
    msg_id: Optional[str] = Field(default=None, description="Message ID")
    iban: Optional[str] = Field(default=None, description="IBAN (originator)")
    status: Optional[str] = Field(default=None, description="Payment status")
    channel: Optional[str] = Field(default=None, description="Channel name")
    product: Optional[str] = Field(default=None, description="Product name")
    date_from: Optional[str] = Field(default=None, description="Start date filter")
    date_to: Optional[str] = Field(default=None, description="End date filter")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    offset: int = Field(default=0, ge=0, description="Offset")


class TransactionSearchQuery(BaseModel):
    """Transaction search query"""
    tx_id: Optional[str] = Field(default=None, description="Transaction ID")
    pmt_id: Optional[str] = Field(default=None, description="Payment ID")
    end_to_end_id: Optional[str] = Field(default=None, description="End-to-end ID")
    iban: Optional[str] = Field(default=None, description="IBAN (originator or counterparty)")
    status: Optional[str] = Field(default=None, description="Transaction status")
    channel: Optional[str] = Field(default=None, description="Channel name")
    product: Optional[str] = Field(default=None, description="Product name")
    amount_min: Optional[float] = Field(default=None, description="Minimum amount")
    amount_max: Optional[float] = Field(default=None, description="Maximum amount")
    currency: Optional[str] = Field(default=None, description="Currency")
    date_from: Optional[str] = Field(default=None, description="Start date filter")
    date_to: Optional[str] = Field(default=None, description="End date filter")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")
    offset: int = Field(default=0, ge=0, description="Offset")


class PaymentSearchResult(BaseModel):
    """Payment search results"""
    total: int = Field(..., description="Total matching records")
    count: int = Field(..., description="Returned records count")
    offset: int = Field(..., description="Offset")
    limit: int = Field(..., description="Limit")
    payments: List[dict] = Field(default_factory=list, description="Payment records")


class TransactionSearchResult(BaseModel):
    """Transaction search results"""
    total: int = Field(..., description="Total matching records")
    count: int = Field(..., description="Returned records count")
    offset: int = Field(..., description="Offset")
    limit: int = Field(..., description="Limit")
    transactions: List[dict] = Field(default_factory=list, description="Transaction records")


# ============== Legacy Models (kept for compatibility) ==============

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
