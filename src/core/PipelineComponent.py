from abc import ABC, abstractmethod
# abc for define abstract classes
class PipelineComponent(ABC):
    @abstractmethod
    def process(self, context):
        pass