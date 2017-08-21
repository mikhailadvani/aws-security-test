import unittest
from aws.api import IAM
from aws.entity import IAMUser

class IamAudit(unittest.TestCase):
    def testRootAccountLoginIsAvoided(self):
        for iamUser in self._getIamUserList():
            if iamUser.isRootUser():
                file = open('artifacts/root_login.txt', 'w')
                file.write(iamUser.passwordLastUsed)

    def testMfaEnabledForConsoleUsers(self):
        iamUsersWithoutMfa = []
        for iamUser in self._getIamUserList():
            if not iamUser.mfaEnabled():
                iamUsersWithoutMfa.append(iamUser)
        self.assertEqual([], iamUsersWithoutMfa, "User(s) with console passwords without MFA: %s." % self._users(iamUsersWithoutMfa))

    def testUnusedCredentialsAreDeactivated(self):
        oldUserTimePeriod = 90
        iamUsersWithUnusedCredentials = []
        for iamUser in self._getIamUserList():
            if ((not iamUser.credentialsUsed(oldUserTimePeriod)) | (not iamUser.accessKeysUsed(oldUserTimePeriod))):
                iamUsersWithUnusedCredentials.append(iamUser)
        self.assertEqual([], iamUsersWithUnusedCredentials, "Active user(s) with passwords/access keys unused for long: %s." % self._users(iamUsersWithUnusedCredentials))

    def testAccessKeysAreRotated(self):
        oldAccessKeyTimePeriodInDays = 90
        iamUsersWithOldAccessKeys = []
        for iamUser in self._getIamUserList():
            if not iamUser.accessKeysRotated(oldAccessKeyTimePeriodInDays):
                iamUsersWithOldAccessKeys.append(iamUser)
        self.assertEqual([], iamUsersWithOldAccessKeys, "Active user(s) with access keys not rotated for long: %s." % self._users(iamUsersWithOldAccessKeys))

    def testPasswordPolicyRequiresUpperCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireUppercaseCharacters'), "Password policy does not mandate upper case characters in password.")

    def testPasswordPolicyRequiresLowerCaseLetters(self):
        self.assertTrue(self._getPasswordPolicyField('RequireLowercaseCharacters'), "Password policy does not mandate lower case characters in password.")

    def testPasswordPolicyRequiresSymbols(self):
        self.assertTrue(self._getPasswordPolicyField('RequireSymbols'), "Password policy does not mandate symbols in password.")

    def testPasswordPolicyRequiresNumbers(self):
        self.assertTrue(self._getPasswordPolicyField('RequireNumbers'), "Password policy does not mandate numbers in password.")

    def testPasswordPolicyRequiresMinimumLength(self):
        requirePasswordLength = 14
        self.assertGreaterEqual(self._getPasswordPolicyField('MinimumPasswordLength'), requirePasswordLength, "Password policy does not mandate required minimum length of password.")

    def testPasswordPolicyPreventsPasswordReuse(self):
        requiredPasswordsToRemember = 24
        self.assertGreaterEqual(self._getPasswordPolicyField('PasswordReusePrevention', 0), requiredPasswordsToRemember, "Password policy does not mandate minimum password re-use prevention.")

    def testPasswordPolicyEnsuresPasswordExpiry(self):
        requiredPasswordExpirationPeriod = 90
        self.assertLessEqual(self._getPasswordPolicyField('MaxPasswordAge', 1000) , requiredPasswordExpirationPeriod, "Password policy does not mandate minimum password expiry time.")

    def testRootAccountHasNoActiveAccessKeys(self):
        rootUser = None
        for iamUser in self._getIamUserList():
            if iamUser.isRootUser():
                rootUser = iamUser
        self.assertTrue(rootUser.accessKeysActive, "Root user has access key(s) active.")

    def testPoliciesAreNotAttachedToUsers(self):
        usersWithAttachedPolicies = []
        for iamUser in self._getIamUserList():
            if not iamUser.isRootUser():
                if self._userHasAttachedPolicies(iamUser.user):
                    usersWithAttachedPolicies.append(iamUser)
        self.assertEqual([], usersWithAttachedPolicies, "User(s) with policies attached to them: %s." % self._users(usersWithAttachedPolicies))

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
