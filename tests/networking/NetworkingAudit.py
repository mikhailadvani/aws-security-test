import unittest
from aws.api import EC2
from aws.entity import SecurityGroup
from aws.entity import RouteTable

class NetworkingAudit(unittest.TestCase):
    def testSshNotOpenFromInternet(self):
        sshOpenSecurityGroups = self._getSecurityGroupsWithProtocolPortOpenFromInternet('tcp', 22)
        self.assertEqual([], sshOpenSecurityGroups, "Security group(s) with SSH allowed from Internet[vpcId:groupId]: %s." % self._vpcIdsGroupIds(sshOpenSecurityGroups))

    def testRdpNotOpenFromInternet(self):
        rdpOpenSecurityGroups = self._getSecurityGroupsWithProtocolPortOpenFromInternet('tcp', 3389)
        self.assertEqual([], rdpOpenSecurityGroups, "Security group(s) with RDP allowed from Internet[vpcId:groupId]: %s." % self._vpcIdsGroupIds(rdpOpenSecurityGroups))

    def testPortsOpenFromTheInternet(self):
        internetOpenSecurityGroups = self._getSecurityGroupsWithAccessOpenFromInternet()
        file = open('artifacts/internet_open_security_groups.csv', 'w')
        file.write("VPC ID, Security Group ID")
        for securityGroup in self._vpcIdsGroupIds(internetOpenSecurityGroups).split(','):
            file.write('\n'+ securityGroup.replace(':',','))

    def testDefaultSecurityGroupsNotOpenFromInternet(self):
        defaultSecurityGroupsOpenFromInternet = self._getDefaultSecurityGroupsOpenFromInternet()
        self.assertEqual([], defaultSecurityGroupsOpenFromInternet, "Default Security group(s) with access allowed from Internet[vpcId:groupId]: %s." % self._vpcIdsGroupIds(defaultSecurityGroupsOpenFromInternet))

    def testMainRouteTableIsPrivate(self):
        nonPrivateMainRouteTables = []
        for routeTable in self._getAllRouteTables():
            if routeTable.isMain() and not routeTable.isPrivateOnly():
                nonPrivateMainRouteTables.append(routeTable)
        self.assertEqual([], nonPrivateMainRouteTables, "Main Route table(s) with routes other than default local route: %s" % self._vpcIdsRtbIds(nonPrivateMainRouteTables))

    def _getAllRouteTables(self):
        routeTables = []
        for rtb in EC2().getRouteTables()['RouteTables']:
            routeTable = RouteTable(rtb)
            routeTables.append(routeTable)
        return routeTables

    def _getAllSecurityGroups(self):
        securityGroups = []
        for sg in EC2().getSecurityGroups()['SecurityGroups']:
            securityGroup = SecurityGroup(sg['VpcId'], sg['GroupId'], sg['GroupName'], sg['IpPermissions'])
            securityGroups.append(securityGroup)
        return securityGroups

    def _getDefaultSecurityGroupsOpenFromInternet(self):
        sgs = []
        allSecurityGroups = self._getAllSecurityGroups()
        for securityGroup in allSecurityGroups:
            if securityGroup.isDefault() and securityGroup.inboundAccessOpenFromInternet():
                sgs.append(securityGroup)
        return sgs

    def _getSecurityGroupsWithAccessOpenFromInternet(self):
        sgs = []
        allSecurityGroups = self._getAllSecurityGroups()
        for securityGroup in allSecurityGroups:
            if securityGroup.inboundAccessOpenFromInternet():
                sgs.append(securityGroup)
        return sgs

    def _getSecurityGroupsWithProtocolPortOpenFromInternet(self, protocol, port):
        sgs = []
        allSecurityGroups = self._getAllSecurityGroups()
        for securityGroup in allSecurityGroups:
            if securityGroup.inboundProtocolPortOpenFromInternet(protocol, port):
                sgs.append(securityGroup)
        return sgs

    def _vpcIdsGroupIds(self, securityGroups):
        return ",".join(map(lambda securityGroup: securityGroup.vpcId + ":" + securityGroup.groupId, securityGroups))

    def _vpcIdsRtbIds(self, routeTables):
        return ",".join(map(lambda routeTable: routeTable.vpcId + ":" + routeTable.id, routeTables))


