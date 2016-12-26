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

    def consoleAuthFailureFilterAlarmOrSubscriberNotDefined(self):
        consoleAuthFailureFilters = self._consoleAuthFailureFilters()
        consoleAuthFailureAlarmDefined = self._alarmsWithSubscribers(consoleAuthFailureFilters)
        return (consoleAuthFailureFilters == []) | (not consoleAuthFailureAlarmDefined)

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
            iamPolicyChangeFilters = self._eventNameFilters(policyChangeEvent)
            iamPolicyChangeAlarmDefined = self._alarmsWithSubscribers(iamPolicyChangeFilters)
            iamPolicyChangeFiltersAlarmOrSubscriberNotDefined = (iamPolicyChangeFilters == []) | (not iamPolicyChangeAlarmDefined)
        return iamPolicyChangeFiltersAlarmOrSubscriberNotDefined

    def cloudtrailConfigChangeFilterAlarmOrSubscriberNotDefined(self):
        configChangeEvents = ['CreateTrail', 'UpdateTrail', 'DeleteTrail', 'StartLogging', 'StopLogging']
        cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined = False
        for configChangeEvent in configChangeEvents:
            cloudtrailConfigChangeFilters = self._eventNameFilters(configChangeEvent)
            cloudtrailConfigChangeAlarmDefined = self._alarmsWithSubscribers(cloudtrailConfigChangeFilters)
            cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined = (cloudtrailConfigChangeFilters == []) | (not cloudtrailConfigChangeAlarmDefined)
        return cloudtrailConfigChangeFiltersAlarmOrSubscriberNotDefined

    def s3PolicyChangeFilterAlarmOrSubscriberNotDefined(self):
        s3PolicyChangeEvents = ['PutBucketAcl', 'PutBucketPolicy', 'PutBucketCors', 'PutBucketLifecycle', 'PutBucketReplication',
                                'DeleteBucketPolicy', 'DeleteBucketCors', 'DeleteBucketLifecycle', 'DeleteBucketReplication']
        s3PolicyChangeFiltersAlarmOrSubscriberNotDefined = False
        for s3PolicyChangeEvent in s3PolicyChangeEvents:
            s3PolicyChangeFilters = self._twoFilterCombination('eventSource','s3.amazonaws.com', 'eventName', s3PolicyChangeEvent)
            s3PolicyChangeAlarmDefined = self._alarmsWithSubscribers(s3PolicyChangeFilters)
            s3PolicyChangeFiltersAlarmOrSubscriberNotDefined = (s3PolicyChangeFilters == []) | (not s3PolicyChangeAlarmDefined)
        return s3PolicyChangeFiltersAlarmOrSubscriberNotDefined

    def securityGroupChangeFilterAlarmOrSubscriberNotDefined(self):
        securityGroupChangeEvents = ['AuthorizeSecurityGroupIngress', 'AuthorizeSecurityGroupEgress', 'RevokeSecurityGroupIngress',
                                     'RevokeSecurityGroupEgress', 'CreateSecurityGroup', 'DeleteSecurityGroup']
        securityGroupChangeFiltersAlarmOrSubscriberNotDefined = False
        for securityGroupChangeEvent in securityGroupChangeEvents:
            securityGroupChangeFilters = self._eventNameFilters(securityGroupChangeEvent)
            securityGroupChangeAlarmDefined = self._alarmsWithSubscribers(securityGroupChangeFilters)
            securityGroupChangeFiltersAlarmOrSubscriberNotDefined = (securityGroupChangeFilters == []) | (not securityGroupChangeAlarmDefined)
        return securityGroupChangeFiltersAlarmOrSubscriberNotDefined

    def networkAclChangeFilterAlarmOrSubscriberNotDefined(self):
        networkAclChangeEvents = ['CreateNetworkAcl', 'CreateNetworkAclEntry', 'DeleteNetworkAcl', 'DeleteNetworkAclEntry',
                                  'ReplaceNetworkAclEntry', 'ReplaceNetworkAclAssociation']
        networkAclChangeFiltersAlarmOrSubscriberNotDefined = False
        for networkAclChangeEvent in networkAclChangeEvents:
            networkAclChangeFilters = self._eventNameFilters(networkAclChangeEvent)
            networkAclChangeAlarmDefined = self._alarmsWithSubscribers(networkAclChangeFilters)
            networkAclChangeFiltersAlarmOrSubscriberNotDefined = (networkAclChangeFilters == []) | (not networkAclChangeAlarmDefined)
        return networkAclChangeFiltersAlarmOrSubscriberNotDefined

    def networkGatewayChangeFilterAlarmOrSubscriberNotDefined(self):
        networkGatewayChangeEvents = ['CreateCustomerGateway', 'DeleteCustomerGateway', 'AttachInternetGateway', 'CreateInternetGateway',
                                      'DeleteInternetGateway', 'DetachInternetGateway']
        networkGatewayChangeFiltersAlarmOrSubscriberNotDefined = False
        for networkGatewayChangeEvent in networkGatewayChangeEvents:
            networkGatewayChangeFilters = self._eventNameFilters(networkGatewayChangeEvent)
            networkGatewayChangeAlarmDefined = self._alarmsWithSubscribers(networkGatewayChangeFilters)
            networkGatewayChangeFiltersAlarmOrSubscriberNotDefined = (networkGatewayChangeFilters == []) | (not networkGatewayChangeAlarmDefined)
        return networkGatewayChangeFiltersAlarmOrSubscriberNotDefined

    def routeTableChangeFilterAlarmOrSubscriberNotDefined(self):
        routeTableChangeEvents = ['CreateRoute', 'CreateRouteTable', 'ReplaceRoute', 'ReplaceRouteTableAssociation', 'DeleteRouteTable',
                                  'DeleteRoute', 'DisassociateRouteTable']
        routeTableChangeFiltersAlarmOrSubscriberNotDefined = False
        for routeTableChangeEvent in routeTableChangeEvents:
            routeTableChangeFilters = self._eventNameFilters(routeTableChangeEvent)
            routeTableChangeAlarmDefined = self._alarmsWithSubscribers(routeTableChangeFilters)
            routeTableChangeFiltersAlarmOrSubscriberNotDefined = (routeTableChangeFilters == []) | (not routeTableChangeAlarmDefined)
        return routeTableChangeFiltersAlarmOrSubscriberNotDefined

    def vpcChangeFilterAlarmOrSubscriberNotDefined(self):
        vpcChangeEvents = ['CreateVpc', 'DeleteVpc', 'ModifyVpcAttribute', 'AcceptVpcPeeringConnection', 'CreateVpcPeeringConnection',
                           'DeleteVpcPeeringConnection', 'RejectVpcPeeringConnection', 'AttachClassicLinkVpc', 'DetachClassicLinkVpc',
                           'DisableVpcClassicLink', 'EnableVpcClassicLink']
        vpcChangeFiltersAlarmOrSubscriberNotDefined = False
        for vpcChangeEvent in vpcChangeEvents:
            vpcChangeFilters = self._eventNameFilters(vpcChangeEvent)
            vpcChangeAlarmDefined = self._alarmsWithSubscribers(vpcChangeFilters)
            vpcChangeFiltersAlarmOrSubscriberNotDefined = (vpcChangeFilters == []) | (not vpcChangeAlarmDefined)
        return vpcChangeFiltersAlarmOrSubscriberNotDefined

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
            if filter.isCombinationOfTwoFilters('additionalEventData.MFAUsed', 'Yes','eventName', 'ConsoleLogin', '!='):
                filters.append(filter)
        return filters

    def _consoleAuthFailureFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isCombinationOfTwoFilters('errorMessage', 'Failed authentication','eventName', 'ConsoleLogin'):
                filters.append(filter)
        return filters

    def _rootLoginFilters(self):
        filters = []
        for filter in self.filters:
            if filter.isRootLoginFilter():
                filters.append(filter)
        return filters

    def _eventNameFilters(self, changeEvent):
        filters = []
        for filter in self.filters:
            if filter.isEventNameSpecificFilter(changeEvent):
                filters.append(filter)
        return filters

    def _twoFilterCombination(self, key1, value1, key2, value2):
        filters = []
        for filter in self.filters:
            if filter.isCombinationOfTwoFilters(key1, value1, key2, value2):
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
