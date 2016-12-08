# Runtime
#### Requirements
- **Python**: 2.6.6
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

##### Tests to run

Setup a config file similar to [default.yml](https://github.com/mikhailadvani/cis-aws-automation/blob/master/config/default.yml) to execute desired tests. Value for each test should be `True` or `False`.

#### Execution Steps
`python main.py -c config/default.yml` - Will use the credentials from the environment variables if found or will fall back to the default profile in `~/.aws/config`

`python main.py -c config/default.yml -p profile_name` - Will use the credentials from the corresponding profile defined in `~/.aws/config`

#### Recommendation that have not been automated

* **Recommendation 1.1**: Avoid the use of "root" account. Since avoid is a subjective term, assertion would be incorrect. The last login of root user would be written to `root_login.txt` for reference. Also recommendation 3.3 asks for an alarm for "root" login which provides traceability for "root" logins.   

# Development
#### Requirements
- **Vagrant** : Version 1.8.5
- **VirtualBox** : Version 5.1.4

# License
Apache License 2.0



