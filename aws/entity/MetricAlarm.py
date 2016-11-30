class MetricAlarm:
    def __init__(self, metricAlarmDict):
        self.name = metricAlarmDict['AlarmName']
        self.actions = metricAlarmDict['AlarmActions']