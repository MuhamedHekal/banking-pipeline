from src.core.PipelineComponent import PipelineComponent
import json
import os 
from src.core.PipelineContext import PipelineContext
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
                        return context
                print("valid")
                context.add_metadata("validation_result", valid)
                       
        
        def validate_schema(self, file_path, schema):
               """ return Json objetc 
                {
                validation_time: Timestamp
                valid_status : true 
                errors: []
                }
               """
               return {'validation_time': 1, "valid_status": True, "errors" :[] }
                


if __name__ == "__main__":
    context = PipelineContext(file_path='/test/customer_profiles.csv')
    v1 = Validator()
    v1.process(context)

        
