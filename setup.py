from distutils.core import setup
import mintr

setup(
  author = mintr.__author__,
  name = mintr.__name__,
  packages = [mintr.__name__], 
  version = mintr.__version__,
  license = mintr.__license__,
  description = 'An API client for Mint.com',
  url = 'https://github.com/shanksauce/mintr',
  keywords = ['client', 'api', 'mint', 'json']
)
