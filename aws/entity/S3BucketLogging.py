class S3BucketLogging:
    def __init__(self, loggingDict):
        if 'LoggingEnabled' in loggingDict:
            self.loggingEnabled = True
        else:
            self.loggingEnabled = False