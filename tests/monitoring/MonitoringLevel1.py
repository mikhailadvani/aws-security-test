import unittest

from aws.api import CloudTrail
from aws.entity import Trail
from aws.api import CloudWatchLogs
from aws.entity import LogMetricFilterSet

class MonitoringLevel1(unittest.TestCase):
    def testMetricFilterAndAlarmExistForUnauthorizedApiCalls(self):
        trailsWithoutAlarmsForUnauthorizedApiCalls = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined. Recommendation: 3.1")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
                continue
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.accessDeniedFilterAlarmOrSubscriberNotDefined() | metricFilters.unauthorizedOperationFilterAlarmOrSubscriberNotDefined():
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