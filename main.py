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

for testCategory, tests in testConfig.iteritems():
    for test, enabled in tests.iteritems():
        if enabled:
            suite.addTest(eval(testCategory)(test))

runner = unittest.TextTestRunner()
testExecution = runner.run(suite)
exit(len(testExecution.failures) + len(testExecution.errors))