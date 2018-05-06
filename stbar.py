#!/usr/bin/env python3

import sys
import signal
import importlib

from subprocess import call
from pathlib import PosixPath
from json import load, JSONDecodeError
from xrdb import parse_colors


from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *

# Ensure that ctrl + c properly kills the bar
signal.signal(signal.SIGINT, signal.SIG_DFL)

CONFIG_PATH = PosixPath('~/.config/stbar').expanduser()

DEFAULT_CONFIG = {
	"modules":{
		"left": [],
		"center": ["Clock"],
		"right": ["Lock"]
	}
}

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
			bar = QLabel("", self)
			bar.setObjectName('bar_' + bar_name)
			
			bar.layout = QHBoxLayout()
			bar.layout.setAlignment(alignment)
			bar.layout.setMargin(0)
			bar.layout.setSpacing(0)

			bar.setLayout(bar.layout)
			bar.show()
			
			self.layout.addWidget(bar)
			self.bar[bar_name] = bar

		stylesheet = ''.join([line for line in open('style.css', 'r')])

		try:
			stylesheet += ''.join([line for line in open(CONFIG_PATH.joinpath('style.css'), 'r')])
		except: print('No user stylesheet found. Loading defaults')
		
		stylesheet = parse_colors(stylesheet)
		self.setStyleSheet(stylesheet)
		
		self.setWindowTitle('stbar')
		self.load_modules()

	def move(self): pass

	def start(self):
		self.show()
		self.app.exec_()

	def exec(self, script):
		'''
		little helper script to pass execution from buttons
		'''
		return call(str(PosixPath(script).expanduser()).split())

	def deep_update(self, original, update):
	    """
	    Recursively update a dict.
	    Subdict's won't be overwritten but also updated.
	    """
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
			if input().lower() is not 'y':
				sys.exit()
		except IOError:
			print('No config found, loading with defaults')

		# If the user config didn't exist, just return defaults
		return DEFAULT_CONFIG

	def load_modules(self):
		for bar_name in self.bar:
			for module_name in self.config['modules'][bar_name]:
				module_import = importlib.import_module('modules.' + module_name.lower())
				module = module_import.init(self, self.bar[bar_name])
				self.bar[bar_name].layout.addWidget(module)
				print('Loaded', module.name)

if __name__ == '__main__':
	app = QApplication([])
	app.setApplicationDisplayName('stbar')
	stbar(app).start()
