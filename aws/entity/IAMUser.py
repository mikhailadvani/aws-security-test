from dateutil.parser import parse
import datetime

class IAMUser():
    def __init__(self, userDict):
        self.user = userDict['user']
        self.mfa = userDict['mfa_active'] == 'true'
        self.passwordEnabled = userDict['password_enabled'] != 'false'
        self.passwordLastUsed = userDict['password_last_used']
        self.accessKeysRotatedDates = self._setAccessKeyRotatedDates(userDict)

    def mfaEnabled(self):
        return (not self.passwordEnabled) | self.mfa

    def credentialsUsed(self, days):
        if self.passwordEnabled:
            return self._daysPassed(self.passwordLastUsed) <= days
        else:
            return True

    def accessKeysRotated(self, days):
        keysRotated = True
        for accessKeyRotatedDate in self.accessKeysRotatedDates:
            keysRotated = keysRotated & (self._daysPassed(accessKeyRotatedDate) <= days)
        return keysRotated

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
