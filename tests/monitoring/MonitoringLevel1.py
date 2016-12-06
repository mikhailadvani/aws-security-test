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
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.unauthorizedApiCallFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForUnauthorizedApiCalls, 'Trail(s) without alarms for unauthorized API calls: %s. Recommendation: 3.1' % self._trails(trailsWithoutAlarmsForUnauthorizedApiCalls))

    def testMetricFilterAndAlarmExistForLoginWithoutMfa(self):
        trailsWithoutAlarmsForLoginWithoutMfa = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined. Recommendation: 3.2")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForLoginWithoutMfa.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.loginWithoutMfaFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForLoginWithoutMfa.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForLoginWithoutMfa, 'Trail(s) without alarms for web console login without MFA: %s. Recommendation: 3.2' % self._trails(trailsWithoutAlarmsForLoginWithoutMfa))

    def testMetricFilterAndAlarmExistForRootLogin(self):
        trailsWithoutAlarmsForRootLogin = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined. Recommendation: 3.3")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForRootLogin.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.rootLoginFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForRootLogin.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForRootLogin, 'Trail(s) without alarms for root login: %s. Recommendation: 3.3' % self._trails(trailsWithoutAlarmsForRootLogin))

    def testMetricFilterAndAlarmExistForIamPolicyChanges(self):
        trailsWithoutAlarmsForIamPolicyChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined. Recommendation: 3.4")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForIamPolicyChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.iamPolicyChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForIamPolicyChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForIamPolicyChanges, 'Trail(s) without alarms for IAM policy chnages: %s. Recommendation: 3.4' % self._trails(trailsWithoutAlarmsForIamPolicyChanges))

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