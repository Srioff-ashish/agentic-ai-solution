# MCP Tools Reference

Quick reference for all 17 tools exposed by the MCP server.

## Infrastructure Service (5 tools)

### 1. infra_list_indices
**Purpose**: List all search indices
**Parameters**: None required
**Example**:
```
Tool: infra_list_indices
Arguments: {}
```
**Response**: Array of indices with metadata

### 2. infra_create_index
**Purpose**: Create a new search index
**Parameters**:
- `name` (string, required): Index name
- `settings` (object, optional): Index settings

**Example**:
```
Tool: infra_create_index
Arguments: {
  "name": "documents",
  "settings": {"replicas": 1, "shards": 5}
}
```
**Response**: Index creation confirmation with ID

### 3. infra_get_index
**Purpose**: Get details of a specific index
**Parameters**:
- `index_id` (string, required): Index ID

**Example**:
```
Tool: infra_get_index
Arguments: {"index_id": "products"}
```
**Response**: Index metadata and configuration

### 4. infra_index_document
**Purpose**: Index (add) a document to an index
**Parameters**:
- `index_id` (string, required): Target index ID
- `content` (string, required): Document content
- `metadata` (object, optional): Custom metadata

**Example**:
```
Tool: infra_index_document
Arguments: {
  "index_id": "products",
  "content": "iPhone 15 Pro - Latest Apple flagship",
  "metadata": {"category": "electronics", "price": 999}
}
```
**Response**: Document ID and indexing status

### 5. infra_search_documents
**Purpose**: Full-text search within an index
**Parameters**:
- `index_id` (string, required): Index to search
- `query` (string, required): Search query
- `limit` (integer, optional): Max results (default: 10)
- `offset` (integer, optional): Result offset (default: 0)

**Example**:
```
Tool: infra_search_documents
Arguments: {
  "index_id": "products",
  "query": "iPhone",
  "limit": 5
}
```
**Response**: Array of matching documents with relevance scores

---

## Inquiry Service (6 tools)

### 6. inquiry_list
**Purpose**: List inquiries with optional filters
**Parameters**:
- `status` (string, optional): Filter by status (open, in_progress, resolved, closed)
- `priority` (string, optional): Filter by priority (low, medium, high, critical)
- `skip` (integer, optional): Pagination offset (default: 0)
- `limit` (integer, optional): Results per page (default: 20)

**Example**:
```
Tool: inquiry_list
Arguments: {
  "status": "open",
  "priority": "high",
  "limit": 10
}
```
**Response**: Array of inquiries matching filters

### 7. inquiry_create
**Purpose**: Create a new support ticket
**Parameters**:
- `title` (string, required): Ticket title
- `description` (string, required): Detailed description
- `customer_id` (string, required): Customer/User ID
- `priority` (string, optional): Priority level (default: "medium")
- `tags` (array, optional): Category tags

**Example**:
```
Tool: inquiry_create
Arguments: {
  "title": "Cannot reset password",
  "description": "User unable to reset forgotten password",
  "customer_id": "cust_001",
  "priority": "high",
  "tags": ["account", "password"]
}
```
**Response**: New inquiry with assigned ID and timestamp

### 8. inquiry_get
**Purpose**: Get details of a specific inquiry
**Parameters**:
- `inquiry_id` (string, required): Inquiry ID

**Example**:
```
Tool: inquiry_get
Arguments: {"inquiry_id": "inq_001"}
```
**Response**: Complete inquiry details including responses

### 9. inquiry_add_response
**Purpose**: Add a response to an inquiry
**Parameters**:
- `inquiry_id` (string, required): Inquiry ID
- `content` (string, required): Response content
- `responder_id` (string, required): Staff member ID
- `is_internal` (boolean, optional): Internal note (default: false)

**Example**:
```
Tool: inquiry_add_response
Arguments: {
  "inquiry_id": "inq_001",
  "content": "Password reset link sent to registered email",
  "responder_id": "staff_001",
  "is_internal": false
}
```
**Response**: Response confirmation with timestamp

### 10. inquiry_update_status
**Purpose**: Update inquiry status
**Parameters**:
- `inquiry_id` (string, required): Inquiry ID
- `status` (string, required): New status (open, in_progress, resolved, closed)

**Example**:
```
Tool: inquiry_update_status
Arguments: {
  "inquiry_id": "inq_001",
  "status": "resolved"
}
```
**Response**: Status update confirmation

### 11. inquiry_search
**Purpose**: Search inquiries by title or description
**Parameters**:
- `query` (string, required): Search keywords
- `skip` (integer, optional): Pagination offset (default: 0)
- `limit` (integer, optional): Results per page (default: 20)

**Example**:
```
Tool: inquiry_search
Arguments: {
  "query": "login issue",
  "limit": 5
}
```
**Response**: Array of matching inquiries

---

## Document Service (6 tools)

### 12. document_list
**Purpose**: List documents with optional filters
**Parameters**:
- `doc_type` (string, optional): Filter by type (pdf, text, image, spreadsheet, presentation, archive)
- `upload_by` (string, optional): Filter by uploader
- `skip` (integer, optional): Pagination offset (default: 0)
- `limit` (integer, optional): Results per page (default: 20)

**Example**:
```
Tool: document_list
Arguments: {
  "doc_type": "pdf",
  "limit": 10
}
```
**Response**: Array of documents matching filters

### 13. document_upload
**Purpose**: Upload a new document
**Parameters**:
- `filename` (string, required): Original filename
- `doc_type` (string, required): Type (pdf, text, image, spreadsheet, presentation, archive)
- `file_size` (integer, required): File size in bytes
- `upload_by` (string, required): User ID
- `metadata` (object, optional): Custom metadata
- `tags` (array, optional): Document tags

**Example**:
```
Tool: document_upload
Arguments: {
  "filename": "Q4_2024_Report.xlsx",
  "doc_type": "spreadsheet",
  "file_size": 524288,
  "upload_by": "user_001",
  "metadata": {"year": 2024, "quarter": "Q4"},
  "tags": ["financial", "report", "2024"]
}
```
**Response**: Document ID and upload confirmation

### 14. document_get
**Purpose**: Get document details
**Parameters**:
- `doc_id` (string, required): Document ID

**Example**:
```
Tool: document_get
Arguments: {"doc_id": "doc_001"}
```
**Response**: Document metadata and details

### 15. document_preview
**Purpose**: Get document preview
**Parameters**:
- `doc_id` (string, required): Document ID

**Example**:
```
Tool: document_preview
Arguments: {"doc_id": "doc_001"}
```
**Response**: Document preview content

### 16. document_get_versions
**Purpose**: Get all versions of a document
**Parameters**:
- `doc_id` (string, required): Document ID

**Example**:
```
Tool: document_get_versions
Arguments: {"doc_id": "doc_001"}
```
**Response**: Array of document versions with timestamps

### 17. document_create_version
**Purpose**: Create a new version of a document
**Parameters**:
- `doc_id` (string, required): Document ID
- `new_filename` (string, required): New filename
- `new_file_size` (integer, required): File size in bytes
- `created_by` (string, required): User ID
- `change_description` (string, optional): Description of changes

**Example**:
```
Tool: document_create_version
Arguments: {
  "doc_id": "doc_001",
  "new_filename": "Q4_2024_Report_v2.xlsx",
  "new_file_size": 524300,
  "created_by": "user_001",
  "change_description": "Added Q4 financial projections"
}
```
**Response**: New version confirmation with version number

---

## Summary Statistics

- **Total Tools**: 17
- **Infrastructure Tools**: 5 (Search, Indexing, CRUD)
- **Inquiry Tools**: 6 (Ticket Management, Responses)
- **Document Tools**: 6 (Upload, Versioning, Management)
- **Required Parameters**: Varies (1-5 per tool)
- **Optional Parameters**: Most tools have 1-3 optional parameters
- **Response Format**: JSON (objects, arrays, strings)

## Common Workflows

### Search Products and Create Ticket
1. `infra_search_documents` - Find product info
2. `inquiry_create` - Create ticket with product details

### Document Version Control
1. `document_list` - Find document
2. `document_get_versions` - Check history
3. `document_create_version` - Create new version

### Support Ticket Management
1. `inquiry_list` - View open tickets
2. `inquiry_get` - Get ticket details
3. `inquiry_add_response` - Respond to customer
4. `inquiry_update_status` - Mark as resolved

---

**Last Updated**: 2024
**Tool Count**: 17
**Status**: ✅ All tools tested and ready
