try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='mail-bug',
    version='0.1',
    description='Stub description for mail-bug.',
    install_requires=['keyring', 'python_utility==0.1'],
    scripts=['bin/mb'],
    packages=[],
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    url='http://example.org',
    download_url='http://example.org/mail-bug.tar.gz',
    dependency_links=[
        'git+git://github.com/FunTimeCoding/python-utility.git'
        '#egg=python_utility-0.1'
    ]
)
