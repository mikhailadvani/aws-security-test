import boto3
class S3:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def getBucketAcl(self, bucket):
        return self.s3.get_bucket_acl(Bucket=bucket)
