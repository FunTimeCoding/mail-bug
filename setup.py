#!/usr/bin/env python3
from setuptools import setup

setup(
    name='mail-bug',
    version='0.1.0',
    description='Stub description.',
    url='https://github.com/FunTimeCoding/mail-bug',
    author='Alexander Reitzel',
    author_email='funtimecoding@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
    ],
    keywords='development project skeleton',
    packages=['mail_bug'],
    install_requires=['keyring'],
    python_requires='>=3.2',
    entry_points={
        'console_scripts': [
            'mb=mail_bug.mail_bug:'
            'MailBug.main',
        ],
    },
)
