#!/usr/bin/env python3

import setuptools

setuptools.setup(
	name='stbar',
	version='1.0',
	description='Taskbar for linux tiling window managers',
	# author='Jean-Michel Mailloux-Huberdeau',
	url='https://github.com/Safturento/stbar',
	packages=['stbar', 'stbar.modules'],
	package_data={'stbar':['style.css']},
	include_package_data=True,
	install_requires=['i3ipc', 'PySide2']
)