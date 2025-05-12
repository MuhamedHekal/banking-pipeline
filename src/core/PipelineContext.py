# Carries both the actual data and metadata about the processing state
from datetime import datetime
class PipelineContext:
    def __init__(self, file_path=None, data=None):
        self.file_path = file_path # file path of the data
        self.data = data # the actual data
        self.metadata = {} # the metadata regarding to the processing file - holding data lineage 
        self.errors = [] # list of error that occured during the file processing
        self._should_stop = False # flag to indicate if the pipeline should stop or not

    def add_metadata(self, key, value):
        self.metadata[key] = value
        return self

    def add_error(self, error):
        self.errors.append({
            "timestamp": datetime.now().isoformat(),
            "error": str(error)
        })
        return self

    def has_errors(self):
        return len(self.errors) > 0

    def stop(self):
        self._should_stop = True
        return self
    
    def should_stop(self):
        return self._should_stop

