import sys
import os
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
        
        if filename not in self.transformer_map:
            context.add_error(f"No transformer found for file: {filename}")
            return context
            
    
        return transformer.process(context)