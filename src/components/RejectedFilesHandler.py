from src.core.PipelineComponent import PipelineComponent
import os
import shutil
import json
from datetime import datetime

class RejectedFilesHandler(PipelineComponent):
    def __init__(self, rejected_dir):
        self.rejected_dir = rejected_dir
        os.makedirs(rejected_dir, exist_ok=True)
    
    def process(self, context):
        # Only process files with errors
        if not context.has_errors():
            return context
            
        # Get original file path if available, otherwise use current path
        original_path = context.metadata.get("original_file_path", context.file_path)
        file_name = os.path.basename(original_path)
        
        # Preserve date/hour directory structure if available
        date_dir = context.metadata.get("input_date_dir")
        hour_dir = context.metadata.get("input_hour_dir")
        
        # Create rejected directory structure
        full_rejected_dir = os.path.join(self.rejected_dir, date_dir, hour_dir)    
        os.makedirs(full_rejected_dir, exist_ok=True)
        reject_file_path = os.path.join(full_rejected_dir, f"{file_name}")
        
        # Copy the file to rejected directory
        try:
            shutil.copy2(context.file_path, reject_file_path)
            
            # Save error info alongside the rejected file
            error_info = {
                "original_path": original_path,
                "rejected_timestamp": datetime.now().isoformat(),
                "errors": context.errors,
                "metadata": context.metadata
            }
            
            error_file_path = f"{reject_file_path}.errors.json"
            with open(error_file_path, 'w') as f:
                json.dump(error_info, f, indent=2)
                
            print(f"File with errors moved to: {reject_file_path}")
            print(f"Error details saved to: {error_file_path}")
            
            # Mark in context that file has been handled as rejected
            context.add_metadata("rejected", True)
            context.add_metadata("rejected_path", reject_file_path)
            
        except Exception as e:
            # Add error but don't stop pipeline
            error_msg = f"Failed to move file to rejected directory: {str(e)}"
            context.add_error(error_msg)
            print(error_msg)
            
        return context