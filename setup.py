# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import re, ast

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in travel_agency/__init__.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('travel_agency/__init__.py', 'rb') as f:
	version = str(ast.literal_eval(_version_re.search(
		f.read().decode('utf-8')).group(1)))

setup(
	name='travel_agency',
	version=version,
	description='ERPNext Module for Travel Agents',
	author='Element Labs',
	author_email='saeed@elementlabs.xyz',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
