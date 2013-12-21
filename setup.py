#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

packages = [
    'fernet',
]

requires = [
    'pycrypto>=2.6.1',
#    'M2Crypto>=0.21.1',
    'py>=1.4.18',
    'python-dateutil>=2.2',
    'should-dsl>=2.1.2',
    'six>=1.4.1'
]

with open('README.md') as f:
    readme = f.read()
with open('HISTORY') as f:
    history = f.read()
with open('LICENSE') as f:
    license = f.read()

setup(
    name='fernet',
    version='1.0.0',
    description='Delicious HMAC Digest(if) authentication and AES-128-CBC encryption.',
    long_description=readme + '\n\n' + history,
    author='Scott Persinger',
    author_email='scottp@heroku.com',
    url='https://github.com/heroku/fernet-py',
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'requests': 'requests'},
    include_package_data=True,
    install_requires=requires,
    license=license,
    zip_safe=False,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ),
)
