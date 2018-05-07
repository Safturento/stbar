from PySide2.QtWidgets import QWidget
from PySide2.QtCore import QThread

# import socket, os
import i3ipc

DEFAULT_CONFIG = {
	'I3': {

	}
}

class I3(QWidget, QThread):
	def __init__(self, stbar, parent_bar):
		QWidget.__init__(self, parent_bar)
		QThread.__init__(self)

		self.stbar = stbar
		self.parent_bar = parent_bar
		self.name = 'I3'
		self.config = stbar.deep_update(DEFAULT_CONFIG, stbar.config)
		self.show()
		self.start()

		self.layout = QHBoxLayout()

		self.buttons = {}

	def run(self):
		i3 = i3ipc.Connection()
		
		for i in i3.get_workspaces():
			print(i)

		i3.on('workspace::focus', self.on_workspace_focus)

		i3.main()

		self.i3 = i3

	def on_workspace_focus(self, i3, event):
		for i in i3.get_workspaces():
			print(i)

	def on_window_focus(self, i3, event):
		pass

def init(stbar, parent_bar): return I3(stbar, parent_bar)