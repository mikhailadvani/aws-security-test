class S3BucketPolicy:
    def __init__(self, bucketPolicyDict):
        self.rules = bucketPolicyDict['Statement']

    def allowsAccessForAllPrincipals(self):
        accessAllowedForAllPrincipals = False
        for rule in self.rules:
            if ((rule['Effect'] == 'Allow') & (rule['Principal'] == '*')):
                accessAllowedForAllPrincipals = True
        return accessAllowedForAllPrincipals
