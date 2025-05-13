from src.transformers.loaders.CsvLoader import CsvLoader
class CustomerTransformer(CsvLoader):
     def transform(self, data):
          pass
     

"""
if __name__ == "__main__":
    l= CustomerTransformer()
    print(l.load_data('../incoming_data/2025-04-18/14/customer_profiles.csv')[0]['customer_id'])
"""