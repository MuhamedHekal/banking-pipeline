
import os
import json
from datetime import datetime
class ProcessingStateManager:
    def __init__(self, state_file_path="state/processed_files.json"):
        self.state_file_path = state_file_path
        os.makedirs(os.path.dirname(state_file_path), exist_ok=True)
        self.processed_files = self.load_state()
    def load_state(self):
        if os.path.exists(self.state_file_path):
            if not self.state_file_path.endswith('.json'):       
                raise ValueError("State file must be a JSON file.")
            if os.path.getsize(self.state_file_path) == 0:
                return {}
            try:
                with open(self.state_file_path, 'r') as f:
                    return json.load(f) 
            except json.JSONDecodeError:
                raise ValueError("State file is not a valid JSON file.")
        return {}
    def save_state(self):
        try:
            with open(self.state_file_path, 'w') as f: 
                json.dump(self.processed_files, f, indent=4)
        except IOError as e:
            raise IOError(f"Error saving state file: {e}")

    def mark_processed(self, file_path, metadata=None):
        print(f"Marking as processed: {file_path}")  # Debug log
        self.processed_files[file_path] = {
            "processed": True,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
            
        }
        self.save_state()
        print(f"State saved to: {self.state_file_path}")  # Debug log

    def is_processed(self, file_path):
         print(f"File {file_path} processed: {self.processed_files.get(file_path, {}).get('processed', False)}")
         return self.processed_files.get(file_path, {}).get("processed", False)
       
    def get_processing_metadata(self, file_path):
        return self.processed_files.get(file_path, {}).get("metadata", {})

