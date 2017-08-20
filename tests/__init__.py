import argparse
import boto3
import unittest
import yaml
import os
from third_party_modules import HTMLTestRunner
from iam import IamAudit
from networking import NetworkingAudit
from log import LoggingAudit
from monitoring import MonitoringAudit


def main():
    artifacts_dir = "artifacts"
    suite = unittest.TestSuite()

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", type=str, required=True, help="Selects the config file")
    parser.add_argument("-p", "--profile", type=str, help="Specifies the boto profile to choose from  ~/.aws/config")
    parser.add_argument("--report", default='html', help="Prints test execution on the console rather than generating a HTML report", choices=['text', 'html'])
    args = parser.parse_args()

    if args.profile :
        boto3.setup_default_session(profile_name=args.profile)

    testConfig = yaml.load(open(args.config, 'r'))

    for testCategory, tests in testConfig.iteritems():
        for test, enabled in tests.iteritems():
            if enabled:
                suite.addTest(eval(testCategory+"Audit")(test))
    runner = ''

    if args.report == 'text':
        runner = unittest.TextTestRunner(verbosity=2)
    elif args.report == 'html':
        reportFile = open("test_results.html", "w")
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=reportFile,
            title='aws-security-test - Report',
            verbosity=2
        )
    else:
        print 'Invalid report type'
        exit(1)

    if not os.path.exists(artifacts_dir):
        os.makedirs(artifacts_dir)

    testExecution = runner.run(suite)
    return len(testExecution.failures) + len(testExecution.errors)