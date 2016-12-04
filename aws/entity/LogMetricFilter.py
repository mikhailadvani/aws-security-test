import aws.entity.MetricAlarm
import aws.api.SNS
import aws.api.CloudWatch

class LogMetricFilter:
    def __init__(self, logMetricFilterDict):
        self.name = logMetricFilterDict['filterName']
        self.filterPattern = logMetricFilterDict['filterPattern'].replace(' ', '')
        self.metricTransformations = logMetricFilterDict['metricTransformations']

    def isUnauthorizedOperationFilter(self):
        return self._checkFilterIs('$.errorCode="*UnauthorizedOperation"')

    def isAccessDeniedFilter(self):
        return self._checkFilterIs('$.errorCode="AccessDenied*')

    def isLoginWithoutMfaFilter(self):
        return self._checkFilterIs('$.userIdentity.sessionContext.attributes.mfaAuthenticated!="true"')

    def fetchAlarmsWithSubscribers(self):
        metricAlarms = []
        for metricTransformation in self.metricTransformations:
            cloudwatchAlarm = aws.api.CloudWatch().getAlarms(metricTransformation['metricName'], metricTransformation['metricNamespace'])['MetricAlarms']
            metricAlarms = metricAlarms + cloudwatchAlarm
        self.alarms = []
        for metricAlarmDict in metricAlarms:
            alarm = aws.entity.MetricAlarm(metricAlarmDict)
            if alarm.actions != []:
                for action in alarm.actions:
                    subscriptions = aws.api.SNS().getSubscriptions(action)['Subscriptions']
                    if subscriptions != []:
                        self.alarms.append(aws.entity.MetricAlarm(metricAlarmDict))

    def _checkFilterIs(self, filterString):
        if filterString in self.filterPattern:
            return True
        else:
            return False
