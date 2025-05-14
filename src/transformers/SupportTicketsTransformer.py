from src.transformers.loaders.CsvLoader import CsvLoader
from datetime import datetime
class SupportTicketsTransformer(CsvLoader):
    def transform(self, data):
        for record in data:
            # Calculate ticket age
            complaint_date = datetime.strptime(record['complaint_date'], '%Y-%m-%d')
            today = datetime.now()
            record['age'] = (today - complaint_date).days
            
            # Add data quality columns
            self._add_data_quality_columns(record)
        
        return data