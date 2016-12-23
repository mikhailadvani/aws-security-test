import boto3
class KMS:
    def __init__(self):
        self.kms = boto3.client('kms')

    def getKeys(self):
        return self.kms.list_keys()

    def getRotationStatus(self, keyId):
        return self.kms.get_key_rotation_status(KeyId=keyId)

    def describeKey(self, keyId):
        return self.kms.describe_key(KeyId=keyId)