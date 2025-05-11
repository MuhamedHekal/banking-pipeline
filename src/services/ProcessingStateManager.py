class ProcessingStateManager:
    def __init__(self, state_file_path="state/processed_files.json"):
        self.state_file_path = state_file_path

    def load_state(self):
        pass

    def save_state(self):
        pass

    def mark_processed(self, file_path):
        pass

    def is_processed(self, file_path):
        pass
