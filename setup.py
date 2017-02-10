#!/usr/bin/env python
import os
import subprocess

from setuptools import setup
from setuptools import find_packages
from setuptools.command.develop import develop as _develop
from setuptools.command.install import install as _install


setup(
    name='biblishelf',
    version = "0.1.0",
    install_requires=[
        "cement",
    ],
    packages=find_packages('src'),
    package_dir={
        "": "src"
    },
    package_data={
        "": []
    },
    description="a file ",
    author="xingci xu",
    author_email="x007007007@hotmail.com",
    license='MIT license',
    url='',
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    entry_points={
        'console_scripts': [
            'biblishelf_cli = biblishelf_cli.main:main',
        ]
    }
)