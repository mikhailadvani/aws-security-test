import datetime
from dateutil.parser import parse
import re
from aws.api import CloudTrail

class Trail():
    def __init__(self, cloudTrailDict):
        self.isMultiRegionTrail = cloudTrailDict['IsMultiRegionTrail']
        self.logFileValidationEnabled = cloudTrailDict['LogFileValidationEnabled']
        self.name = cloudTrailDict['Name']
        self.s3bucket = cloudTrailDict['S3BucketName']
        self.encrypted = ('KmsKeyId' in cloudTrailDict)
        if 'CloudWatchLogsLogGroupArn' in cloudTrailDict:
            self.cloudwatchLogsIntegrated = True
            self.cloudWatchLogGroup = re.search(':log-group:(.+?):\*', cloudTrailDict['CloudWatchLogsLogGroupArn']).group(1)
        else:
            self.cloudwatchLogsIntegrated = False
            self.cloudWatchLogGroup = None

    def cloudWatchUpdated(self, hours):
        lastUpdated = str(CloudTrail().getTrailStatus(self.name)['LatestDeliveryTime'])
        now = str(datetime.datetime.now()) + "+00:00"
        timeSinceLastUpdate = parse(now) - parse(lastUpdated)
        return (timeSinceLastUpdate.seconds / 3600) <= hours
