import sys
import os
from src.transformers.CustomerTransformer import CustomerTransformer
from src.transformers.CreditCardTransformer import CreditCardTransformer
from src.transformers.LoanTransformer import LoanTransformer
from src.transformers.SupportTicketsTransformer import SupportTicketsTransformer
from src.transformers.TransactionTransformer import TransactionTransformer
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
sys.path.append(project_root)
from src.core.PipelineComponent import PipelineComponent

class TransformerSelector(PipelineComponent):
    def __init__(self, transformers):
        self.transformers = transformers
        self.transformer_map = self._build_transformer_map()
        
    def _build_transformer_map(self):
        """Build mapping from file names to transformers"""
        mapping = {
            "customer_profiles.csv": next((t for t in self.transformers 
                                          if isinstance(t, CustomerTransformer)), None),
            "credit_cards_billing.csv": next((t for t in self.transformers 
                                             if isinstance(t, CreditCardTransformer)), None),
            "support_tickets.csv": next((t for t in self.transformers 
                                        if isinstance(t, SupportTicketsTransformer)), None),
            "loans.txt": next((t for t in self.transformers 
                              if isinstance(t, LoanTransformer)), None),
            "transactions.json": next((t for t in self.transformers 
                                      if isinstance(t, TransactionTransformer)), None),
        }
        return mapping
        
    def process(self, context):
        if not context.file_path:
            context.add_error("No file path in context")
            return context
            
        filename = os.path.basename(context.file_path)
        transformer = self.transformer_map.get(filename)
        
        if not transformer:
            context.add_error(f"No transformer found for file: {filename}")
            return context
        
        # Load data if needed
        if hasattr(transformer, 'load_data') and context.data is None:
            context.data = transformer.load_data(context.file_path)
        
        # Transform data and update context
        if hasattr(transformer, 'transform') and context.data is not None:
            context.data = transformer.transform(context.data)
        
        return context