try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='mail-bug',
      version='0.1',
      description='Stub description for mail-bug.',
      install_requires=['keyring'],
      scripts=['bin/mb'],
      packages=[],
      author='Alexander Reitzel',
      author_email='funtimecoding@gmail.com',
      url='http://example.org',
      download_url='http://example.org/mail-bug.tar.gz')
