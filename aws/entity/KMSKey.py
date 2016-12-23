from aws.api import KMS
class KMSKey:
    def __init__(self, kmsKeyDict):
        self.id = kmsKeyDict['KeyId']
        self._fetchRotationInfo()

    def _fetchRotationInfo(self):
        self.enabled = KMS().describeKey(self.id)['KeyMetadata']['KeyState'] == 'Enabled'
        self.rotationEnabled = KMS().getRotationStatus(self.id)['KeyRotationEnabled']