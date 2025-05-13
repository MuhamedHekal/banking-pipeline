import PipelineContext
from components.Listener import Listener
class Pipeline:
    def __init__(self):
        self.components = []
        self.error_handler = None
        self.logger = None
        self.state_manager = None
    def add_component(self, component):
        self.components.append(component)
        return self
    
    def set_error_handler(self, error_handler):
        self.error_handler = error_handler
        return self
    
    def set_logger(self, logger):
        self.logger = logger
        return self
    def set_state_manager(self, state_manager):
        self.state_manager = state_manager
        return self
    
    def process_file(self, file_path):
        #process a single file through the pipeline
        if self.state_manager and self.state_manager.is_processed(file_path):
            if self.logger:
                self.logger.info(f"File {file_path} already processed. Skipping.")                
            return
        context = PipelineContext(file_path=file_path)
        if self.logger:
            self.logger.log(f"Starting processing of {file_path}")
        try:
            for component in self.components:
                if self.logger:
                    self.logger.log(f"Processing {file_path} with {component.__class__.__name__}")
                context = component.process(context)
                if context.should_stop():
                    if self.logger:
                        self.logger.log(f"Pipeline stopped by {component.__class__.__name__}")
                    break
            if self.state_manager and not context.has_errors():
                self.state_manager.mark_processed(file_path)
            if self.logger:
                self.logger.log(f"Completed processing of {file_path}")
            return context
        except Exception as e:
            if self.error_handler:
                self.error_handler.handle(e, context)
            else:
                raise e
    def run(self):
    # Find a listener component
        listener = None
        if not any(isinstance(c, Listener) for c in self.components):
            raise ValueError("Pipeline must contain a Listener component")
        for component in self.components:
            if isinstance(component, Listener):
                listener = component
                break
        # Start listening for files
        listener.start_listening(pipeline=self)