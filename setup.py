#!/usr/bin/env python

from setuptools import setup

setup(
    name='github-download-dependents-info',
    version='0.1.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': ['github-download-dependents-info = main:main']
    },
)
