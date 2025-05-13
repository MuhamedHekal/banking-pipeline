from src.core.PipelineComponent import PipelineComponent
import os
class FileTypeDetector(PipelineComponent):

    def process(self, context):
        # get the file extension and add it in the context metadata
        # then return the context
        if not context.file_path :
            context.add_error("no file type in the context")
            return context
        
        file_name = os.path.basename(context.file_path)
        #print(file_name)
        file_extension = os.path.splitext(file_name)[1].lower() # return tuple and extract just extension .csv
        
        match file_extension:
            case '.csv':
                context.add_metadata("file_type",".csv")
            case '.txt':
                context.add_metadata("file_type",".txt")
            case '.json':
                context.add_metadata("file_type",".json")
            case _ :
                context.add_error(f"Unsupported file type: {file_extension}")
        
        return context


"""
from src.core.PipelineContext import PipelineContext
if __name__ == "__main__":
    context = PipelineContext(file_path='../incoming_data/2025-04-18/14/customer_profiles.csv')
    file_type_detector = FileTypeDetector()
    file_type_detector.process(context)
    print(context.metadata)
"""