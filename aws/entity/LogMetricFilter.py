import aws.entity.MetricAlarm
import aws.api.SNS
import aws.api.CloudWatch
import re
import itertools

class LogMetricFilter:
    def __init__(self, logMetricFilterDict):
        self.name = logMetricFilterDict['filterName']
        self.filterPattern = logMetricFilterDict['filterPattern']
        self.metricTransformations = logMetricFilterDict['metricTransformations']

    def isUnauthorizedOperationFilter(self):
        return self._checkFilterIs('\s*({?)\s*(\(?)\$.errorCode\s*=\s*\"\*UnauthorizedOperation\"\s*(\)?)\s*(}?)\s*')

    def isAccessDeniedFilter(self):
        return self._checkFilterIs('\s*({?)\s*(\(?)\$.errorCode\s*=\s*\"AccessDenied\*\"\s*(\)?)\s*(}?)\s*')

    def isRootLoginFilter(self):
        isFilter = False
        regexes = ['\s*\$.userIdentity.type\s*=\s*\"Root\"\s*', '\s*\$.userIdentity.invokedBy\s+NOT\s+EXISTS\s+', '\s*\$.eventType\s*!=\s*\"AwsServiceEvent\"\s*']
        appendString = '&&'
        filterStringCombinations = list(itertools.permutations(regexes))
        for filterStringCombination in filterStringCombinations:
            isFilter = isFilter | self._checkFilterIs(appendString.join(filterStringCombination))
        return isFilter

    def isEventNameSpecificFilter(self, configChangeEvent):
        regex = '(\(?)\s*\$.eventName\s*=\s*("?)%s("?)\s*(\)?)'
        return self._checkFilterIs(regex % configChangeEvent)

    def isCombinationOfTwoFilters(self, filter1Key, filter1Value, filter2Key, filter2Value, operator1='=', operator2='='):
        regexForFilter1 = '(\(?)\s*\$.%s\s*%s\s*("?)%s("?)(\)?)' % (filter1Key, operator1, filter1Value)
        regexForFilter2 = '(\(?)\s*\$.%s\s*%s\s*("?)%s("?)(\)?)' % (filter2Key, operator2, filter2Value)
        combinedRegex1 = '(\(?)%s(\)?)\s*&&.*(\(?)%s(\)?)' % (regexForFilter1, regexForFilter2)
        combinedRegex2 = '(\(?)%s(\)?)\s*&&.*(\(?)%s(\)?)' % (regexForFilter2, regexForFilter1)
        return self._checkFilterIs(combinedRegex1) | self._checkFilterIs(combinedRegex2)

    def fetchAlarmsWithSubscribers(self):
        metricAlarms = []
        for metricTransformation in self.metricTransformations:
            cloudwatchAlarm = aws.api.CloudWatch().getAlarms(metricTransformation['metricName'], metricTransformation['metricNamespace'])['MetricAlarms']
            metricAlarms = metricAlarms + cloudwatchAlarm
        self.alarms = []
        for metricAlarmDict in metricAlarms:
            alarm = aws.entity.MetricAlarm(metricAlarmDict)
            if alarm.actions != []:
                for action in alarm.actions:
                    subscriptions = aws.api.SNS().getSubscriptions(action)['Subscriptions']
                    if subscriptions != []:
                        self.alarms.append(aws.entity.MetricAlarm(metricAlarmDict))

    def _checkFilterIs(self, filterRegex):
        occurences = re.findall(filterRegex, self.filterPattern)
        if occurences != []:
            return True
        else:
            return False
