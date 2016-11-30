class LogMetricFilter:
    def __init__(self, logMetricFilterDict):
        self.name = logMetricFilterDict['filterName']
        self.filterPattern = logMetricFilterDict['filterPattern'].replace(' ', '')
        self.metricNames = self._getMetricNames(logMetricFilterDict)

    def unauthorizedOperationFilterDefined(self):
        return self._checkFilterDefined('$.errorCode="*UnauthorizedOperation"')

    def accessDeniedFilterDefined(self):
        return self._checkFilterDefined('$.errorCode="AccessDenied*')

    def _checkFilterDefined(self, filterString):
        if filterString in self.filterPattern:
            return True
        else:
            return False

    def _getMetricNames(self, logMetricFilterDict):
        metricNames = []
        for metricName in logMetricFilterDict['metricTransformations']:
            metricNames.append(metricName['metricName'])
        return metricNames
