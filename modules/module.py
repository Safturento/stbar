from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QThread

from subprocess import call, Popen, PIPE
from pathlib import PosixPath

class Module(QPushButton, QThread):
	def __init__(self, name, stbar, parent_bar, default_config={}):
		QPushButton.__init__(self, parent_bar)
		QThread.__init__(self)

		self.stbar = stbar
		self.parent_bar = parent_bar
		self.name = name
		self.setObjectName(name)
		self.config = stbar.deep_update(default_config, stbar.config)
		self.show()
		if hasattr(self, 'on_click'):
			self.clicked.connect(self.on_click)

		if hasattr(self, 'run'):
			self.start()

	def exec(self, script):
		'''
		little helper script to pass execution from buttons
		'''

		parts = script.split('|')
		p = []
		for i, part in enumerate(parts):
			args = str(PosixPath(script).expanduser()).split()
			if i == 0:
				p.append(Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE))
			else:
				p.append(Popen(args, stdin=p[i-1].stdout, stdout=PIPE, stderr=PIPE))
		output, error = p[-1].communicate()

		return output.decode('utf-8'), False if error is '' else error
