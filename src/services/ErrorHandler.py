class ErrorHandler:
    def __init__(self, logger, email_notifier):
        self.logger = logger
        self.email_notifier = email_notifier

    def handle(self, exception, context):
        pass