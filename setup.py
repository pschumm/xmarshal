#!/usr/bin/env python3
# -*- coding: utf-8 -*

from setuptools import setup, find_packages
import os

setup(
    name = 'xmarshal',
    version = '0.0.1a2',
    description = 'A Python XML parser that uses existing schema to create Python objects from XML data.',
    long_description = open('README.md').read(),
    url = 'https://github.com/hexdump/xmarshal',
    author = 'hexdump',
    author_email = 'contact@hexdump.email',
    license = 'MIT',
    packages=['xmarshal'],
    install_requires=['untangle']
)
    
    
    
