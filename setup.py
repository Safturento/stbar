#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
	name = 'stbar',
	version = '0.1.0',
	description = 'Taskbar for linux tiling window managers',
	# author = 'Jean-Michel Mailloux-Huberdeau',
	url = 'https://github.com/Safturento/stbar',
	packages = find_packages(),
	package_data = {'stbar': ['style.css']},
	include_package_data = True,
	install_requires = ['i3ipc', 'PySide2'],
	entry_points = {'console_scripts': ['stbar=stbar.__main__:main']}
)