from src.core.PipelineComponent import PipelineComponent
import os
import shutil
class Extractor(PipelineComponent):
    def __init__(self,destination_dir ):
        self.destination_dir  = destination_dir 
        if not self.destination_dir :
            raise ValueError("Target cannot be None")
        if not isinstance(self.destination_dir , str):
            raise TypeError("Target must be a string")
        os.makedirs(destination_dir , exist_ok=True)
    
    def process(self, context):
        if not context.file_path :
            context.add_error("No file path in context")    
            return context
        if not os.path.exists(context.file_path):
            context.add_error("Source File does not exist")
            return context
        file_name = os.path.basename(context.file_path)     
        destination_path = os.path.join(self.destination_dir, file_name)    
        try:
            shutil.copy2(context.file_path, destination_path)
        except Exception as e:
            context.add_error(f"Failed to copy file: {str(e)}")
            return context          
        context.add_metadata("original_file_path", context.file_path)
        context.file_path = destination_path
        return context