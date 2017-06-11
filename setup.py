#!/usr/bin/env python3
from setuptools import setup

setup(
    name='mail-bug',
    version='0.1',
    description='Stub description for mail-bug.',
    install_requires=['keyring', 'python-utility'],
    scripts=['bin/mb'],
    packages=['mail_bug'],
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    url='http://example.org',
    download_url='http://example.org/mail-bug.tar.gz'
)
