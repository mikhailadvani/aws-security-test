from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
      long_description = f.read()

with open(path.join(here, 'version.txt'), encoding='utf-8') as f:
      version = f.read()

setup(name='aws-security-test',
      version=version,

      description='Test automation to determine adherence to pre-defined set of security recommendations',
      long_description=long_description,

      url='https://github.com/mikhailadvani/aws-security-test',

      author='Mikhail Advani',
      author_email='mikhail.advani@gmail.com',

      license='Apache',

      classifiers=[
            'Development Status :: 4 - Beta',

            'Intended Audience :: Developers',
            'Intended Audience :: Information Technology',
            'Intended Audience :: System Administrators',
            'Topic :: Internet',
            'Topic :: Security',
            'Topic :: Software Development :: Build Tools',
            'Topic :: Software Development :: Testing',
            'Topic :: System',
            'Topic :: System :: Logging',
            'Topic :: System :: Monitoring',
            'Topic :: System :: Networking :: Firewalls',

            'License :: OSI Approved :: Apache Software License',

            'Programming Language :: Python :: 2.7'
      ],
      keywords='aws security test iam networking logging monitoring ec2 vpc',
      packages=['tests','tests.iam', 'tests.log','tests.monitoring','tests.networking', 'aws', 'aws.api','aws.entity', 'aws.util', 'third_party_modules'],
      install_requires=[
          'boto3',
          'pyyaml'
      ],
      extras_require={
            'dev': ['twine'],
      },
      entry_points={
            'console_scripts': [
                  'aws_security_test=tests:main'
            ],
      },
      zip_safe=False)