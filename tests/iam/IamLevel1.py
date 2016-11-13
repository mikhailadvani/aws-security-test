import unittest
from aws.api import IAM
from aws.entity import IAMUser

class IamLevel1(unittest.TestCase):
    def testMfaEnabledForConsoleUsers(self):
        iamUsersWithoutMfa = []
        for iamUser in self._getIamUserList():
            if not iamUser.mfaEnabled():
                iamUsersWithoutMfa.append(iamUser)
        self.assertEqual([], iamUsersWithoutMfa, "Users %s have console passwords without MFA" % self._users(iamUsersWithoutMfa))

    def testUnusedCredentialsAreDeactivated(self):
        oldUserTimePeriod = 90
        iamUsersWithUnusedCredentials = []
        for iamUser in self._getIamUserList():
            if ((not iamUser.credentialsUsed(oldUserTimePeriod)) | (not iamUser.accessKeysUsed(oldUserTimePeriod))):
                iamUsersWithUnusedCredentials.append(iamUser)
        self.assertEqual([], iamUsersWithUnusedCredentials, "Active users %s have passwords/access keys unused for long" % self._users(iamUsersWithUnusedCredentials))

    def testAccessKeysAreRotated(self):
        oldAccessKeyTimePeriodInDays = 90
        iamUsersWithOldAccessKeys = []
        for iamUser in self._getIamUserList():
            if not iamUser.accessKeysRotated(oldAccessKeyTimePeriodInDays):
                iamUsersWithOldAccessKeys.append(iamUser)
        self.assertEqual([], iamUsersWithOldAccessKeys, "Active users %s have access keys not rotated for long" % self._users(iamUsersWithOldAccessKeys))

    def testRootAccountHasNoActiveAccessKeys(self):
        rootUser = None
        for iamUser in self._getIamUserList():
            if iamUser.isRootUser():
                rootUser = iamUser
        self.assertTrue(rootUser.accessKeysActive, "Root user has access key(s) active")

    def testPoliciesAreNotAttachedToUsers(self):
        usersWithAttachedPolicies = []
        for iamUser in self._getIamUserList():
            if not iamUser.isRootUser():
                if self._userHasAttachedPolicies(iamUser.user):
                    usersWithAttachedPolicies.append(iamUser)
        self.assertEqual([], usersWithAttachedPolicies, "Users %s have policies attached to them" % self._users(usersWithAttachedPolicies))

    def testPasswordPolicyRequiresUpperCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireUppercaseCharacters'), "Password policy does not mandate upper case characters in password")

    def testPasswordPolicyRequiresLowerCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireLowercaseCharacters'), "Password policy does not mandate lower case characters in password")

    def testPasswordPolicyRequiresNumbers(self):
        self.assertTrue(self._getPasswordPolicyField('RequireNumbers'), "Password policy does not mandate numbers in password")

    def testPasswordPolicyRequiresSymbols(self):
        self.assertTrue(self._getPasswordPolicyField('RequireSymbols'), "Password policy does not mandate symbols in password")

    def testPasswordPolicyRequiresMinimumLength(self):
        requirePasswordLength = 14
        self.assertTrue(self._getPasswordPolicyField('MinimumPasswordLength') >= requirePasswordLength, "Password policy does not mandate required minimum length of password")

    def testPasswordPolicyPreventsPasswordReuse(self):
        requiredPasswordsToRemember = 24
        self.assertTrue(self._getPasswordPolicyField('PasswordReusePrevention', 0) >= requiredPasswordsToRemember, "Password policy does not mandate minimum password re-use prevention")

    def testPasswordPolicyEnsuresPasswordExpiry(self):
        requiredPasswordExpirationPeriod = 90
        self.assertTrue(self._getPasswordPolicyField('MaxPasswordAge', 1000) <= requiredPasswordExpirationPeriod, "Password policy does not mandate minimum password expiry time")

    def _getPasswordPolicyField(self, field, default=False):
        passwordPolicy = IAM().getPasswordPolicy()
        return passwordPolicy['PasswordPolicy'].get(field, default)

    def _getIamUserList(self):
        iamUserList = []
        users = IAM().getCredentialReport()
        for user in users:
            iamUser = IAMUser(user)
            iamUserList.append(iamUser)
        return iamUserList

    def _users(self, iamUsers):
        users = []
        for iam in iamUsers:
            users.append(iam.user)
        return ",".join(users)

    def _userHasAttachedPolicies(self, userName):
        return len(IAM().getUserPolicies(userName)['AttachedPolicies'])
