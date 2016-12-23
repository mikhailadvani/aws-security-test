# Runtime
#### Requirements
- **Python**: 2.7.12
- **Boto3**: 1.4.1

#### Configuring Tests

##### Credentials

Credentials need to be setup as described in [Boto3 Documentation](http://boto3.readthedocs.io/en/latest/guide/configuration.html).
Access needed by the users' API keys configured:

- AmazonEC2ReadOnlyAccess
- IAMReadOnlyAccess
- AWSCloudTrailReadOnlyAccess
- AmazonS3ReadOnlyAccess
- CloudWatchLogsReadOnlyAccess
- CloudWatchReadOnlyAccess
- AmazonSNSReadOnlyAccess
- *KMSReadOnlyPolicy* - There is no pre-defined AWS Policy with the necessary privileges. The custom policy can defined as mentioned in the [documentation](https://docs.aws.amazon.com/kms/latest/developerguide/iam-policies.html#iam-policy-example-read-only-console)

##### Tests to run

Setup a config file similar to [default.yml](https://github.com/mikhailadvani/cis-aws-automation/blob/master/config/default.yml) to execute desired tests. Value for each test should be `True` or `False`.

#### Execution Steps

##### Run as script
`python cis_aws_automation.py -c config/default.yml` - Will use the credentials from the environment variables if found or will fall back to the default profile in `~/.aws/config`

`python cis_aws_automation.py -c config/default.yml -p profile_name` - Will use the credentials from the corresponding profile defined in `~/.aws/config`

##### Run installed module
`python -m cis_aws_automation -c config/default.yml`

`python -m cis_aws_automation -c config/default.yml -p profile_name`

#### Recommendation that have not been automated

* **Recommendation 1.1**: Avoid the use of "root" account. Since avoid is a subjective term, assertion would be incorrect. The last login of root user would be written to `root_login.txt` for reference. Also recommendation 3.3 asks for an alarm for "root" login which provides traceability for "root" logins.
* **Recommendation 1.14**: Ensure security questions are registered in the AWS account. There is no API available to fetch this information and hence automation would not be possible. Audit and remediation needs to be carried out as mentioned in the recommendation document.
* **Recommendation 3.15**: Ensure security contact information is registered. There is no API available to fetch this information and hence automation would not be possible. Audit and remediation needs to be carried out as mentioned in the recommendation document.

# Development
#### Requirements
- **Vagrant** : Version 1.8.5
- **VirtualBox** : Version 5.1.4

#### Notes:

- Python in the vagrant box is 2.6.6. Upgrade needs to be done manually

# License
Apache License 2.0



