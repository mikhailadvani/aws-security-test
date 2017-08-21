import unittest
from aws.api import CloudTrail
from aws.entity import Trail
from aws.api import S3
from aws.entity import S3BucketAcl
from aws.entity import S3BucketPolicy
from aws.entity import S3BucketLogging
from aws.api import KMS
from aws.entity import KMSKey

class LoggingAudit(unittest.TestCase):
    def testCloudtrailEnabledForAllRegions(self):
        trailEnabledForAllRegions = False
        for trail in self._getTrails():
            trailEnabledForAllRegions = trailEnabledForAllRegions | trail.isMultiRegionTrail
        self.assertEqual(trailEnabledForAllRegions, True, "No multi-region trail defined.")

    def testCloudTrailValidationIsEnabled(self):
        trailsWithValidationDisabled = []
        for trail in self._getTrails():
            if not trail.logFileValidationEnabled:
                trailsWithValidationDisabled.append(trail)
        self.assertEqual([], trailsWithValidationDisabled, "Trail(s) with validation disabled: %s." % self._trails(trailsWithValidationDisabled))

    def testCloudTrailLogsS3BucketIsNotPublic(self):
        trailsWithPublicS3Buckets = []
        for trail in self._getTrails():
            bucketName = trail.s3bucket
            bucketAcl = S3BucketAcl(S3().getBucketAcl(bucketName))
            bucketPolicy = S3BucketPolicy(S3().getBucketPolicy(bucketName))
            if (bucketAcl.allUsersHavePrivileges() | bucketAcl.allAuthenticatedUsersHavePrivileges() | bucketPolicy.allowsAccessForAllPrincipals()):
                trailsWithPublicS3Buckets.append(trail)
        self.assertEqual([], trailsWithPublicS3Buckets, "Trail(s) with publicly accessible S3 buckets: %s." % self._trails(trailsWithPublicS3Buckets))

    def testCloudTrialsLogsAreIntegratedWithCloudWatch(self):
        trailsNotIntegratedWithCloudWatch = []
        cloudWatchNotUpdatedThreshold = 24
        for trail in self._getTrails():
            if not trail.cloudWatchUpdated(cloudWatchNotUpdatedThreshold):
                trailsNotIntegratedWithCloudWatch.append(trail)
        self.assertEqual([], trailsNotIntegratedWithCloudWatch, "Trail(s) without cloudwatch integration %s." % self._trails(trailsNotIntegratedWithCloudWatch))

    def testCloudTrailLogsS3BucketHasAccessLoggingEnabled(self):
        trailsWithPublicS3BucketsWithoutLogging = []
        for trail in self._getTrails():
            bucketName = trail.s3bucket
            if not S3BucketLogging(S3().getBucketLogging(bucketName)).loggingEnabled:
                trailsWithPublicS3BucketsWithoutLogging.append(trail)
        self.assertEqual([], trailsWithPublicS3BucketsWithoutLogging, "Trail(s) with S3 buckets without access logging enabled: %s." % self._trails(trailsWithPublicS3BucketsWithoutLogging))

    def testCloudTrailLogsAreEncrypted(self):
        trailsWithoutEncryption = []
        for trail in self._getTrails():
            if not trail.encrypted:
                trailsWithoutEncryption.append(trail)
        self.assertEqual([], trailsWithoutEncryption, "Trail(s) without KMS encryption on S3: %s." % self._trails(trailsWithoutEncryption))

    def testCustomerCreatedCMKKeysAreRotationEnabled(self):
        keysWithoutRotationEnabled = []
        for key in self._getCMKKeys():
            if key.enabled & (not key.rotationEnabled):
                keysWithoutRotationEnabled.append(key)
        self.assertEqual([], keysWithoutRotationEnabled, "CMK key(s) without rotation enabled: %s." % self._getCMKKeyIds(keysWithoutRotationEnabled))

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

    def _getCMKKeys(self):
        keys = []
        for key in KMS().getKeys()['Keys']:
            keys.append(KMSKey(key))
        return keys

    def _getCMKKeyIds(self, keys):
        keyIds = []
        for key in keys:
            keyIds.append(key.id)
        return ",".join(keyIds)
