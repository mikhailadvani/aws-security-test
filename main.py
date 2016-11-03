import unittest
import yaml
import sys
import boto3
import argparse
from networking import NetworkingLevel1

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--config", type=str, help="Selects the config file")
parser.add_argument("-p", "--profile", type=str, help="Specifies the boto profile to choose from  ~/.aws/config")
args = parser.parse_args()


suite = unittest.TestSuite()
file = open(args.config, 'r')
if args.profile :
    boto3.setup_default_session(profile_name=args.profile)

testConfig = yaml.load(file)

for test, enabled in testConfig['networkingLevel1'].iteritems():
    if enabled:
        suite.addTest(NetworkingLevel1(test))

runner = unittest.TextTestRunner()
runner.run(suite)