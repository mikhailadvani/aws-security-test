import datetime
from aws.api import CloudTrail

class Trail():
    def __init__(self, cloudTrailDict):
        self.isMultiRegionTrail = cloudTrailDict['IsMultiRegionTrail']
        self.logFileValidationEnabled = cloudTrailDict['LogFileValidationEnabled']
        self.name = cloudTrailDict['Name']
        self.s3bucket = cloudTrailDict['S3BucketName']

    def cloudWatchUpdated(self, hours):
        lastUpdated = str(CloudTrail().getTrailStatus(self.name)['LatestDeliveryTime'])
        now = str(datetime.datetime.now())
        timeSinceLastUpdate = self._parseDate(now) - self._parseDate(lastUpdated)
        return (timeSinceLastUpdate.seconds / 3600) <= hours

    def _parseDate(self, dateStr):
        timezoneSplit = dateStr.split('-')[0:3]
        timezoneRemovedTimestamp = "-".join(timezoneSplit)
        datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
        return datetime.datetime.strptime(timezoneRemovedTimestamp, datetimeFormat)
