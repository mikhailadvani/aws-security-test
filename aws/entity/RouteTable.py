class RouteTable:
    def __init__(self, routeTableDict):
        self.id = routeTableDict['RouteTableId']
        self.associations = routeTableDict['Associations']
        self.vpcId = routeTableDict['VpcId']
        self.routes = routeTableDict['Routes']

    def isMain(self):
        result = False
        for association in self.associations:
            if association['Main']:
                result = True
        return result

    def isPrivateOnly(self):
        return len(self.routes) == 1 and self.routes[0]['GatewayId'] == 'local'


