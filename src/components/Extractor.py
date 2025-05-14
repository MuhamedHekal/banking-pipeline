from src.core.PipelineComponent import PipelineComponent
import os
import shutil
import re

class Extractor(PipelineComponent):
    def __init__(self, destination_dir):
        self.destination_dir = destination_dir
        if not self.destination_dir:
            raise ValueError("Target cannot be None")
        if not isinstance(self.destination_dir, str):
            raise TypeError("Target must be a string")
        os.makedirs(destination_dir, exist_ok=True)
    
    def process(self, context):
        if not context.file_path:
            context.add_error("No file path in context")    
            return context
            
        if not os.path.exists(context.file_path):
            context.add_error("Source File does not exist")
            return context
            
        # Extract date and hour from the input path
        file_path_parts = os.path.normpath(context.file_path).split(os.sep)
        # Handle case where there might not be date/hour directories
        if len(file_path_parts) >= 3:
            # Check if the directory looks like a date (YYYY-MM-DD format)
            date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
            for i, part in enumerate(file_path_parts):
                if date_pattern.match(part) and i+1 < len(file_path_parts):
                    date_dir = part
                    hour_dir = file_path_parts[i+1]
                    
                    # Store date/hour in context metadata
                    context.add_metadata("input_date_dir", date_dir)
                    context.add_metadata("input_hour_dir", hour_dir)
                    
                    # Create matching directory structure in destination
                    output_dir = os.path.join(self.destination_dir, date_dir, hour_dir)
                    os.makedirs(output_dir, exist_ok=True)
                    
                    file_name = os.path.basename(context.file_path)
                    destination_path = os.path.join(output_dir, file_name)
                    break
        
        try:
            shutil.copy2(context.file_path, destination_path)
            print(f"Copied: {context.file_path} → {destination_path}")
        except Exception as e:
            context.add_error(f"Failed to copy file: {str(e)}")
            return context
            
        context.add_metadata("original_file_path", context.file_path)
        context.file_path = destination_path
        return context