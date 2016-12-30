import boto3
import time
from botocore.client import ClientError

class CloudWatch:
    def __init__(self):
        self.cloudWatch = boto3.client('cloudwatch')

    def getAlarms(self, metricName, namespace):
        return self._getAlarms(metricName, namespace, 1)

    def _getAlarms(self, metricName, namespace, sleepForIfFailed):
        alarms = []
        if sleepForIfFailed > 60:
            raise RuntimeError("Too many client errors")
        try:
            alarms = self.cloudWatch.describe_alarms_for_metric(MetricName=metricName, Namespace=namespace)
        except ClientError:
            time.sleep(sleepForIfFailed)
            self._getAlarms(metricName, namespace, sleepForIfFailed * 2)
        return alarms