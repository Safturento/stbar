from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QThread
from time import strftime

DEFAULT_CONFIG = {
	'Clock': {
		'format': '%H:%M:%S',
		'interval': 1
	}
}

class Clock(QPushButton, QThread):
	def __init__(self, stbar, parent_bar):
		QPushButton.__init__(self, parent_bar)
		QThread.__init__(self)

		self.name = 'Clock'
		self.config = stbar.deep_update(DEFAULT_CONFIG, stbar.config)
		self.setText(strftime(self.config[self.name]['format']))
		self.show()
		self.start()

	def run(self):
		while True:
			self.sleep(self.config[self.name]['interval'])
			self.setText(strftime(self.config[self.name]['format']))

def init(stbar, parent_bar): return Clock(stbar, parent_bar)