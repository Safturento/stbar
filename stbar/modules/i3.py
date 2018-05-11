from PySide2.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PySide2.QtCore import QThread, Signal, Slot

# import socket, os
import i3ipc

DEFAULT_CONFIG = {
	'I3': {
		'workspaces': {
			1: '',
			2: '',
			3: '',
			4: '',
			5: '',
			6: '',
		}
	}
}


class I3(QWidget, QThread):

	class Workspace(QPushButton):
		def __init__(self, i3, ws_info):
			QPushButton.__init__(self, i3)
			self.num = ws_info['num']

			# bind workspace swap
			self.clicked.connect(lambda x: i3.switch_to_workspace(self))
		
			if 'workspaces' in i3.config[i3.name] and \
			self.num in i3.config[i3.name]['workspaces']:
				self.setText(i3.config[i3.name]['workspaces'][self.num]) 
			else:
				self.setText(str(self.num))

			i3.layout.insertWidget(self.num, self)

		def update_info(self, ws_info):
			self.info = ws_info
			# Update css properties
			self.setProperty('i3visible', ws_info['visible'])
			self.setProperty('i3focused', ws_info['focused'])
			self.redraw()

		def redraw(self):
			self.style().unpolish(self)
			self.style().polish(self)
			self.update()

	def __init__(self, stbar, parent_bar):
		QWidget.__init__(self, parent_bar)
		QThread.__init__(self)

		# Load main module structure
		self.stbar = stbar
		self.parent_bar = parent_bar
		self.name = 'I3'
		self.setObjectName(self.name)
		self.config = stbar.deep_update(DEFAULT_CONFIG, stbar.config)

		# Setup layout for nested workspace buttons
		self.layout = QHBoxLayout()
		self.layout.setMargin(0)
		self.layout.setSpacing(0)
		self.buttons = {}

		# Bind update to main thread
		self.stbar.update.connect(self.update_workspaces)
		
		self.show()
		self.setLayout(self.layout)
		self.start()

	def run(self):
		self.ipc = i3ipc.Connection()
		self.ipc.on('workspace::focus', self.on_workspace_focus)
		# Spoof ipc event to update initially
		self.on_workspace_focus(self.ipc, 'focus')
		self.ipc.main()


	def switch_to_workspace(self, workspace):
		self.ipc.command('workspace {}'.format(workspace.num))

	@Slot(str)
	def update_workspaces(self):
		visible = []
		workspaces = self.ipc.get_workspaces()
		# Make sure all active workspaces have a button created
		for ws_info in self.ipc.get_workspaces():
			if ws_info['num'] not in self.buttons:				
				self.buttons[ws_info['num']] = self.Workspace(self, ws_info)
			visible.append(ws_info['num'])
			self.buttons[ws_info['num']].update_info(ws_info)

		for num, button in self.buttons.items():
			if num in visible:
				button.setVisible(True)
			else:
				button.setVisible(False)

	def on_workspace_focus(self, i3ipc, event):
		self.stbar.update.emit()

def init(stbar, parent_bar): return I3(stbar, parent_bar)