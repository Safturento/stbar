from PySide2.QtWidgets import QPushButton
from PySide2.QtCore import QThread

DEFAULT_CONFIG = {
	'Battery': {
		'charging-icon': ''
		'10%-icon':  ''
		'25%-icon':  ''
		'50%-icon':  ''
		'75%-icon':  ''
		'100%-icon': ''
		'charging-format':'[icon][percent]'
		'draining-format':'[icon][percent][time]'

		'exec': 'xfce4-power-manager -c'
	}
}

class Battery(QPushButton, QThread):
	def __init__(self, stbar, parent_bar):
		QPushButton.__init__(self, parent_bar)
		QThread.__init__(self)

		self.name = 'Battery'
		self.config = stbar.deep_update(DEFAULT_CONFIG, stbar.config)
		self.setText('text')
		self.clicked.connect(self.on_click)

	def run(self):
		while True:
			self.sleep(self.config[self.name]['interval'])
			output = self.stbar.exec('upower -i $(upower -e | grep 'BAT') | grep -E "state|to\ full|percentage"')
			self.setText(output)

	def on_click(self):
		self.stbar.exec(self.config[self.name]['exec'])

def init(stbar, parent_bar, config): return Battery(stbar, parent_bar, config)
