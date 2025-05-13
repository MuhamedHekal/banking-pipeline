import uuid # for generating Unique id for error_id
from src.services.Logger import Logger
from src.services.EmailNotifier import EmailNotifier
from datetime import datetime
class ErrorHandler:
    def __init__(self, logger, email_notifier):
        self.logger = logger
        self.email_notifier = email_notifier

    def handle(self, exception, context):
        error_id = str(uuid.uuid4())
        file_path = context.file_path
        error_msg = f"Error id : {error_id} file_path : {file_path}, exception: {str(exception)}"
        self.logger.log(error_msg)
        context.add_error(error_msg)
        # send email for debugging
        self.email_notifier.send_email( subject=f"Pipeline Error: {error_id}", body=error_msg)
        context.stop()# Stop pipeline for this file
        return context


"""
from src.core.PipelineContext import PipelineContext
from src.components.Validator import Validator
if __name__ == "__main__":
    context = PipelineContext(file_path='../incoming_data/2025-04-18/14/customer_profiles.csv')
    v1 = Validator()
    logger = Logger()
    emailnotifier = EmailNotifier()
    context = v1.process(context)
    error_handler = ErrorHandler(logger, emailnotifier)
    error_handler.handle("exception1", context)
    print(context.errors)
"""
    
