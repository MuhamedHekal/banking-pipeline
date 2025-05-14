from src.transformers.loaders.CsvLoader import CsvLoader
from datetime import datetime

class CreditCardTransformer(CsvLoader):
    def transform(self, context):
        # No longer loading data from file_path, accepting data directly
        data = context.data
        for record in data:
            amount_due = float(record["amount_due"])
            amount_paid = float(record["amount_paid"])    
            # Calculate fully_paid flag
            record["fully_paid"] = amount_due <= amount_paid 

            # Calculate debt 
            record["debt"] = max(0, amount_due - amount_paid)

            # Parse dates for late_days calculation
            payment_date = datetime.strptime(record["payment_date"], '%Y-%m-%d')
            
            # Calculate due date (1st of the payment month)
            due_date = datetime(payment_date.year, payment_date.month, 1)
            
            # Calculate late days (ensure non-negative)
            late_days = (payment_date - due_date).days
            record["late_days"] = max(0, late_days)
            
            # Calculate fine
            record["fine"] = record["late_days"] * 5.15
            
            # Calculate total amount
            record["total_amount"] = amount_due + record["fine"]
            
            # Add data quality columns
            self._add_data_quality_columns(context.file_path, record)
            
        return data