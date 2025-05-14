from datetime import datetime
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.transformers.loaders.CsvLoader import CsvLoader
class CustomerTransformer(CsvLoader):
     def transform(self, context):
        data = context.data
        for record in data:
            account_open_date = datetime.strptime(record['account_open_date'], '%Y-%m-%d')
            today = datetime.now()
            tenure_years = (today - account_open_date).days / 365.25
            record['tenure'] = int(tenure_years)
            
            if tenure_years > 5:
                record['customer_segment'] = 'Loyal'
            elif tenure_years < 1:
                record['customer_segment'] = 'Newcomer'
            else:
                record['customer_segment'] = 'Normal'
                
            self._add_data_quality_columns(context.file_path, record)
          
        return data



# if __name__ == "__main__":
#     transformer = CustomerTransformer()
    
#     # Change this path based on where your CSV file is
#     csv_path = "incoming_data/2025-04-18/14/customer_profiles.csv"
    
#     try:
#         data = transformer.load_data(csv_path)
#         transformed_data = transformer.transform(data)
#         for record in transformed_data:
#             print(record)
#     except Exception as e:
#         print(f"Error during transformation: {e}")

"""
if __name__ == "__main__":
    l= CustomerTransformer()
    print(l.load_data('../incoming_data/2025-04-18/14/customer_profiles.csv')[0]['customer_id'])
"""