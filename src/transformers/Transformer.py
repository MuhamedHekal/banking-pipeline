from src.core.PipelineComponent import PipelineComponent
from abc import ABC, abstractmethod
class Transformer(PipelineComponent, ABC):
    @abstractmethod
    def transform(self, data):
        """Transform data and return the result"""
        pass
    def process(self, context):
        pass

    def load_data(self, file_path):
        # implemented by sup classes 
        pass