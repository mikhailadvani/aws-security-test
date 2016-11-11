from dateutil.parser import parse
import datetime

class IAMUser():
    def __init__(self, userDict):
        self.user = userDict['user']
        self.mfa = userDict['mfa_active'] == 'true'
        self.passwordEnabled = userDict['password_enabled'] != 'false'
        self.passwordLastUsed = userDict['password_last_used']
        self.accessKeysRotatedDates = self._setAccessKeyRotatedDates(userDict)
        self.accessKeysUsedDates = self._setAccessKeyUsedDates(userDict)
        self.accessKeysActive = (userDict['access_key_1_active'] == 'false') & (userDict['access_key_2_active'] == 'false')

    def mfaEnabled(self):
        return (not self.passwordEnabled) | self.mfa

    def credentialsUsed(self, days):
        if self.passwordEnabled:
            return self._daysPassed(self.passwordLastUsed) <= days
        else:
            return True

    def isRootUser(self):
        return self.user == '<root_account>'

    def accessKeysUsed(self, days):
        return self._checkKeyDate('used', days)

    def accessKeysRotated(self, days):
        return self._checkKeyDate('rotated', days)

    def _checkKeyDate(self, action, days):
        if action == 'used':
            keyDates = self.accessKeysUsedDates
        else:
            keyDates = self.accessKeysRotatedDates
        keyAccessed = False
        for keyDate in keyDates:
            keyAccessed = keyAccessed | (self._daysPassed(keyDate) >= days)
        return not keyAccessed

    def _daysPassed(self, dateStr):
        passwordLastUsedDate = parse(dateStr)
        date = datetime.date(passwordLastUsedDate.year, passwordLastUsedDate.month, passwordLastUsedDate.day)
        now = datetime.datetime.now()
        today = datetime.date(now.year, now.month, now.day)
        return (today - date).days

    def _setAccessKeyRotatedDates(self, userDict):
        accessKeysRotatedDates = []
        if userDict['access_key_1_active'] == 'true':
            accessKeysRotatedDates.append(userDict['access_key_1_last_rotated'])
        if userDict['access_key_2_active'] == 'true':
            accessKeysRotatedDates.append(userDict['access_key_2_last_rotated'])
        return accessKeysRotatedDates

    def _setAccessKeyUsedDates(self, userDict):
        accessKeysUsedDates = []
        if userDict['access_key_1_active'] == 'true':
            accessKeysUsedDates.append(userDict['access_key_1_last_used_date'])
        if userDict['access_key_2_active'] == 'true':
            accessKeysUsedDates.append(userDict['access_key_1_last_used_date'])
        return accessKeysUsedDates
