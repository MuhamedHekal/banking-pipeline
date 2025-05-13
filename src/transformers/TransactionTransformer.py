from src.transformers.loaders.JsonLoader import JsonLoader
class TransactionTransformer(JsonLoader):
    def transform(self, data):
          pass



if __name__ == "__main__":
    l= TransactionTransformer()
    print(l.load_data('../incoming_data/2025-04-18/14/transactions.json')[0])