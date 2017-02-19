from setuptools import setup

setup(name='aws-security-test',
      version='0.0.1',
      description='Test automation to determine adherence to pre-defined set of security recommendations',
      url='https://github.com/mikhailadvani/aws-security-test',
      author='Mikhail Advani',
      author_email='mikhail.advani@gmail.com',
      license='Apache',
      packages=['tests', 'aws'],
      install_requires=[
          'boto3',
          'pyyaml'
      ],
      zip_safe=False)