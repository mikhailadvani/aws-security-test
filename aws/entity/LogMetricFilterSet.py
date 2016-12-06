from aws.entity import LogMetricFilter

class LogMetricFilterSet():
    def __init__(self, metricFilters):
        self.filters = []
        for filter in metricFilters:
            self.filters.append(LogMetricFilter(filter))

    def unauthorizedApiCallFilterAlarmOrSubscriberNotDefined(self):
        unauthorizedOperationFilters = self._unauthorizedOperationFilters()
        unauthorizedOperationAlarmDefined = self._alarmsWithSubscribers(unauthorizedOperationFilters)
        unauthorizedOperationFilterAlarmOrSubscriberNotDefined = (unauthorizedOperationFilters == []) | (not unauthorizedOperationAlarmDefined)
        accessDeniedFilters = self._accessDeniedFilters()
        accessDeniedAlarmDefined = self._alarmsWithSubscribers(accessDeniedFilters)
        accessDeniedFilterAlarmOrSubscriberNotDefined = (accessDeniedFilters == []) | (not accessDeniedAlarmDefined)
        return unauthorizedOperationFilterAlarmOrSubscriberNotDefined | accessDeniedFilterAlarmOrSubscriberNotDefined

    def loginWithoutMfaFilterAlarmOrSubscriberNotDefined(self):
        loginWithoutMfaFilters = self._loginWithoutMfaFilters()
        loginWithoutMfaAlarmDefined = self._alarmsWithSubscribers(loginWithoutMfaFilters)
        return (loginWithoutMfaFilters == []) | (not loginWithoutMfaAlarmDefined)

    def rootLoginFilterAlarmOrSubscriberNotDefined(self):
        rootLoginFilters = self._rootLoginFilters()
        rootLoginAlarmDefined = self._alarmsWithSubscribers(rootLoginFilters)
        return (rootLoginFilters == []) | (not rootLoginAlarmDefined)

    def iamPolicyChangeFilterAlarmOrSubscriberNotDefined(self):
        policyChangeEvents = ['DeleteGroupPolicy', 'DeleteRolePolicy', 'DeleteUserPolicy', 'PutGroupPolicy', 'PutRolePolicy', 'PutUserPolicy',
                               'CreatePolicy', 'DeletePolicy', 'CreatePolicyVersion', 'DeletePolicyVersion', 'AttachRolePolicy', 'DetachRolePolicy',
                               'AttachUserPolicy', 'DetachUserPolicy', 'AttachGroupPolicy', 'DetachGroupPolicy']
        iamPolicyChangeFiltersAlarmOrSubscriberNotDefined = False
        for policyChangeEvent in policyChangeEvents:
            iamPolicyChangeFilters = self._eventSpecificChangeFilters(policyChangeEvent)
            iamPolicyChangeAlarmDefined = self._alarmsWithSubscribers(iamPolicyChangeFilters)
            iamPolicyChangeFiltersAlarmOrSubscriberNotDefined = (iamPolicyChangeFilters == []) | (not iamPolicyChangeAlarmDefined)
        return iamPolicyChangeFiltersAlarmOrSubscriberNotDefined

    def cloudtrailConfigChangeFilterAlarmOrSubscriberNotDefined(self):
        configChangeEvents = ['CreateTrail', 'UpdateTrail', 'DeleteTrail', 'StartLogging', 'StopLogging']
        cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined = False
        for configChangeEvent in configChangeEvents:
            cloudtrailConfigChangeFilters = self._eventSpecificChangeFilters(configChangeEvent)
            cloudtrailConfigChangeAlarmDefined = self._alarmsWithSubscribers(cloudtrailConfigChangeFilters)
            cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined = (cloudtrailConfigChangeFilters == []) | (not cloudtrailConfigChangeAlarmDefined)
        return cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined

    def networkGatewayChangeFilterAlarmOrSubscriberNotDefined(self):
        networkGatewayChangeEvents = ['CreateCustomerGateway', 'DeleteCustomerGateway', 'AttachInternetGateway', 'CreateInternetGateway',
                                      'DeleteInternetGateway', 'DetachInternetGateway']
        networkGatewayChangeFiltersAlarmOrSubscriberNotDefined = False
        for networkGatewayChangeEvent in networkGatewayChangeEvents:
            networkGatewayChangeFilters = self._eventSpecificChangeFilters(networkGatewayChangeEvent)
            networkGatewayChangeAlarmDefined = self._alarmsWithSubscribers(networkGatewayChangeFilters)
            networkGatewayChangeFiltersAlarmOrSubscriberNotDefined = (networkGatewayChangeFilters == []) | (not networkGatewayChangeAlarmDefined)
        return networkGatewayChangeFiltersAlarmOrSubscriberNotDefined

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

    def _rootLoginFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isRootLoginFilter():
                filters.append(filter)
        return filters

    def _eventSpecificChangeFilters(self, changeEvent):
        filters = []
        for filter in self.filters:
            if filter.isEventNameSpecificFilter(changeEvent):
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
