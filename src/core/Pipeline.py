class Pipeline:
    def __init__(self):
        self.components = []
        self.error_handler = None
        self.logger = None
        self.state_manager = None
    def add_component(self, component):
        pass
    
    def set_error_handler(self, error_handler):
        pass
        
    def set_logger(self, logger):
        pass
        
    def set_state_manager(self, state_manager):
        pass
    
    def process_file(self, file_path):
        #حrocess a single file through the pipeline
        pass

    def run(self):
        pass