import unittest
import yaml
import boto3
import argparse
from networking import NetworkingLevel1
from iam import IamLevel1

suite = unittest.TestSuite()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, help="Selects the config file")
parser.add_argument("-p", "--profile", type=str, help="Specifies the boto profile to choose from  ~/.aws/config")
args = parser.parse_args()

if args.profile :
    boto3.setup_default_session(profile_name=args.profile)

testConfig = yaml.load(open(args.config, 'r'))
for test, enabled in testConfig['networkingLevel1'].iteritems():
    if enabled:
        suite.addTest(NetworkingLevel1(test))

for test, enabled in testConfig['iamLevel1'].iteritems():
    if enabled:
        suite.addTest(IamLevel1(test))

runner = unittest.TextTestRunner()
exit(len(runner.run(suite).failures))