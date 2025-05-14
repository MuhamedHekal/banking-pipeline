# First, let's fix the imports
import os
import pandas as pd
from src.core.PipelineComponent import PipelineComponent
class ParquetWriter(PipelineComponent):
    def __init__(self, target_dir):
        self.target_dir = target_dir
        os.makedirs(self.target_dir, exist_ok=True)
    
    def process(self, context):
        # Use proper checks for DataFrame instead of direct boolean evaluation
        if not hasattr(context, 'data') or context.data is None or (
                isinstance(context.data, pd.DataFrame) and context.data.empty):
                context.add_error("No data in context to write")
                return context
                
        if not hasattr(context, 'file_path') or not context.file_path:
                context.add_error("No file path provided in context")
                return context
        
        input_filename = os.path.basename(context.file_path)
        base_name = os.path.splitext(input_filename)[0]
        output_path = os.path.join(self.target_dir, f"{base_name}.parquet")
        
        try:
                # Convert the data to a DataFrame if it's not already
                if not isinstance(context.data, pd.DataFrame):
                        df = pd.DataFrame(context.data)
                else:
                        df = context.data
                
                # Write the DataFrame to a Parquet file
                df.to_parquet(output_path, index=False)
                
                # Add metadata 
                context.add_metadata("output_file", output_path)
                
        except Exception as e:
                context.add_error(f"Error writing data to Parquet: {e}")
                
        return context


