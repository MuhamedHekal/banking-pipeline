import os
import pandas as pd
import re
from datetime import datetime
from src.core.PipelineComponent import PipelineComponent

class ParquetWriter(PipelineComponent):
    def __init__(self, target_dir):
        self.target_dir = target_dir
        os.makedirs(self.target_dir, exist_ok=True)
    
    def process(self, context):
        # Checks for DataFrame and file path
        if not hasattr(context, 'data') or context.data is None or (
                isinstance(context.data, pd.DataFrame) and context.data.empty):
            context.add_error("No data in context to write")
            return context
                
        if not hasattr(context, 'file_path') or not context.file_path:
            context.add_error("No file path provided in context")
            return context
        
        # Use date/hour directories from input metadata if available
        # Otherwise use current date/time
        date_dir = context.metadata.get("input_date_dir")
        hour_dir = context.metadata.get("input_hour_dir")
        
        if not date_dir or not hour_dir:
            # Fallback to extracting from file path if metadata not available
            file_path_parts = os.path.normpath(context.file_path).split(os.sep)
            date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
            
            for i, part in enumerate(file_path_parts):
                if date_pattern.match(part) and i+1 < len(file_path_parts):
                    date_dir = part
                    hour_dir = file_path_parts[i+1]
                    break
   
        # Create nested directory structure
        output_dir = os.path.join(self.target_dir, date_dir, hour_dir)
        os.makedirs(output_dir, exist_ok=True)
        
        # Determine output filename
        input_filename = os.path.basename(context.file_path)
        base_name = os.path.splitext(input_filename)[0]
        output_path = os.path.join(output_dir, f"{base_name}.parquet")
        
        try:
            # Convert the data to a DataFrame if it's not already
            if not isinstance(context.data, pd.DataFrame):
                df = pd.DataFrame(context.data)
            else:
                df = context.data
            
            # Write the DataFrame to a Parquet file
            df.to_parquet(output_path, index=False)
            
            # Add metadata with the complete output path
            context.add_metadata("output_file", output_path)
            context.add_metadata("output_date_dir", date_dir)
            context.add_metadata("output_hour_dir", hour_dir)
            
            # Log success for debugging
            print(f"Successfully wrote data to {output_path}")
            
        except Exception as e:
            error_msg = f"Error writing data to Parquet: {e}"
            context.add_error(error_msg)
            print(error_msg)  # Print for debugging
                
        return context