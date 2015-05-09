from setuptools import setup

MAJOR=0
MINOR=0
BUILD=8

setup(
  author = 'Ben Shank',
  author_email = 'ben@shankware.com',
  name = 'mintr',
  packages = ['mintr'],
  version = '{0}.{1}.{2}'.format(MAJOR, MINOR, BUILD),
  license = 'MIT',
  description = 'An API client for Mint.com',
  url = 'https://github.com/shanksauce/mintr',
  keywords = ['client', 'api', 'mint', 'json'],
  zip_safe = False,
  install_requires = ['requests']
)
