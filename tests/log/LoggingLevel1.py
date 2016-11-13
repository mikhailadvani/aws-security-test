import unittest
from aws.api import CloudTrail
from aws.entity import Trail

class LoggingLevel1(unittest.TestCase):
    def testCloudtrailEnabledForAllRegions(self):
        trailEnabledForAllRegions = False
        for cloudTrail in CloudTrail().getTrails()['trailList']:
            trailEnabledForAllRegions = trailEnabledForAllRegions | Trail(cloudTrail).isMultiRegionTrail
        self.assertEqual(trailEnabledForAllRegions, True, "No multi-region trail defined")