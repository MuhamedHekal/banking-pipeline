import os
import sys
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from src.components.Listener import Listener
from src.components.Extractor import Extractor
from src.components.Validator import Validator
from src.services.Logger import Logger
from src.services.ErrorHandler import ErrorHandler
from src.services.ProcessingStateManager import ProcessingStateManager
from src.transformers.CustomerTransformer import CustomerTransformer
from src.transformers.CreditCardTransformer import CreditCardTransformer
from src.transformers.LoanTransformer import LoanTransformer
from src.transformers.SupportTicketsTransformer import SupportTicketsTransformer
from src.transformers.TransactionTransformer import TransactionTransformer
from src.components.writers.ParquetWriter import ParquetWriter
from src.components.writers.HDFSUploader import HDFSUploader
from src.components.utilities.FileTypeDetector import FileTypeDetector
from src.components.utilities.TransformerSelector import TransformerSelector
from src.core.Pipeline import Pipeline
from src.services.EmailNotifier import EmailNotifier
from src.services.Encryptor import Encryptor
from src.components.RejectedFilesHandler import RejectedFilesHandler
def build_pipeline():
    """Build a complete pipeline"""
    # Create services
    logger = Logger(log_file="logs/pipeline.log")
    
    email_notifier = EmailNotifier(smtp_server='smtp.gmail.com',
    smtp_port=465,
    sender_email='hhekal000@gmail.com',
    sender_password='ujjkvtsvlmvdyblx',  # use app-specific password for Gmail
    recipient_emails=['hamohjdfjxv22@gmail.com'])
    error_handler = ErrorHandler(logger, email_notifier)
    state_manager = ProcessingStateManager()
    encryptor = Encryptor()

    # Create components
    listener = Listener(directory="Incoming_data",state_manager=state_manager)
    extractor = Extractor(destination_dir="Processing_data")
    validator = Validator(config_path="config/schemas.json")
  
    
    # Create transformers
    customer_transformer = CustomerTransformer()
    credit_card_transformer = CreditCardTransformer()
    loan_transformer = LoanTransformer(encryptor=encryptor)
    support_transformer = SupportTicketsTransformer()
    transaction_transformer = TransactionTransformer()
    
    # Create writer and uploader
    parquet_writer = ParquetWriter(target_dir="Output_data")
    hdfs_uploader = HDFSUploader(hdfs_base_path="/data/banking")
    
    # Create file type detector
    file_type_detector = FileTypeDetector()
    
    # Create pipeline
    pipeline = Pipeline()
    pipeline.set_logger(logger)
    pipeline.set_error_handler(error_handler)
    pipeline.set_state_manager(state_manager)
    rejected_files_handler = RejectedFilesHandler(rejected_dir="Rejected_data")
    # Add initial components
    pipeline.add_component(listener)
    pipeline.add_component(extractor)
    pipeline.add_component(file_type_detector)
    pipeline.add_component(validator)
    pipeline.add_component(rejected_files_handler)
    
    # Dynamic transformer component (decides which transformer to use)
    pipeline.add_component(TransformerSelector([
        customer_transformer,
        credit_card_transformer,
        loan_transformer,
        support_transformer,
        transaction_transformer
    ]))
    
    # Output components
    pipeline.add_component(parquet_writer)
    #pipeline.add_component(hdfs_uploader)
    
    return pipeline


# Build the pipeline
pipeline = build_pipeline()

# Start the pipeline in listening mode
print("Starting pipeline in real-time mode. Press Ctrl+C to stop.")
try:
    pipeline.run()
except KeyboardInterrupt:
    print("Pipeline stopped by user.")