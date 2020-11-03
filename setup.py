# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md', 'r') as rf:
    README = rf.read()

install_requirements = [
    # General utilities
    'boto3==1.16.9',
    'filetype==1.0.7',
]

setup(
    name='yas3',
    version='1.0',
    description='Yet another simple S3 management tool for python.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='David Chan',
    author_email='davidchan@berkeley.edu',
    url='https://github.com/DavidMChan/yas3',
    license='Apache-2',
    install_requires=install_requirements,
    packages=find_packages(exclude='example'),  # exclude=('tests', 'docs'),
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Typing :: Typed",
    ],
)
