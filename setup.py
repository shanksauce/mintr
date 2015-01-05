from setuptools import setup

setup(
  author = 'Ben Shank',
  author_email = 'ben@shankware.com',
  name = 'mintr',
  packages = ['mintr'],
  version = '0.0.4',
  license = 'MIT',
  description = 'An API client for Mint.com',
  url = 'https://github.com/shanksauce/mintr',
  keywords = ['client', 'api', 'mint', 'json'],
  zip_safe = False,
  install_requires = ['requests']
)
