#!/usr/bin/env python3

import os
import sys
import signal
import importlib

from subprocess import call, Popen, PIPE
from pathlib import PosixPath
from json import load, JSONDecodeError
from .xrdb import parse_colors

from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# Ensure that ctrl + c properly kills the bar
signal.signal(signal.SIGINT, signal.SIG_DFL)

CONFIG_PATH = PosixPath('~/.config/stbar').expanduser()
FILE_PATH = os.path.dirname(__file__)

DEFAULT_CONFIG = {
	'modules':{
		'left': ['I3'],
		'center': ['Clock'],
		'right': ['Sound', 'Battery', 'Wifi', 'Lock']
	}
}

TEXT_COLOR = {
    'HEADER':	 '\033[95m',
    'OKBLUE':	 '\033[94m',
    'OKGREEN':	 '\033[92m',
    'WARNING':	 '\033[93m',
    'FAIL':		 '\033[91m',
    'ENDC':		 '\033[0m',
    'BOLD':		 '\033[1m',
    'UNDERLINE': '\033[4m',
	
}

def color(text, flag):
	return TEXT_COLOR[flag] + text + TEXT_COLOR['ENDC']

class stbar(QWidget):
	
	def __init__(self, app):
		QWidget.__init__(self)
		self.app = app
		self.config = self.load_config()
		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setObjectName('stbar')

		# Nesting the app within a translucent widget allows
		# for transparency in the bar's background.
		# Current requires a compositor like compton
		self.setAttribute(Qt.WA_TranslucentBackground, True)

		self.setAttribute(Qt.WA_X11NetWmWindowTypeDock, True)
		self.setAttribute(Qt.WA_X11DoNotAcceptFocus, True)
		self.layout = QHBoxLayout()
		self.layout.setMargin(0)
		self.layout.setSpacing(0)
		self.setLayout(self.layout)
		
		self.bar = {}
		alignments = [Qt.AlignLeft, Qt.AlignCenter, Qt.AlignRight]
		bar_names = ['left','center','right']

		for bar_name, alignment in zip(bar_names, alignments):
			'''QWidget acts really weird in this scenario, but
			QLabel conforms to css and splitting
			evenly in the QHBoxlayout'''
			bar = QLabel('', self)
			bar.setObjectName('bar_' + bar_name)
			
			bar.layout = QHBoxLayout()
			bar.layout.setAlignment(alignment)
			bar.layout.setMargin(0)
			bar.layout.setSpacing(0)

			bar.setLayout(bar.layout)
			bar.show()
			
			self.layout.addWidget(bar)
			self.bar[bar_name] = bar

		stylesheet = ''.join([line for line in open(FILE_PATH + '/style.css', 'r')])

		try:
			stylesheet += ''.join([line for line in open(CONFIG_PATH.joinpath('style.css'), 'r')])
		except: print('No user stylesheet found. Loading defaults')
		
		stylesheet = parse_colors(stylesheet)
		self.setStyleSheet(stylesheet)
		self.stylesheet = stylesheet
		
		self.setWindowTitle('stbar')
		self.load_modules()

	def start(self):
		self.show()
		self.app.exec_()

	def deep_update(self, original, update):
	    '''
	    Recursively update a dict.
	    Subdict's won't be overwritten but also updated.

	    Parameters
	    ----------
	    original : dict
	    	The dictionary to be updated
	    update : dict
	    	The dictionary to override original with
	    '''
	    for key, value in original.items(): 
	        if key not in update:
	            update[key] = value
	        elif isinstance(value, dict):
	            self.deep_update(value, update[key]) 

	    return update

	# update with user config if available
	def load_config(self):
		# Load up user config if it exists, updating the defaults if needed
		try: 
			return self.deep_update(DEFAULT_CONFIG, load(open(CONFIG_PATH.joinpath('config'), 'r')))
		except JSONDecodeError:
			print('Invalid config file, continue with defaults? [y/n]')
			if input().lower() != 'y':
				sys.exit()
		except IOError:
			print('No config found, loading with defaults')

		# If the user config didn't exist, just return defaults
		return DEFAULT_CONFIG

	@Slot()
	def update_module(self, module, *args, **kwargs):
		module.update(*args, **kwargs)

	def load_module(self, module_import, bar_name):
		module = module_import.init(self, self.bar[bar_name])

		self.bar[bar_name].layout.addWidget(module)
		module.update_signal.connect(self.update_module)
		print(color('Loaded', 'OKGREEN'))

	def load_modules(self):
		for bar_name in self.bar:
			for module_name in self.config['modules'][bar_name]:
				print('Loading {}: '.format(module_name), end='')
				# Attempt to import as user modules. We check user first
				# so that users can override core modules if they wish
				try:
					# attempt to load from user config modules
					module_path = CONFIG_PATH.joinpath('modules', module_name.lower()+'.py')
					spec = importlib.util.spec_from_file_location(module_name, module_path)
					module_import = importlib.util.module_from_spec(spec)
					spec.loader.exec_module(module_import)
					self.load_module(module_import, bar_name)

				except:
					# if loading from user failed try to load as core module
					try:
						module_import = importlib.import_module('stbar.modules.' + module_name.lower())
					
						self.load_module(module_import, bar_name)
					
					except ModuleNotFoundError:
						print(color('Module doesn\'t exist.', 'FAIL'))