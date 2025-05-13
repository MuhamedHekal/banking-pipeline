from src.transformers.loaders.TxtLoader import TxtLoader
class LoanTransformer(TxtLoader):
    def transform(self, data):
          pass



"""
if __name__ == "__main__":
    l= LoanTransformer()
    print(l.load_data('../incoming_data/2025-04-18/14/loans.txt')[0:2])
"""
