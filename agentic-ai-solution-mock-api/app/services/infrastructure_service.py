"""Mock Infrastructure Service"""
import uuid
from datetime import datetime
from typing import Dict, Optional

from app.models import (
    SearchIndex,
    IndexStatus,
    IndexedDocument,
    SearchQuery,
    SearchResult,
)


class InfrastructureService:
    """Mock Elasticsearch-like infrastructure service"""

    def __init__(self):
        self.indices: Dict[str, SearchIndex] = {}
        self.documents: Dict[str, Dict[str, IndexedDocument]] = {}
        self._populate_mock_data()

    def _populate_mock_data(self):
        """Populate with mock data for demonstration"""
        # Create mock indices
        products_index = self.create_index("products", {"replicas": 1, "shards": 5})
        users_index = self.create_index("users", {"replicas": 1, "shards": 3})
        orders_index = self.create_index("orders", {"replicas": 1, "shards": 3})

        # Add mock documents to products index
        products = [
            {
                "content": "iPhone 15 Pro Max - Latest Apple smartphone with advanced camera system",
                "metadata": {"product_id": "PROD001", "category": "Electronics", "price": 1199},
            },
            {
                "content": "Samsung Galaxy S24 Ultra - Premium Android phone with 200MP camera",
                "metadata": {"product_id": "PROD002", "category": "Electronics", "price": 1299},
            },
            {
                "content": "MacBook Pro 16 - Powerful laptop for developers and professionals",
                "metadata": {"product_id": "PROD003", "category": "Computers", "price": 2499},
            },
        ]
        for product in products:
            self.index_document(products_index.index_id, product["content"], product["metadata"])

        # Add mock documents to users index
        users = [
            {
                "content": "John Doe - Premium customer from New York with 50+ orders",
                "metadata": {"user_id": "USER001", "status": "active", "orders": 52},
            },
            {
                "content": "Jane Smith - VIP member from California interested in electronics",
                "metadata": {"user_id": "USER002", "status": "active", "orders": 128},
            },
            {
                "content": "Robert Johnson - Inactive user from Texas last active 6 months ago",
                "metadata": {"user_id": "USER003", "status": "inactive", "orders": 12},
            },
        ]
        for user in users:
            self.index_document(users_index.index_id, user["content"], user["metadata"])

        # Add mock documents to orders index
        orders = [
            {
                "content": "Order #ORD001 - Customer purchased iPhone 15 Pro Max on 2024-01-15",
                "metadata": {"order_id": "ORD001", "customer_id": "USER001", "status": "delivered"},
            },
            {
                "content": "Order #ORD002 - MacBook Pro delivery pending for customer from NY",
                "metadata": {"order_id": "ORD002", "customer_id": "USER002", "status": "in_transit"},
            },
            {
                "content": "Order #ORD003 - Galaxy S24 Ultra returned for refund processing",
                "metadata": {"order_id": "ORD003", "customer_id": "USER003", "status": "refunded"},
            },
        ]
        for order in orders:
            self.index_document(orders_index.index_id, order["content"], order["metadata"])

    def create_index(self, name: str, settings: Optional[dict] = None) -> SearchIndex:
        """Create a new search index"""
        index_id = str(uuid.uuid4())
        index = SearchIndex(
            index_id=index_id,
            name=name,
            status=IndexStatus.ACTIVE,
            document_count=0,
            settings=settings or {},
        )
        self.indices[index_id] = index
        self.documents[index_id] = {}
        return index

    def delete_index(self, index_id: str) -> bool:
        """Delete a search index"""
        if index_id in self.indices:
            del self.indices[index_id]
            if index_id in self.documents:
                del self.documents[index_id]
            return True
        return False

    def get_index(self, index_id: str) -> Optional[SearchIndex]:
        """Get index details"""
        return self.indices.get(index_id)

    def list_indices(self) -> list[SearchIndex]:
        """List all indices"""
        return list(self.indices.values())

    def index_document(
        self, index_id: str, content: str, metadata: Optional[dict] = None
    ) -> Optional[IndexedDocument]:
        """Add document to index"""
        if index_id not in self.indices:
            return None

        doc_id = str(uuid.uuid4())
        document = IndexedDocument(
            doc_id=doc_id,
            content=content,
            metadata=metadata or {},
        )

        self.documents[index_id][doc_id] = document
        
        # Update document count
        index = self.indices[index_id]
        index.document_count = len(self.documents[index_id])
        index.updated_at = datetime.utcnow()

        return document

    def get_document(self, index_id: str, doc_id: str) -> Optional[IndexedDocument]:
        """Get document from index"""
        if index_id not in self.documents:
            return None
        return self.documents[index_id].get(doc_id)

    def search(
        self, index_id: str, query: SearchQuery
    ) -> tuple[list[SearchResult], int]:
        """Search documents in index"""
        if index_id not in self.documents:
            return [], 0

        index_docs = self.documents[index_id]
        results = []

        # Simple keyword search with scoring
        query_words = query.query.lower().split()
        scored_results = []

        for doc_id, doc in index_docs.items():
            score = 0
            content_lower = doc.content.lower()

            # Calculate score based on keyword matches
            for word in query_words:
                occurrences = content_lower.count(word)
                score += occurrences * 10

            # Check metadata filters
            if query.filters:
                match = True
                for key, value in query.filters.items():
                    if doc.metadata.get(key) != value:
                        match = False
                        break
                if not match:
                    continue

            if score > 0:
                scored_results.append((doc_id, doc, score))

        # Sort by score descending
        scored_results.sort(key=lambda x: x[2], reverse=True)

        # Apply pagination
        total = len(scored_results)
        paginated = scored_results[query.offset : query.offset + query.limit]

        for doc_id, doc, score in paginated:
            results.append(
                SearchResult(
                    doc_id=doc_id,
                    content=doc.content,
                    score=min(score / 100.0, 1.0),  # Normalize score
                    metadata=doc.metadata,
                )
            )

        return results, total

    def delete_document(self, index_id: str, doc_id: str) -> bool:
        """Delete document from index"""
        if index_id not in self.documents:
            return False

        if doc_id in self.documents[index_id]:
            del self.documents[index_id][doc_id]
            
            # Update document count
            if index_id in self.indices:
                self.indices[index_id].document_count = len(self.documents[index_id])
                self.indices[index_id].updated_at = datetime.utcnow()
            
            return True
        return False


# Global service instance
infra_service = InfrastructureService()
