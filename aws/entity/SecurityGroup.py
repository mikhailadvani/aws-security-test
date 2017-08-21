from aws.util import SecurityGroupRule

class SecurityGroup:
    def __init__(self, vpcId, groupId, groupName, ipPermissions):
        self.vpcId = vpcId
        self.groupId = groupId
        self.groupName = groupName
        sgRules = []
        for inboundRule in ipPermissions:
            sgRule = SecurityGroupRule(inboundRule)
            sgRules.append(sgRule)
        self.securityGroupRules = sgRules

    def inboundProtocolPortOpenFromInternet(self, protocol, port):
        accessAllowed = False
        for securityGroupRule in self.securityGroupRules:
            accessAllowed = accessAllowed | securityGroupRule.accessToProtocolPortAllowedFromInternet(protocol, port)
        return accessAllowed

    def inboundAccessOpenFromInternet(self):
        accessAllowed = False
        for securityGroupRule in self.securityGroupRules:
            accessAllowed = accessAllowed | securityGroupRule.accessAllowedFromInternet()
        return accessAllowed

    def isDefault(self):
        return self.groupName == 'default'