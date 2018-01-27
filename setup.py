#!/usr/bin/env python
# pylint: disable=C0111,C0103
from setuptools import setup
from setuptools import find_packages

import versioneer

version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()


setup(
    name='biblishelf',
    version=version,
    install_requires=[
        "cement",
    ],
    packages=find_packages('src'),
    package_dir={
        "": "src",
    },
    package_data={
        "": [],
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
            'bib = biblishelf_core.loader:command_entry',
        ],
    },
    cmdclass=cmdclass,
)
