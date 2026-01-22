# Mock API - Sample Data Summary

## Overview
The Mock API services now come pre-populated with realistic sample data for demonstration and testing purposes.

---

## 1. Infrastructure Service (Search Indices)

### Sample Indices Created:
1. **products** - Contains product information
2. **users** - Contains user information
3. **orders** - Contains order information

### Sample Data in Each Index:

#### Products Index
- iPhone 15 Pro Max - Advanced camera smartphone ($1199)
- Samsung Galaxy S24 Ultra - Premium Android phone ($1299)
- MacBook Pro 16 - Professional laptop ($2499)

#### Users Index
- John Doe - Premium customer from New York (50+ orders)
- Jane Smith - VIP member from California (128 orders)
- Robert Johnson - Inactive user from Texas (12 orders)

#### Orders Index
- Order #ORD001 - iPhone 15 Pro Max delivery (Status: delivered)
- Order #ORD002 - MacBook Pro order (Status: in_transit)
- Order #ORD003 - Galaxy S24 Ultra return (Status: refunded)

**Endpoints to Test:**
```
GET  /api/v1/infra/indices                    # List all indices with document counts
GET  /api/v1/infra/indices/{index_id}         # Get specific index details
POST /api/v1/infra/indices/{index_id}/search  # Search documents in an index
GET  /api/v1/infra/indices/{index_id}/documents/{doc_id}
```

---

## 2. Inquiry Service

### Sample Inquiries Created:

1. **Unable to login to account** (HIGH Priority)
   - Status: IN_PROGRESS
   - Assigned to: support_agent_01
   - Tags: login, account, urgent
   - Responses: 2 (1 public, 1 internal)

2. **Refund request for order #ORD001** (HIGH Priority)
   - Status: OPEN
   - Product: Damaged product return
   - Tags: refund, damaged, return
   - Responses: None

3. **Shipping address update needed** (MEDIUM Priority)
   - Status: OPEN
   - Tags: shipping, address
   - Responses: None

4. **Question about product features** (LOW Priority)
   - Status: RESOLVED
   - Topic: Battery life inquiry
   - Tags: product, features, info
   - Responses: None

**Endpoints to Test:**
```
GET    /api/v1/inquiries/                     # List all inquiries
GET    /api/v1/inquiries/{inquiry_id}         # Get inquiry details
GET    /api/v1/inquiries/{inquiry_id}/responses
POST   /api/v1/inquiries/{inquiry_id}/responses  # Add response to inquiry
GET    /api/v1/inquiries/search?query=login   # Search inquiries
```

---

## 3. Document Service

### Sample Documents Created:

1. **Product_Specifications.pdf** (PDF)
   - Size: 2.0 MB
   - Department: Product
   - Version: 1.0
   - Tags: specifications, product, technical

2. **Q4_2024_Financial_Report.xlsx** (Spreadsheet)
   - Size: 512 KB
   - Department: Finance
   - Quarter: Q4 2024
   - Tags: financial, report, confidential

3. **User_Guide.pdf** (PDF)
   - Size: 3.0 MB
   - Department: Documentation
   - Version: 2.1
   - Tags: guide, user, documentation

4. **Marketing_Campaign_Presentation.pptx** (Presentation)
   - Size: 5.0 MB
   - Department: Marketing
   - Campaign: 2025_Spring
   - Tags: marketing, campaign, presentation

5. **API_Documentation.md** (Text)
   - Size: 256 KB
   - Department: Development
   - API Version: 2.0
   - Tags: api, documentation, development

6. **Company_Logo.png** (Image)
   - Size: 1.0 MB
   - Department: Branding
   - Format: PNG
   - Tags: logo, branding, image

7. **Database_Backup_2024.tar.gz** (Archive)
   - Size: 1.0 GB
   - Department: DevOps
   - Date: 2024-12-31
   - Tags: backup, database, archive

**Endpoints to Test:**
```
GET  /api/v1/documents/                       # List all documents
GET  /api/v1/documents/{doc_id}                # Get document details
GET  /api/v1/documents/{doc_id}/versions       # Get document versions
GET  /api/v1/documents/{doc_id}/preview        # Get document preview
```

---

## API Access

**Base URL:** `http://localhost:8001`

**API Documentation:**
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

**Health Checks:**
```bash
# Overall health
curl http://localhost:8001/health

# Service-specific health
curl http://localhost:8001/api/v1/infra/health
curl http://localhost:8001/api/v1/inquiries/health
curl http://localhost:8001/api/v1/documents/health
```

---

## Testing Examples

### Infrastructure Service - Search
```bash
curl "http://localhost:8001/api/v1/infra/indices"

# Search for "iPhone"
curl "http://localhost:8001/api/v1/infra/indices/{index_id}/search?query=iPhone&limit=10"
```

### Inquiry Service - List
```bash
curl "http://localhost:8001/api/v1/inquiries/"

# Filter by status
curl "http://localhost:8001/api/v1/inquiries/?status=open&priority=high"

# Search inquiries
curl "http://localhost:8001/api/v1/inquiries/search?query=login"
```

### Document Service - List
```bash
curl "http://localhost:8001/api/v1/documents/"

# Filter by type
curl "http://localhost:8001/api/v1/documents/?doc_type=pdf"

# Get specific document
curl "http://localhost:8001/api/v1/documents/{doc_id}"
```

---

## Key Features of Mock Data

✅ **Realistic Data** - Uses realistic names, product descriptions, and scenarios
✅ **Relationships** - Documents reference each other (e.g., orders reference customers)
✅ **Varied Statuses** - Different status values for testing filters
✅ **Metadata** - Rich metadata for each entity
✅ **Timestamps** - All records have creation/update timestamps
✅ **Responsive Service** - Ready to test CRUD operations

---

## Notes

- All mock data is stored in-memory and persists during the server lifetime
- Creating/updating/deleting records adds/modifies the mock data
- When you restart the server, the mock data is reloaded fresh
- No database required - perfect for demo and testing
