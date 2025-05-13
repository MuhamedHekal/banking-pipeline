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
        return context

    def _add_data_quality_columns(self, record):
        now = datetime.now()
        record['processing_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
        record['partition_date'] = now.strftime('%Y-%m-%d')
        record['partition_hour'] = int(now.strftime('%H'))
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
