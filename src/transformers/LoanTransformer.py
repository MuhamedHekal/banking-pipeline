from src.transformers.loaders.TxtLoader import TxtLoader
from datetime import datetime
class LoanTransformer(TxtLoader):
    def __init__(self, encryptor):
        self.encryptor = encryptor


    def transform(self, data):
        "transform the load data"
        for record in data:
            # Calculate loan age
            utilization_date = datetime.strptime(record['utilization_date'], '%Y-%m-%d')
            today = datetime.now()
            record['age'] = (today - utilization_date).days

            # Calculate loan cost
            amount = float(record['amount_utilized'])
            annual_rate = 0.2  # 20%
            fixed_cost = 1000  # $1000
            record['total_cost'] = amount * annual_rate + fixed_cost
            
            # Encrypt loan reason
            if self.encryptor and 'loan_reason' in record:
                record['loan_reason'] = self.encryptor.encrypt(record['loan_reason'], f"loan_reason_{record['customer_id']}")
            # Add data quality columns
            self._add_data_quality_columns(record)
        return data


"""
from src.services.Encryptor import Encryptor
if __name__ == "__main__":
    encryptor = Encryptor()
    l= LoanTransformer(encryptor)
    data = l.load_data('../incoming_data/2025-04-18/14/loans.txt')
    print(l.transform(data)[0])
"""
