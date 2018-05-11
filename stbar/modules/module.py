from PySide2.QtWidgets import QWidget, QPushButton, QMenu, QAction
from PySide2.QtCore import QThread, QPoint, Qt, Signal

from subprocess import call, Popen, PIPE
from pathlib import PosixPath
import re

class Module(QPushButton, QThread):
	update_signal = Signal(QWidget)

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

	def init_menu(self):
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.menu = QMenu(self.stbar)
		self.customContextMenuRequested.connect(self.on_context_menu)

	def add_menu_action(self, name, function):
		action = QAction(name, self)
		action.triggered.connect(function)
		self.menu.addAction(action)

		return action

	def on_context_menu(self, point):		
		# self.setAttribute(Qt.WA_Hover, False)
		pos = self.get_menu_point('BOTTOMRIGHT', 'TOPRIGHT', 0, -5)
		self.menu.exec_(pos)

	def get_menu_point(self, button_position, menu_position, xOffset = 0, yOffset = 0):
		''' 
			Calculates offsets for positioning menu relative to button. For example, if you want
			the menu to have it's top right anchored to the bottom right of the button you would call

			self.get_point(point, 'TOPRIGHT', 'BOTTOMRIGHT')
		'''

		button_position = button_position.upper()
		menu_position = menu_position.upper()

		# start at topleft of of button
		global_pos = self.mapToGlobal(QPoint(0,0))

		# Get the alignment relative to the button
		button_position_y = re.search('.?(TOP|BOTTOM).?', button_position)
		if button_position_y: button_position_y = button_position_y.groups()[0]

		button_position_x = re.search('.?(LEFT|RIGHT).?', button_position)
		if button_position_x: button_position_x = button_position_x.groups()[0]

		# Get the alignment of the menu
		menu_position_y = re.search('.?(TOP|BOTTOM).?', menu_position)
		if menu_position_y: menu_position_y = menu_position_y.groups()[0]

		menu_position_x = re.search('.?(LEFT|RIGHT).?', menu_position)
		if menu_position_x: menu_position_x = menu_position_x.groups()[0]


		if button_position_x == 'RIGHT':
			xOffset += self.width()

		if button_position_y == 'BOTTOM':
			yOffset += self.height()

		if menu_position_x == 'RIGHT':
			xOffset -= self.menu.width()

		if menu_position_y == 'BOTTOM':
			yOffset -= self.menu.height()


		global_pos.setX(global_pos.x() + xOffset)
		global_pos.setY(global_pos.y() + yOffset)

		return global_pos

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
