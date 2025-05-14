from src.core.PipelineComponent import PipelineComponent
import json
import os 
from datetime import datetime
class Validator(PipelineComponent):
        def __init__(self, config_path='config/schemas.json'):
                with open(config_path) as f:
                        self.config = json.load(f)

        def process(self, context):
                # validate the file to it's schema 
                # if the context doesn't have the file_name add error to context 
                if not context.file_path :
                        context.add_error("the context does not have file_path")
                        return context
                file_name = os.path.basename(context.file_path)
                #print(file_name)
                # if the file_name not has a schema in the config/schemas.json add error 
                if file_name not in self.config['schemas']:
                       context.add_error(f"the {file_name} not have a supported schema")
                       return context
                # now validate the schema 
                schema = self.config['schemas'][file_name]
                #print(schema)
                valid = self.validate_schema(context.file_path, schema,context.metadata.get('file_type'))
                if not valid['valid_status'] :
                        context.add_error(f"the file {context.file_path} has invalid schema ")
                        context.add_metadata("validation_result", valid)
                        return context
                context.add_metadata("validation_result", valid)
                return context
                       
        
        def validate_schema(self, file_path, schema,file_type):
                result = {
                'validation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'valid_status': False
                }
                print(file_type)
                try:
                        if file_type == ".csv":
                                # CSV validation
                                with open(file_path, 'r') as f:
                                        header = f.readline()
                                        header_columns = [col.strip() for col in header.split(',')]
                                        result['valid_status'] = (header_columns == schema['columns'])
                                
                        elif file_type == ".txt":
                                # TXT validation (pipe-delimited)
                                with open(file_path, 'r') as f:
                                        header = f.readline()
                                        header_columns = [col.strip() for col in header.split('|')]
                                        result['valid_status'] = (header_columns == schema['columns'])
                                
                        elif file_type == ".json":
                                # JSON validation - check if it's valid JSON
                                import json
                                with open(file_path, 'r') as f:
                                        data = json.load(f)
                                # For JSON, we won't check headers since it doesn't have them
                                # Instead, we'll trust that if it loads as valid JSON, it's okay
                                # You could add specific structure validation here if needed
                                result['valid_status'] = True
                                
                        else:
                                result['valid_status'] = False
                                result['error'] = f"Unsupported file type: {file_type}"
                                
                except Exception as e:
                        result['valid_status'] = False
                        result['error'] = str(e)
                
                return result
                        

"""
testing
if __name__ == "__main__":
    context = PipelineContext(file_path='../incoming_data/2025-04-18/14/customer_profiles.csv')
    v1 = Validator()
    context = v1.process(context)
    print(context.metadata)
"""
