from .module import Module
from PySide2.QtCore import QProcess

DEFAULT_CONFIG = {
	"Sound": {
		'exec': 'pavucontrol'
	}
}

class Sound(Module):
	proc = QProcess()

	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Sound', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText('')

	def on_click(self):
		self.proc.start(self.config[self.name]['exec'])

	def run(self): pass
		# print(self.get_sinks())

	def get_sinks(self):
		info = ['index', 'muted', 'alias', 'card_name', 'priority:', 'volume']
		script = 'pacmd list-sinks | awk \'' + ''.join(['/' + x + '/ {print $0}' for x in info]) + '\''
		return self.exec(script)[0]

def init(stbar, parent_bar): return Sound(stbar, parent_bar)