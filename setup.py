#!/usr/bin/python3
from setuptools import setup, find_packages
from setuptools.command.install import install

import os

class PostInstall(install):
	def run(self):
		'''populate config folder'''
		
		from stbar.stbar import CONFIG_PATH
		
		# Check root config folder
		if not os.path.exists(CONFIG_PATH):
			os.mkdir(CONFIG_PATH)

		# Check modules folder
		if not os.path.exists(CONFIG_PATH.joinpath('modules')):
			os.mkdir(CONFIG_PATH.joinpath('modules'))

		# Check config file
		if not os.path.exists(CONFIG_PATH.joinpath('config')):
			with open(CONFIG_PATH.joinpath('config'), 'a') as file:
				file.write('{\n\n}')

		# Check style file
		with open(CONFIG_PATH.joinpath('style.css'), 'a') as file: pass

setup(
	name = 'stbar',
	version = '0.2.2',
	description = 'Taskbar for linux tiling window managers',
	# author = 'Jean-Michel Mailloux-Huberdeau',
	url = 'https://github.com/Safturento/stbar',
	packages = find_packages(),
	package_data = {'stbar': ['style.css']},
	include_package_data = True,
	install_requires = ['i3ipc', 'PySide2'],
	entry_points = {'console_scripts': ['stbar=stbar.__main__:main']},
	cmdclass = { 'install': PostInstall }
)