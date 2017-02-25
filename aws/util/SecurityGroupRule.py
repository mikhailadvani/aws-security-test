class SecurityGroupRule:
    def __init__(self, rule):
        self.protocol = rule['IpProtocol']
        fromPort = rule.get('FromPort', -2)
        toPort = rule.get('ToPort', -3)
        self.portRange = range(fromPort, toPort+1)
        ipRanges = []
        for ipRange in rule['IpRanges']:
            ipRanges.append(ipRange['CidrIp'])
        self.ips = ipRanges

    def accessToProtocolPortAllowedFromInternet(self, protocol, port):
        return self._accessAllowedFromInternet() & (self._allProtocolsAllowed() | (self._protocolAllowed(protocol) & self._portAllowed(port)))

    def accessAllowedFromInternet(self):
        return self._accessAllowedFromInternet()

    def _allProtocolsAllowed(self):
        return self.protocol == '-1'

    def _protocolAllowed(self, protocol):
        return (protocol == self.protocol)

    def _portAllowed(self, port):
        return port in self.portRange

    def _accessAllowedFromInternet(self):
        return '0.0.0.0/0' in self.ips
