import unittest
from networking import NetworkingLevel1

class Main():
    def testNetworkingLevel1(self):
        networkingLevel1Rules = NetworkingLevel1()
        networkingLevel1Rules.testSshNotOpenFromInternet()

if __name__ == '__main__':
    unittest.main()