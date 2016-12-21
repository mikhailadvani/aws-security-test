from setuptools import setup

setup(name='cis_aws_automation',
      version='0.0.1',
      description='Test automation to determine compliance with CIS benchmarks for AWS',
      url='https://github.com/mikhailadvani/cis-aws-automation',
      author='Mikhail Advani',
      author_email='mikhail.advani@gmail.com',
      license='Apach',
      packages=['tests', 'aws'],
      install_requires=[
          'boto3',
          'pyyaml'
      ],
      zip_safe=False)