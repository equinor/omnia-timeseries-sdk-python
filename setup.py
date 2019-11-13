#!/usr/bin/python3
from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    # package data
    name='omnia_timeseries_sdk',
    use_scm_version=True,
    packages=find_packages(exclude=('test',)),
    package_data={},
    python_requires='~=3.7',
    setup_requires=['setuptools_scm'],
    install_requires=[
        'matplotlib>=3,<4',
        'adal>=1,<2',
        'pandas>=0.25.3,<1',
    ],
    zip_safe=True,

    # meta data
    author='Per Voie',
    description='Python software developer kit for the Omnia Timeseries API.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/equinor/omnia-timeseries-sdk-python',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
