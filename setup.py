#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from setuptools import setup, find_packages


setup(
    name='dexsim',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        # 'Click_utils',
        'powerzip',
        'adbwrapper',
        'cigam',
        'pyaml',
        'smafile',
        'smaliemu',
        'timeout3',
    ],
    package_data={
        'dexsim': ['dexsim/data/*', 'dexsim/server/*', 'dexsim/smali/*'],
    },
    entry_points='''
        [console_scripts]
        dexsim=dexsim.cli:main
    ''',
)
