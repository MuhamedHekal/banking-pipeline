from src.transformers.Transformer import Transformer
class TxtLoader(Transformer):
    def load_data(self, file_path):
        # read the file path as line and return list of lines (as txt)
        """
        {'customer_id': 'CUST051615', 'loan_type': 'Loan Against Deposit', 'amount_utilized': '968000', 'utilization_date': '2025-04-12', 'loan_reason': 'Let me know if we could go on a spontaneous road trip without much planning'}
        """
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
            headers = lines[0].split('|')  # First line = header
            data = [dict(zip(headers, line.split('|'))) for line in lines[1:]]
        return data