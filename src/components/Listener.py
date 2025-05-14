import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import time
from src.core.PipelineComponent import PipelineComponent
from src.services import ProcessingStateManager  

class Listener(PipelineComponent):
    def __init__(self, directory, state_manager):
        self.directory = directory
        self.state_manager = ProcessingStateManager()
        self.watching = False

    def process(self, context):
        return context

    def _get_new_files(self):
        new_files = []
        for root, _, filenames in os.walk(self.directory):
            for filename in filenames:
                if (filename.startswith('.')):
                    continue
                file_path = os.path.join(root, filename)

            if not self.state_manager.is_processed(file_path):
                new_files.append(file_path)

        return new_files

    def start_listening(self, pipeline):
        self.watching = True

        while self.watching:
            files = self._get_new_files()
            for file_path in files:
                pipeline.process_file(file_path)
            time.sleep(5)
