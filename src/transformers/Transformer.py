import sys
import os
from datetime import datetime 
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.PipelineComponent import PipelineComponent
from abc import ABC, abstractmethod
class Transformer(PipelineComponent, ABC):
    @abstractmethod
    def transform(self, data):
        pass

    def process(self, context):
        """Process data in context using the transform method"""
        if not context.data and not context.file_path:
            context.add_error("No data or file path in context")
            return context
            
        # If data not loaded yet, load it from file
        if not context.data and context.file_path:
            data = self.load_data(context.file_path)
            context.data = data
            
        # Transform the data
        try:
            transformed_data = self.transform(context)
            context.data = transformed_data
        except Exception as e:
            context.add_error(f"Transformation error: {str(e)}")
            
        return context

    def _add_data_quality_columns(self, file_path, record):
        now = datetime.now()
        record['processing_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
        partition_date = file_path.split('/')[1]
        record['partition_date'] = partition_date
        partition_hour = file_path.split('/')[2]
        record['partition_hour'] = partition_hour
        return record

    def load_data(self, file_path):
        # implemented by sup classes 
        pass


    # class DummyTransformer(Transformer):
#     def transform(self, data):
#         for record in data:
#             self._add_data_quality_columns(record)
#         return data


# # Main testing function
# def main():
#     sample_data = [
#         {'name': 'Alice', 'transaction_amount': '100'},
#         {'name': 'Bob', 'transaction_amount': '200'},
#     ]

#     transformer = DummyTransformer()
#     transformed_data = transformer.transform(sample_data)

#     for record in transformed_data:
#         print(record)


# if __name__ == "__main__":
#     main()
