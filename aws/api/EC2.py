import boto3

class EC2:
    def __init__(self):
        self.ec2 = boto3.client('ec2')

    def get_security_groups(self):
        return self.ec2.describe_security_groups()