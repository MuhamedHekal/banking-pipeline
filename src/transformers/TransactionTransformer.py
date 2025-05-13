import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.transformers.loaders.JsonLoader import JsonLoader
class TransactionTransformer(JsonLoader):
    def transform(self, data):
        for record in data:
            amount = float(record['transaction_amount'])
            record['cost'] = 0.5 + (amount * 0.001)
            record['total_amount'] = amount + record['cost']
            self._add_data_quality_columns(record)
        return data


# def main():
#     transaction_data = [
#         {"transaction_id": "TX1001", "transaction_amount": "1000"},
#         {"transaction_id": "TX1002", "transaction_amount": "2000"},
#         {"transaction_id": "TX1003", "transaction_amount": "1500"},
#     ]

#     transformer = TransactionTransformer()
#     transformed_data = transformer.transform(transaction_data)

#     for record in transformed_data:
#         print(record)
        
# if __name__ == "__main__":
#     main()



# if __name__ == "__main__":
#     l= TransactionTransformer()
#     print(l.load_data('../incoming_data/2025-04-18/14/transactions.json')[0])