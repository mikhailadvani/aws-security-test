import argparse
import boto3
import unittest
import yaml
from tests.iam import IamAudit
from tests.networking import NetworkingAudit
from tests.log import LoggingAudit
from tests.monitoring import MonitoringAudit

suite = unittest.TestSuite()

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, help="Selects the config file")
parser.add_argument("-p", "--profile", type=str, help="Specifies the boto profile to choose from  ~/.aws/config")
args = parser.parse_args()

if args.profile :
    boto3.setup_default_session(profile_name=args.profile)

testConfig = yaml.load(open(args.config, 'r'))

for testCategory, levelConfig in testConfig.iteritems():
    for level, tests in levelConfig.iteritems():
        for test, enabled in tests.iteritems():
            if enabled:
                suite.addTest(eval(testCategory+"Audit")(test))

runner = unittest.TextTestRunner()
testExecution = runner.run(suite)
exit(len(testExecution.failures) + len(testExecution.errors))