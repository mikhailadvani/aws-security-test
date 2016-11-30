import unittest

from aws.api import CloudTrail
from aws.entity import Trail
from aws.api import CloudWatchLogs
from aws.entity import LogMetricFilter
from aws.api import CloudWatch
from aws.entity import MetricAlarm
from aws.api import SNS

class MonitoringLevel1(unittest.TestCase):
    def testMetricFilterAndAlarmExistForUnauthorizedApiCalls(self):
        trailsWithoutAlarmsForUnauthorizedApiCalls = []
        for trail in self._getTrails():
            cloudWatchLogGroup = CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)
            if cloudWatchLogGroup is None:
                trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
            else:
                metricFilters = cloudWatchLogGroup['metricFilters']
                if metricFilters == []:
                    trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
                else:
                    for metricFilter in metricFilters:
                        logMetricFilter = LogMetricFilter(metricFilter)
                        if (not logMetricFilter.unauthorizedOperationFilterDefined()) | (not logMetricFilter.accessDeniedFilterDefined()):
                            trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
                        else:
                            metricAlarms = CloudWatch().getAlarms(logMetricFilter.metricNames)['MetricAlarms']
                            if metricAlarms == []:
                                trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
                            else:
                                for metricAlarm in metricAlarms:
                                    alarm = MetricAlarm(metricAlarm)
                                    if alarm.actions is []:
                                        trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
                                    else:
                                        for snsTopicArn in alarm.actions:
                                            subscriptions = SNS().getSubscriptions(snsTopicArn)['Subscriptions']
                                            if subscriptions == []:
                                                trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForUnauthorizedApiCalls, 'Trail(s) without alarms for unauthorized API calls: %s. Recommendation: 3.1' % self._trails(trailsWithoutAlarmsForUnauthorizedApiCalls))

    def _getTrails(self):
        trails = []
        for cloudTrail in CloudTrail().getTrails()['trailList']:
            trails.append(Trail(cloudTrail))
        return trails

    def _trails(self, cloudtrails):
        trails = []
        for cloudtrail in cloudtrails:
            trails.append(cloudtrail.name)
        return ",".join(trails)