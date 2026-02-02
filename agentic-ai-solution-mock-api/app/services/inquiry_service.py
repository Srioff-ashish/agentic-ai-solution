"""Mock Inquiry Service - Payment and Transaction Data"""
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from app.models import (
    PaymentSearchQuery,
    TransactionSearchQuery,
    PaymentSearchResult,
    TransactionSearchResult,
)


class InquiryService:
    """Mock inquiry service for payments and transactions"""

    def __init__(self):
        self.payments: Dict[str, dict] = {}
        self.transactions: Dict[str, dict] = {}
        self._load_mock_data()

    def _load_mock_data(self):
        """Load payment and transaction data from mockdata JSON files"""
        # Get the mockdata directory path
        current_dir = Path(__file__).parent.parent.parent
        mockdata_dir = current_dir / "mockdata"

        # Load payment files (epayment01.json, epayment02.json, epayment03.json)
        for i in range(1, 4):
            payment_file = mockdata_dir / f"epayment0{i}.json"
            if payment_file.exists():
                try:
                    with open(payment_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        pmt_id = data.get("_source", {}).get("pmt-id")
                        if pmt_id:
                            self.payments[pmt_id] = data
                except Exception as e:
                    print(f"Error loading {payment_file}: {e}")

        # Load transaction files (epaymenttxn01.json, epaymenttxn02.json, epaymenttxn03.json)
        for i in range(1, 4):
            txn_file = mockdata_dir / f"epaymenttxn0{i}.json"
            if txn_file.exists():
                try:
                    with open(txn_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        tx_id = data.get("_source", {}).get("tx-id")
                        if tx_id:
                            self.transactions[tx_id] = data
                except Exception as e:
                    print(f"Error loading {txn_file}: {e}")

        print(f"Loaded {len(self.payments)} payments and {len(self.transactions)} transactions")

    # ============== Payment Methods ==============

    def get_payment(self, pmt_id: str) -> Optional[dict]:
        """Get payment by payment ID"""
        return self.payments.get(pmt_id)

    def get_payment_by_msg_id(self, msg_id: str) -> Optional[dict]:
        """Get payment by message ID"""
        for payment in self.payments.values():
            if payment.get("_source", {}).get("msg-id") == msg_id:
                return payment
        return None

    def search_payments(self, query: PaymentSearchQuery) -> PaymentSearchResult:
        """Search payments with filters"""
        results = []

        for payment in self.payments.values():
            source = payment.get("_source", {})

            # Apply filters
            if query.pmt_id and source.get("pmt-id") != query.pmt_id:
                continue
            if query.msg_id and source.get("msg-id") != query.msg_id:
                continue
            if query.iban and source.get("pmtInf-orgtAcct-id-iban") != query.iban:
                continue
            if query.status and source.get("pmt-sts") != query.status:
                continue
            if query.channel and source.get("ing-chnl-nm") != query.channel:
                continue
            if query.product and source.get("ing-prdct-nm") != query.product:
                continue

            # Date filters (simplified - just check if date matches)
            if query.date_from:
                rcvd_dt = source.get("ing-rcvd-dtTm", "")
                if rcvd_dt < query.date_from:
                    continue
            if query.date_to:
                rcvd_dt = source.get("ing-rcvd-dtTm", "")
                if rcvd_dt > query.date_to:
                    continue

            results.append(payment)

        total = len(results)
        paginated = results[query.offset : query.offset + query.limit]

        return PaymentSearchResult(
            total=total,
            count=len(paginated),
            offset=query.offset,
            limit=query.limit,
            payments=paginated
        )

    def list_all_payments(self, limit: int = 10, offset: int = 0) -> PaymentSearchResult:
        """List all payments with pagination"""
        all_payments = list(self.payments.values())
        total = len(all_payments)
        paginated = all_payments[offset : offset + limit]

        return PaymentSearchResult(
            total=total,
            count=len(paginated),
            offset=offset,
            limit=limit,
            payments=paginated
        )

    # ============== Transaction Methods ==============

    def get_transaction(self, tx_id: str) -> Optional[dict]:
        """Get transaction by transaction ID"""
        return self.transactions.get(tx_id)

    def get_transaction_by_pmt_id(self, pmt_id: str) -> List[dict]:
        """Get all transactions for a payment ID"""
        results = []
        for txn in self.transactions.values():
            if txn.get("_source", {}).get("pmt-id") == pmt_id:
                results.append(txn)
        return results

    def get_transaction_by_end_to_end_id(self, e2e_id: str) -> Optional[dict]:
        """Get transaction by end-to-end ID"""
        for txn in self.transactions.values():
            if txn.get("_source", {}).get("txInf-pmtId-endToEndId") == e2e_id:
                return txn
        return None

    def search_transactions(self, query: TransactionSearchQuery) -> TransactionSearchResult:
        """Search transactions with filters"""
        results = []

        for txn in self.transactions.values():
            source = txn.get("_source", {})

            # Apply filters
            if query.tx_id and source.get("tx-id") != query.tx_id:
                continue
            if query.pmt_id and source.get("pmt-id") != query.pmt_id:
                continue
            if query.end_to_end_id and source.get("txInf-pmtId-endToEndId") != query.end_to_end_id:
                continue
            if query.status and source.get("tx-sts") != query.status:
                continue
            if query.channel and source.get("ing-chnl-nm") != query.channel:
                continue
            if query.product and source.get("ing-prdct-nm") != query.product:
                continue
            if query.currency and source.get("txInf-amt-instdAmt-ccy") != query.currency:
                continue

            # IBAN filter (check both originator and counterparty)
            if query.iban:
                orig_iban = source.get("pmtInf-orgtAcct-id-iban", "")
                crpty_iban = source.get("txInf-crptyAcct-id-iban", "")
                if query.iban not in (orig_iban, crpty_iban):
                    continue

            # Amount filters
            amount = source.get("txInf-amt-instdAmt-value", 0)
            if query.amount_min is not None and amount < query.amount_min:
                continue
            if query.amount_max is not None and amount > query.amount_max:
                continue

            # Date filters
            if query.date_from:
                rcvd_dt = source.get("ing-rcvd-dtTm", "")
                if rcvd_dt < query.date_from:
                    continue
            if query.date_to:
                rcvd_dt = source.get("ing-rcvd-dtTm", "")
                if rcvd_dt > query.date_to:
                    continue

            results.append(txn)

        total = len(results)
        paginated = results[query.offset : query.offset + query.limit]

        return TransactionSearchResult(
            total=total,
            count=len(paginated),
            offset=query.offset,
            limit=query.limit,
            transactions=paginated
        )

    def list_all_transactions(self, limit: int = 10, offset: int = 0) -> TransactionSearchResult:
        """List all transactions with pagination"""
        all_txns = list(self.transactions.values())
        total = len(all_txns)
        paginated = all_txns[offset : offset + limit]

        return TransactionSearchResult(
            total=total,
            count=len(paginated),
            offset=offset,
            limit=limit,
            transactions=paginated
        )

    # ============== Combined Inquiry Methods ==============

    def get_payment_with_transactions(self, pmt_id: str) -> Optional[dict]:
        """Get payment along with its associated transactions"""
        payment = self.get_payment(pmt_id)
        if not payment:
            return None

        transactions = self.get_transaction_by_pmt_id(pmt_id)
        
        return {
            "payment": payment,
            "transactions": transactions,
            "transaction_count": len(transactions)
        }

    def get_stats(self) -> dict:
        """Get statistics about payments and transactions"""
        payment_statuses = {}
        transaction_statuses = {}

        for payment in self.payments.values():
            status = payment.get("_source", {}).get("pmt-sts", "UNKNOWN")
            payment_statuses[status] = payment_statuses.get(status, 0) + 1

        for txn in self.transactions.values():
            status = txn.get("_source", {}).get("tx-sts", "UNKNOWN")
            transaction_statuses[status] = transaction_statuses.get(status, 0) + 1

        return {
            "total_payments": len(self.payments),
            "total_transactions": len(self.transactions),
            "payment_statuses": payment_statuses,
            "transaction_statuses": transaction_statuses
        }


# Global service instance
inquiry_service = InquiryService()

