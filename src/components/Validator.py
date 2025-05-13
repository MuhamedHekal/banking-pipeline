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
                valid = self.validate_schema(context.file_path, schema)
                if not valid['valid_status'] :
                        context.add_error(f"the file {context.file_path} has invalid schema ")
                        context.add_metadata("validation_result", valid)
                        return context
                context.add_metadata("validation_result", valid)
                return context
                       
        
        def validate_schema(self, file_path, schema):
                """ return Json object
                { validation_time: Timestamp , valid_status : true}
                """
                result = {}
                # get header of the file_path
                with open(file_path, 'r') as f:
                       header = f.readline()
                
                header_columns= [col.strip() for col in header.split(',')]
                result['validation_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if header_columns == schema['columns']:
                       result['valid_status'] = True
                else:
                       result['valid_status'] = False
                return result
                

"""
testing
if __name__ == "__main__":
    context = PipelineContext(file_path='../incoming_data/2025-04-18/14/customer_profiles.csv')
    v1 = Validator()
    context = v1.process(context)
    print(context.metadata)
"""
