import unittest
from aws.api import CloudTrail
from aws.entity import Trail
from aws.api import S3
from aws.entity import S3BucketAcl

class LoggingLevel1(unittest.TestCase):
    def testCloudtrailEnabledForAllRegions(self):
        trailEnabledForAllRegions = False
        for trail in self._getTrails():
            trailEnabledForAllRegions = trailEnabledForAllRegions | trail.isMultiRegionTrail
        self.assertEqual(trailEnabledForAllRegions, True, "No multi-region trail defined. Recommendation: 2.1")

    def testCloudTrialsLogsAreIntegratedWithCloudWatch(self):
        trailsNotIntegratedWithCloudWatch = []
        cloudWatchNotUpdatedThreshold = 1
        for trail in self._getTrails():
            if not trail.cloudWatchUpdated(cloudWatchNotUpdatedThreshold):
                trailsNotIntegratedWithCloudWatch.append(trail)
        self.assertEqual([], trailsNotIntegratedWithCloudWatch, "Trail(s) without cloudwatch integration %s. Recommendation: 2.4" % self._trails(trailsNotIntegratedWithCloudWatch))

    def testCloudTrailValidationIsEnabled(self):
        trailsWithValidationDisabled = []
        for trail in self._getTrails():
            if not trail.logFileValidationEnabled:
                trailsWithValidationDisabled.append(trail)
        self.assertEqual([], trailsWithValidationDisabled, "Trail(s) with validation disabled: %s. Recommendation: 2.2" % self._trails(trailsWithValidationDisabled))

    def testCloudTrailLogsS3BucketIsNotPublic(self):
        trailsWithPublicS3Buckets = []
        for trail in self._getTrails():
            bucketName = trail.s3bucket
            bucketAcl = S3BucketAcl(S3().getBucketAcl(bucketName))
            if bucketAcl.allUsersHavePrivileges() | bucketAcl.allAuthenticatedUsersHavePrivileges():
                trailsWithPublicS3Buckets.append(trail)
        self.assertEqual([], trailsWithPublicS3Buckets, "Trail(s) with publicly accessible S3 buckets: %s. Recommendation: 2.3 ")

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
