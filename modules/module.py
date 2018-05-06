from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QThread

class Module(QPushButton, QThread):
	def __init__(self, name, stbar, parent_bar, default_config={}):
		QPushButton.__init__(self, parent_bar)
		QThread.__init__(self)

		self.name = name
		self.config = stbar.deep_update(default_config, stbar.config)
		self.show()

		if hasattr(self, 'run'):
			self.start()

		if 'exec' in self.config[self.name]:
			self.clicked.connect(self.on_click)