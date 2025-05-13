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
        for file_name in os.listdir(self.directory):
            file_path = os.path.join(self.directory, file_name)

            if os.path.isdir(file_path):
                continue  

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
