from src.transformers.Transformer import Transformer
import json
class JsonLoader(Transformer):
    def load_data(self, file_path):
        """
        return 
        {'sender': 'CUST000001', 'receiver': 'CUST015796', 'transaction_amount': 96, 'transaction_date': '2024-12-13'}
        """
        with open(file_path, 'r') as f:
            return json.load(f)