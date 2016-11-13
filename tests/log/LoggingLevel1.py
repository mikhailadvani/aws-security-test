import unittest
from aws.api import CloudTrail
from aws.entity import Trail

class LoggingLevel1(unittest.TestCase):
    def testCloudtrailEnabledForAllRegions(self):
        trailEnabledForAllRegions = False
        for trail in self._getTrails():
            trailEnabledForAllRegions = trailEnabledForAllRegions | trail.isMultiRegionTrail
        self.assertEqual(trailEnabledForAllRegions, True, "No multi-region trail defined")

    def testCloudTrialsLogsAreIntegratedWithCloudWatch(self):
        trailsNotIntegratedWithCloudWatch = []
        cloudWatchNotUpdatedThreshold = 1
        for trail in self._getTrails():
            if not trail.cloudWatchUpdated(cloudWatchNotUpdatedThreshold):
                trailsNotIntegratedWithCloudWatch.append(trail)
        self.assertEqual([], trailsNotIntegratedWithCloudWatch, "Trail(s) without cloudwatch integration %s" % self._trails(trailsNotIntegratedWithCloudWatch))

    def testCloudTrailValidationIsEnabled(self):
        trailsWithValidationDisabled = []
        for trail in self._getTrails():
            if not trail.logFileValidationEnabled:
                trailsWithValidationDisabled.append(trail)
        self.assertEqual([], trailsWithValidationDisabled, "Trail(s) with validation disabled: %s" % self._trails(trailsWithValidationDisabled))

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
