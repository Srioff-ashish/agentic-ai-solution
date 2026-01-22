# Agentic AI Solution - Mock API

Mock API services for the Agentic AI Solution. Provides three main service modules:

1. **Infrastructure Service** - Mock Elasticsearch-like search and indexing
2. **Inquiry Service** - Manage inquiries, tracking, and responses
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

### Infrastructure Service (`/api/v1/infra`)
- `GET /health` - Health check
- `POST /indices` - Create search index
- `DELETE /indices/{index_id}` - Delete index
- `GET /indices` - List all indices
- `POST /indices/{index_id}/documents` - Index a document
- `GET /indices/{index_id}/search` - Search documents
- `GET /indices/{index_id}/documents/{doc_id}` - Get document

### Inquiry Service (`/api/v1/inquiries`)
- `POST /` - Create new inquiry
- `GET /` - List inquiries with filtering
- `GET /{inquiry_id}` - Get inquiry details
- `PUT /{inquiry_id}` - Update inquiry
- `POST /{inquiry_id}/responses` - Add response to inquiry
- `GET /{inquiry_id}/responses` - Get inquiry responses
- `PUT /{inquiry_id}/status` - Update inquiry status
- `DELETE /{inquiry_id}` - Delete inquiry

### Document Service (`/api/v1/documents`)
- `POST /upload` - Upload document
- `GET /` - List documents
- `GET /{doc_id}` - Get document metadata
- `PUT /{doc_id}` - Update document metadata
- `DELETE /{doc_id}` - Delete document
- `POST /{doc_id}/versions` - Create document version
- `GET /{doc_id}/versions` - Get document versions
- `GET /{doc_id}/preview` - Get document preview

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
