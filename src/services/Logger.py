import os
from datetime import datetime

class Logger:
    def __init__(self, log_file='log/log.txt'):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

    def log(self, message):
        timestamp = datetime.now().isoformat()
        log_entry = f"{timestamp} => {message}"
        self.write_log(log_entry)
        return log_entry

    def write_log(self, log_entry):
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')


# def main():
#     logger = Logger()  # Default path is 'log/log.txt'
    
#     logger.log("Application started")
#     logger.log("Processing data...")
#     logger.log("Application finished")

#     print("Log entries written successfully.")

# if __name__ == "__main__":
#     main()
        