from src.transformers.Transformer import Transformer
class TxtLoader(Transformer):
    def load_data(self, file_path):
        # read the file path as line and return list of lines (as txt)
        """
        ['customer_id|loan_type|amount_utilized|utilization_date|loan_reason', 'CUST026688|Top-Up Loan|172000|2025-03-02|Let me know if we could spend a lazy Sunday just binge-watching old shows']
        """
        with open(file_path, 'r') as f:
            return [line.strip() for line in f if line.strip()]