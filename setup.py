from setuptools import setup

MAJOR=0
MINOR=0
BUILD=6

setup(
  author = 'Ben Shank',
  author_email = 'ben@shankware.com',
  name = 'mintr',
  packages = ['mintr'],
  version = '%i.%i.%i' % MAJOR, MINOR, BUILD,
  license = 'MIT',
  description = 'An API client for Mint.com',
  url = 'https://github.com/shanksauce/mintr',
  keywords = ['client', 'api', 'mint', 'json'],
  zip_safe = False,
  install_requires = ['requests']
)
