import unittest

from aws.api import CloudTrail
from aws.entity import Trail
from aws.api import CloudWatchLogs
from aws.entity import LogMetricFilterSet
from aws.api import SNS
from aws.entity import Subscriber

class MonitoringAudit(unittest.TestCase):
    def testMetricFilterAndAlarmExistForUnauthorizedApiCalls(self):
        trailsWithoutAlarmsForUnauthorizedApiCalls = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.unauthorizedApiCallFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForUnauthorizedApiCalls.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForUnauthorizedApiCalls, 'Trail(s) without alarms for unauthorized API calls: %s.' % self._trails(trailsWithoutAlarmsForUnauthorizedApiCalls))

    def testMetricFilterAndAlarmExistForLoginWithoutMfa(self):
        trailsWithoutAlarmsForLoginWithoutMfa = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForLoginWithoutMfa.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.loginWithoutMfaFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForLoginWithoutMfa.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForLoginWithoutMfa, 'Trail(s) without alarms for web console login without MFA: %s.' % self._trails(trailsWithoutAlarmsForLoginWithoutMfa))

    def testMetricFilterAndAlarmExistForRootLogin(self):
        trailsWithoutAlarmsForRootLogin = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForRootLogin.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.rootLoginFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForRootLogin.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForRootLogin, 'Trail(s) without alarms for root login: %s.' % self._trails(trailsWithoutAlarmsForRootLogin))

    def testMetricFilterAndAlarmExistForIamPolicyChanges(self):
        trailsWithoutAlarmsForIamPolicyChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForIamPolicyChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.iamPolicyChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForIamPolicyChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForIamPolicyChanges, 'Trail(s) without alarms for IAM policy changes: %s.' % self._trails(trailsWithoutAlarmsForIamPolicyChanges))

    def testMetricFilterAndAlarmExistForCloudtrailConfigChanges(self):
        trailsWithoutAlarmsForCloudtrailConfigChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForCloudtrailConfigChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.cloudtrailConfigChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForCloudtrailConfigChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForCloudtrailConfigChanges, 'Trail(s) without alarms for cloudtrail config changes: %s.' % self._trails(trailsWithoutAlarmsForCloudtrailConfigChanges))

    def testMetricFilterAndAlarmExistForConsoleAuthFailure(self):
        trailsWithoutAlarmsForConsoleAuthFailures = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForConsoleAuthFailures.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.consoleAuthFailureFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForConsoleAuthFailures.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForConsoleAuthFailures, 'Trail(s) without alarms for web console auth failures: %s.' % self._trails(trailsWithoutAlarmsForConsoleAuthFailures))

    def testMetricFilterAndAlarmExistForS3PolicyChanges(self):
        trailsWithoutAlarmsForS3PolicyChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForS3PolicyChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.s3PolicyChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForS3PolicyChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForS3PolicyChanges, 'Trail(s) without alarms for S3 policy changes: %s.' % self._trails(trailsWithoutAlarmsForS3PolicyChanges))

    def testMetricFilterAndAlarmExistForSecurityGroupChanges(self):
        trailsWithoutAlarmsForSecurityGroupChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForSecurityGroupChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.securityGroupChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForSecurityGroupChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForSecurityGroupChanges, 'Trail(s) without alarms for security group changes: %s.' % self._trails(trailsWithoutAlarmsForSecurityGroupChanges))

    def testMetricFilterAndAlarmExistForNetworkAclChanges(self):
        trailsWithoutAlarmsForNetworkAclChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForNetworkAclChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.networkAclChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForNetworkAclChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForNetworkAclChanges, 'Trail(s) without alarms for network acl changes: %s.' % self._trails(trailsWithoutAlarmsForNetworkAclChanges))

    def testMetricFilterAndAlarmExistForNetworkGatewayChanges(self):
        trailsWithoutAlarmsForNetworkGatewayChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForNetworkGatewayChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.networkGatewayChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForNetworkGatewayChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForNetworkGatewayChanges, 'Trail(s) without alarms for network gateway changes: %s.' % self._trails(trailsWithoutAlarmsForNetworkGatewayChanges))

    def testMetricFilterAndAlarmExistForRouteTableChanges(self):
        trailsWithoutAlarmsForRouteTableChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForRouteTableChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.routeTableChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForRouteTableChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForRouteTableChanges, 'Trail(s) without alarms for route table changes: %s.' % self._trails(trailsWithoutAlarmsForRouteTableChanges))

    def testMetricFilterAndAlarmExistForVpcChanges(self):
        trailsWithoutAlarmsForVpcChanges = []
        trails = self._getTrails()
        self.assertNotEqual([], trails, "No trails defined.")
        for trail in trails:
            if trail.cloudWatchLogGroup is None:
                trailsWithoutAlarmsForVpcChanges.append(trail)
            else:
                metricFilters = LogMetricFilterSet(CloudWatchLogs().getMetricFilters(trail.cloudWatchLogGroup)['metricFilters'])
                if metricFilters.vpcChangeFilterAlarmOrSubscriberNotDefined():
                    trailsWithoutAlarmsForVpcChanges.append(trail)
        self.assertEqual([], trailsWithoutAlarmsForVpcChanges, 'Trail(s) without alarms for VPC changes: %s.' % self._trails(trailsWithoutAlarmsForVpcChanges))

    def testSNSTopicsHaveAppropriateSubscribers(self):
        file = open('artifacts/sns_subscribers.csv', 'w')
        file.write("Topic Owner, Subscription ID, Protocol, Endpoint, Subscriber (Account ID)")
        for subscription in SNS().getAllSubscriptions()['Subscriptions']:
            file.write(Subscriber(subscription).getCsv())

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