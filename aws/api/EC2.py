import boto3

class EC2:
    def __init__(self, region):
        self.ec2 = boto3.client('ec2', region_name=region)

    def get_security_groups(self):
        return self.ec2.describe_security_groups()