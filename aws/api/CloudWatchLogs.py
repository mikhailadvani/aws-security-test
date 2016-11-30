import boto3

class CloudWatchLogs:
    def __init__(self):
        self.logs = boto3.client('logs')

    def getMetricFilters(self, logGroupName):
        return self.logs.describe_metric_filters(logGroupName=logGroupName)