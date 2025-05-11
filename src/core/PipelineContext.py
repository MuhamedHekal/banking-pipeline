
from datetime import datetime
class PipelineContext:
    def __init__(self, file_path=None, data=None):
        self.file_path = file_path
        self.data = data
        self.metadata = {}
        self.errors = []
        self._should_stop = False

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

