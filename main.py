import argparse
import boto3
import unittest
import yaml
from tests.iam import IamLevel1
from tests.networking import NetworkingLevel1
from tests.log import LoggingLevel1

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

for test, enabled in testConfig['loggingLevel1'].iteritems():
    if enabled:
        suite.addTest(LoggingLevel1(test))

runner = unittest.TextTestRunner()
testExecution = runner.run(suite)
exit(len(testExecution.failures) + len(testExecution.errors))