# Agentic AI Solution - Mock API

Mock API services for the Agentic AI Solution. Provides **Payment and Transaction Inquiry** APIs using mock data.

## Services

1. **Payment Inquiry Service** - Query payments and transactions from mock e-payment data
2. **Infrastructure Service** - Mock Elasticsearch-like search and indexing
3. **Document Service** - Handle document storage, retrieval, and metadata

## Setup

### Prerequisites
- Python 3.9+
- Poetry

### Installation

```bash
# Install dependencies using Poetry
poetry install

# Run the development server
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Payment Inquiry Service (`/api/v1/inquiry`)

#### Health & Stats
- `GET /health` - Health check with payment/transaction counts
- `GET /stats` - Get statistics (status breakdown)

#### Payment Endpoints
- `GET /payments` - List all payments with pagination
- `GET /payments/search` - Search payments with filters:
  - `pmt_id` - Payment ID
  - `msg_id` - Message ID
  - `iban` - Originator IBAN
  - `status` - Payment status (RCVD, ACTC, ACSC, IAUT, RJCT)
  - `channel` - Channel name (MOBP, MINGZ, MMINGP)
  - `product` - Product name (INST, SEPA-CT)
  - `date_from`, `date_to` - Date range
- `GET /payments/{pmt_id}` - Get payment by ID
- `GET /payments/{pmt_id}/full` - Get payment with all transactions
- `GET /payments/by-message/{msg_id}` - Get payment by message ID

#### Transaction Endpoints
- `GET /transactions` - List all transactions with pagination
- `GET /transactions/search` - Search transactions with filters:
  - `tx_id` - Transaction ID
  - `pmt_id` - Payment ID
  - `end_to_end_id` - End-to-end ID
  - `iban` - IBAN (originator or counterparty)
  - `status` - Transaction status (ACTC, ACSC, RJCT)
  - `channel` - Channel name
  - `product` - Product name
  - `amount_min`, `amount_max` - Amount range
  - `currency` - Currency code
  - `date_from`, `date_to` - Date range
- `GET /transactions/{tx_id}` - Get transaction by ID
- `GET /transactions/by-payment/{pmt_id}` - Get all transactions for a payment
- `GET /transactions/by-e2e/{e2e_id}` - Get transaction by end-to-end ID

### Infrastructure Service (`/api/v1/infra`)
- `GET /health` - Health check
- `POST /indices` - Create search index
- `DELETE /indices/{index_id}` - Delete index
- `GET /indices` - List all indices
- `POST /indices/{index_id}/documents` - Index a document
- `GET /indices/{index_id}/search` - Search documents
- `GET /indices/{index_id}/documents/{doc_id}` - Get document

### Document Service (`/api/v1/documents`)
- `POST /upload` - Upload document
- `GET /` - List documents
- `GET /{doc_id}` - Get document metadata
- `PUT /{doc_id}` - Update document metadata
- `DELETE /{doc_id}` - Delete document
- `POST /{doc_id}/versions` - Create document version
- `GET /{doc_id}/versions` - Get document versions
- `GET /{doc_id}/preview` - Get document preview

## Mock Data

The mock data is located in the `mockdata/` folder:

### Payments (epayment01.json, epayment02.json, epayment03.json)
- Sample ING payment records with various statuses:
  - `RJCT` (Rejected), `IAUT` (In Authorization), `ACSC` (Completed)
- Contains full payment information including:
  - Payment ID, Message ID
  - Debtor/Originator details (IBAN, Name, BIC)
  - Status history and audit logs
  - Product and channel information

### Transactions (epaymenttxn01.json, epaymenttxn02.json, epaymenttxn03.json)
- Sample transaction records linked to payments
- Contains:
  - Transaction ID, Payment ID linkage
  - Amount, Currency
  - Creditor/Counterparty details
  - End-to-end ID, UETR
  - Status history

## Example Queries

```bash
# List all payments
curl http://localhost:8000/api/v1/inquiry/payments

# Search for rejected payments
curl "http://localhost:8000/api/v1/inquiry/payments/search?status=RJCT"

# Get payment with transactions
curl http://localhost:8000/api/v1/inquiry/payments/d145a790-8ef1-4776-8e98-92dad80f0a9d/full

# Search transactions by IBAN
curl "http://localhost:8000/api/v1/inquiry/transactions/search?iban=NL19INGB0588118729"

# Get stats
curl http://localhost:8000/api/v1/inquiry/stats
```

## Development

```bash
# Format code
poetry run black .

# Lint
poetry run flake8 .

# Sort imports
poetry run isort .

# Run tests
poetry run pytest
```
