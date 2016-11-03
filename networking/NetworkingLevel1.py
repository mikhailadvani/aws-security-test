import unittest
from aws.api import EC2
from aws.entity import SecurityGroup

class NetworkingLevel1(unittest.TestCase):
    def testSshNotOpenFromInternet(self):
        securityGroups = []
        for sg in EC2('us-east-1').get_security_groups()['SecurityGroups']:
            securityGroup = SecurityGroup(sg['VpcId'], sg['GroupId'], sg['IpPermissions'])
            if securityGroup.inboundSshOpenFromInternet():
                securityGroups.append(securityGroup)
        self.assertEqual([], securityGroups, "Security groups %s allow SSH from Internet" % self._groupIdsVpcIds(securityGroups))

    def _groupIdsVpcIds(self, securityGroups):
        ids = []
        for sg in securityGroups:
            ids.append(sg.vpcId + ":" + sg.groupId)
        return ",".join(ids)


