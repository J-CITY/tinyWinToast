from setuptools import setup, find_packages
from os.path import join, dirname

import tinyWinToast

setup(
	name='tinyWinToast',
	version=tinyWinToast.__version__,
	packages=find_packages(),
	url="https://github.com/J-CITY/tinyWinToast",
	long_description=open(join(dirname(__file__), 'README.txt')).read(),
	description=(
		"Tiny Python library for displaying "
		"Windows toasts"
	),
	author="J-CITY (Glushchenko Daniil)"
)