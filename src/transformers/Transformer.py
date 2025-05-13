from src.core.PipelineComponent import PipelineComponent
from abc import ABC, abstractmethod
class Transformer(PipelineComponent, ABC):
    @abstractmethod
    def transform(self, data):
        """Transform data and return the result"""
    def process(self, context):
        if not context.data and context.file_path:
            data = self._load_data(context.file_path)
            context.data = data
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