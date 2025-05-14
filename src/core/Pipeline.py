from src.core.PipelineContext import PipelineContext
from src.components.Listener import Listener
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
        try:
            context = PipelineContext(file_path=file_path)
            for component in self.components:
                try:
                    if self.logger:
                        self.logger.log(f"Processing {file_path} with {component.__class__.__name__}")
                    context = component.process(context)
                    if context.has_errors():
                        for error in context.errors:
                            self.logger.log(f"Error during processing: {error['error']}")
                    if context.should_stop():
                        if self.logger:
                            self.logger.log(f"Pipeline stopped by {component.__class__.__name__}")
                        break
                except Exception as e:
                    if self.logger:
                        self.logger.log(f"Exception in {component.__class__.__name__}: {str(e)}")
                    context.add_error(f"Exception in {component.__class__.__name__}: {str(e)}")
            
            # Even if there are errors, we should mark the file as attempted
            if self.state_manager:
                self.state_manager.mark_processed(file_path, {"has_errors": context.has_errors()})
            
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