#!/usr/bin/python3
from setuptools import setup, find_packages
import os


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# version number
version = "0.1.0"


setup(
    # package data
    name='dclutter',
    version=version,
    packages=find_packages(exclude=("test",)),
    package_data={},
    python_requires='~=3.6',
    install_requires=[
        'numpy>=1,<2',
        'dtm>=0.2,<0.3',
        'qats>=4,<5'
    ],
    entry_points={
        'console_scripts': [],
        'gui_scripts': []
    },
    zip_safe=True,

    # meta data
    author='Per Voie',
    description='Cleans data to ensure validity and uniformity.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    url='https://github.com/equinor/simpos',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
