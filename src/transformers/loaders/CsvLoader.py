from src.transformers.Transformer import Transformer
import csv
class CsvLoader(Transformer):
    def load_data(self, file_path):
        # read the file path as line and return list of dict (as csv)
        # used of all csv extension
        """
        return 
        {'customer_id': 'CUST000001', 'name': 'Matthew Crawford', 'gender': 'Male', 'age': '19', 'city': 'Dubai', 'account_open_date': '2021-06-22', 'product_type': 'CreditCard', 'customer_tier': 'Gold'}
        """
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
        

