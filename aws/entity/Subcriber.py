class Subscriber():
    def __init__(self, subscriberDict):
        self.topicArn = subscriberDict['TopicArn']
        self.owner = subscriberDict['Owner']
        self.endpoint = subscriberDict['Endpoint']
        self.protocol = subscriberDict['Protocol']
        self.subscriptionArn = subscriberDict['SubscriptionArn']

    def getCsv(self):
        return "\n%s,%s,%s,%s,%s" % (self.topicArn, self.subscriptionArn, self.protocol, self.endpoint, self.owner)