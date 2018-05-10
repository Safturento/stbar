from .module import Module
from PySide2.QtCore import QProcess

DEFAULT_CONFIG = {
	'Wifi': {
		'interval': 1,
		'icon': ''
	}
}

class Wifi(Module):
	proc = QProcess()

	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Wifi', stbar, parent_bar, DEFAULT_CONFIG)

	def run(self):
		while True:
			output = self.exec('nmcli -t -f active,ssid dev wifi')[0].strip('\n').split(':')
			if output[0] == 'yes':
				self.setText('{} {}'.format(self.config[self.name]['icon'], output[1]))
				self.setProperty('connected', True)
			else:
				self.setText(self.config[self.name]['icon'])
				self.setProperty('connected', False)
			self.sleep(self.config[self.name]['interval'])

	def on_click(self):
		self.proc.start('nm-connection-editor')

def init(stbar, parent_bar): return Wifi(stbar, parent_bar)