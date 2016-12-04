from aws.entity import LogMetricFilter

class LogMetricFilterSet():
    def __init__(self, metricFilters):
        self.filters = []
        for filter in metricFilters:
            self.filters.append(LogMetricFilter(filter))

    def unauthorizedOperationFilterAlarmOrSubscriberNotDefined(self):
        unauthorizedOperationFilters = self._unauthorizedOperationFilters()
        unauthorizedOperationAlarmDefined = self._alarmsWithSubscribers(unauthorizedOperationFilters)
        return (unauthorizedOperationFilters == []) | (not unauthorizedOperationAlarmDefined)

    def accessDeniedFilterAlarmOrSubscriberNotDefined(self):
        accessDeniedFilters = self._accessDeniedFilters()
        accessDeniedAlarmDefined = self._alarmsWithSubscribers(accessDeniedFilters)
        return (accessDeniedFilters == []) | (not accessDeniedAlarmDefined)

    def loginWithoutMfaFilterAlarmOrSubscriberNotDefined(self):
        loginWithoutMfaFilters = self._loginWithoutMfaFilters()
        loginWithoutMfaAlarmDefined = self._alarmsWithSubscribers(loginWithoutMfaFilters)
        return (loginWithoutMfaFilters == []) | (not loginWithoutMfaAlarmDefined)

    def _unauthorizedOperationFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isUnauthorizedOperationFilter():
                filters.append(filter)
        return filters

    def _accessDeniedFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isAccessDeniedFilter():
                filters.append(filter)
        return filters

    def _loginWithoutMfaFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isLoginWithoutMfaFilter():
                filters.append(filter)
        return filters

    def _alarmsWithSubscribers(self, filters):
        alarms = 0
        for filter in filters:
            filter.fetchAlarmsWithSubscribers()
            alarms = alarms + len(filter.alarms)
        return alarms != 0

    def _filtersDefined(self):
        return not self.filters == []
