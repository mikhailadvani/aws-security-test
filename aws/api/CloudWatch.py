import boto3

class CloudWatch:
    def __init__(self):
        self.cloudWatch = boto3.client('cloudwatch')

    def getAlarms(self, metricName, namespace):
        return self.cloudWatch.describe_alarms_for_metric(MetricName=metricName, Namespace=namespace)