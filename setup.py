from distutils.core import setup
import mintr
import pandoc

#pandoc.core.PANDOC_PATH = '/path/to/pandoc'
doc = pandoc.Document()
doc.markdown = open('README.md').read()

setup(
  author = mintr.__author__,
  name = mintr.__name__,
  packages = [mintr.__name__], 
  version = mintr.__version__,
  license = mintr.__license__,
  description = 'An API client for Mint.com',
  longdescription = doc.rst,
  url = 'https://github.com/shanksauce/mintr',
  keywords = ['client', 'api', 'mint', 'json']
)
