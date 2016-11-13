class Trail():
    def __init__(self, cloudTrailDict):
        self.isMultiRegionTrail = cloudTrailDict['IsMultiRegionTrail']
        self.logFileValidationEnabled = cloudTrailDict['LogFileValidationEnabled']
        self.name = cloudTrailDict['Name']
