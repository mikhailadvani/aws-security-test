import boto3

class CloudTrail:
    def __init__(self):
        self.cloudTrail = boto3.client('cloudtrail')

    def getTrails(self):
        return self.cloudTrail.describe_trails()

    def getTrailStatus(self, name):
        return self.cloudTrail.get_trail_status(Name=name)