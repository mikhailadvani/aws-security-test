import boto3

class SNS:
    def __init__(self):
        self.sns = boto3.client('sns')

    def getSubscriptions(self, topicArn):
        return self.sns.list_subscriptions_by_topic(TopicArn=topicArn)

    def getAllSubscriptions(self):
        return self.sns.list_subscriptions()