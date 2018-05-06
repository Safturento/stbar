from PySide2.QtWidgets import QPushButton

DEFAULT_CONFIG = {
	'Lock': {
		'exec': '~/.config/i3/scripts/i3lock.sh',
	}
}

class Lock(QPushButton):
	def __init__(self, stbar, parent_bar):
		QPushButton.__init__(self, parent_bar)

		self.setText('')

		self.name = 'Lock'
		self.stbar = stbar
		self.config = stbar.deep_update(DEFAULT_CONFIG, stbar.config)
		self.clicked.connect(self.on_click)
		self.show()

	def on_click(self):
		self.stbar.exec(self.config[self.name]['exec'])

def init(stbar, parent_bar): return Lock(stbar, parent_bar)