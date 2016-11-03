import unittest
from aws.api import IAM
from aws.entity import IAMUser

class IamLevel1(unittest.TestCase):
    def testMfaEnabledForConsoleUsers(self):
        iamUsersWithoutMfa = []
        users = IAM().getCredentialReport()
        for user in users:
            iamUser = IAMUser(user)
            if not iamUser.mfa:
                iamUsersWithoutMfa.append(iamUser)
        self.assertEqual([], iamUsersWithoutMfa, "Users %s have console passwords without MFA" % self._users(iamUsersWithoutMfa))

    def _users(self, iamUsers):
        users = []
        for iam in iamUsers:
            users.append(iam.user)
        return ",".join(users)
