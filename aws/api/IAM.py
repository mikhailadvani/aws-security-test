import boto3

class IAM:
    def __init__(self):
        self.iam = boto3.client('iam')

    def getCredentialReport(self):
        self.iam.generate_credential_report()
        credentialReportCsv = self.iam.get_credential_report()['Content']
        return self._credentialReportDict(credentialReportCsv)

    def _credentialReportDict(self, csvReport):
        credentialReportDict = []
        rows = csvReport.split('\n')
        keys = rows[0].split(',')
        for row in rows[1:len(rows)]:
            dict = {}
            values = row.split(',')
            for index in range(0,len(keys)):
                dict[keys[index]] = values[index]
            credentialReportDict.append(dict)
        return credentialReportDict
