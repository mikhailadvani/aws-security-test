class S3BucketAcl:
    def __init__(self, bucketAclDict):
        self.grants = bucketAclDict['Grants']

    def allUsersHavePrivileges(self):
        return self._checkPrivilege('http://acs.amazonaws.com/groups/global/AllUsers')

    def allAuthenticatedUsersHavePrivileges(self):
        return self._checkPrivilege('http://acs.amazonaws.com/groups/global/AuthenticatedUsers')

    def _checkPrivilege(self, privilegeUrl):
        privilege = False
        for grant in self.grants:
            if 'URI' in grant['Grantee']:
                privilege = privilege | (grant['Grantee']['URI'] == privilegeUrl)
        return privilege