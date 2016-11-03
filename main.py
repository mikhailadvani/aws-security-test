import unittest
import yaml
import sys
from networking import NetworkingLevel1

suite = unittest.TestSuite()
file = open(sys.argv[1], 'r')
testConfig = yaml.load(file)

for test, enabled in testConfig['networkingLevel1'].iteritems():
    if enabled:
        suite.addTest(NetworkingLevel1(test))

runner = unittest.TextTestRunner()
runner.run(suite)