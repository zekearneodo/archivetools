from setuptools import setup
import sys

# It uses features of tarfile that are only python 3.x
if sys.version_info < (2, 7):
    sys.exit('Sorry, Python < 2.7 is not supported')

setup(name='archivetools',
      version='0.0.1',
      description='Tools to compress and keep trakc of data',
      url='http://github.com/zekearneodo/archivetools',
      author='Zeke Arneodo',
      author_email='earneodo@ucsd.edu',
      license='GNU3',
      packages=['archivetools'],
      install_requires=[],
      zip_safe=False)
