# Runtime
#### Requirements
- **Python**: 2.6.6
- **Boto3**: 1.4.1

#### Configuring Tests
Setup a config file similar to [config.yml](https://github.com/mikhailadvani/cis-aws-automation/blob/master/config.yml) to execute desired tests. Value for each test should be `True` or `False`. Credentials need to be setup as described in [Boto3 Documentation](http://boto3.readthedocs.io/en/latest/guide/configuration.html)

#### Execution Steps
`python main.py -c config.yml` - Will use the credentials from the environment variables if found or will fall back to the default profile in `~/.aws/config`

`python main.py -c config.yml -p profile_name` - Will use the credentials from the corresponding profile defined in `~/.aws/config`
# Development
#### Requirements
- **Vagrant** : Version 1.8.5
- **VirtualBox** : Version 5.1.4

# License
Apache License 2.0



