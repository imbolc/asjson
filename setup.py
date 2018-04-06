#!/usr/bin/env python
import os
import sys
import doctest
from setuptools import setup

import asjson as mod


DOC = mod.__doc__.strip()
NAME = mod.__name__
VERSION = mod.__version__
DESC = DOC.split('===\n')[1].strip().split('\n\n')[0].replace('\n', ' ')

open('README.md', 'w').write(DOC)
if sys.argv[-1] == 'publish':
    if not doctest.testfile(
            'README.md', optionflags=doctest.NORMALIZE_WHITESPACE).failed:
        os.system('python setup.py sdist upload')
        sys.exit(0)

setup(
    name=NAME,
    url='https://github.com/imbolc/{}'.format(NAME),
    version=VERSION,
    description=DESC,
    long_description=DOC,

    py_modules=[NAME],

    author='Imbolc',
    author_email='imbolc@imbolc.name',
    license='ISC',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python :: 3',
    ],
)
