import boto3
import ast
class S3:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def getBucketAcl(self, bucket):
        return self.s3.get_bucket_acl(Bucket=bucket)

    def getBucketPolicy(self, bucket):
        return ast.literal_eval(self.s3.get_bucket_policy(Bucket=bucket)['Policy'])

    def getBucketLogging(self, bucket):
        return self.s3.get_bucket_logging(Bucket=bucket)
