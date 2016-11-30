import boto3

class CloudWatch:
    def __init__(self):
        self.cloudWatch = boto3.client('cloudwatch')

    def getAlarms(self, metricNames):
        return self.cloudWatch.describe_alarms(AlarmNames=metricNames)