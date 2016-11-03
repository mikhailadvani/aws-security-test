class IAMUser():
    def __init__(self, userDict):
        self.user = userDict['user']
        self.mfa = userDict['mfa_active'] == 'true'
