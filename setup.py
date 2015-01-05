from distutils.core import setup
import mintr

setup(
  name = mintr.__name__,
  packages = [mintr.__name__], 
  version = mintr.__version__,
  description = 'An API client for Mint.com',
  author = mintr.__author__,
  author_email = 'ben@shankware.com',
  url = 'https://github.com/shanksauce/mintr',
  download_url = 'https://github.com/shanksauce/mintr/tarball/0.1',
  keywords = ['client', 'api', 'mint', 'json'],
  classifiers = [],
)
