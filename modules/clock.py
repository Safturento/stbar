from .module import Module
from time import strftime

DEFAULT_CONFIG = {
	'Clock': {
		'format': '%H:%M:%S',
		'interval': 1
	}
}

class Clock(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Clock', stbar, parent_bar, DEFAULT_CONFIG)
		
		self.setText(strftime(self.config[self.name]['format']))

	def run(self):
		while True:
			self.setText(strftime(self.config[self.name]['format']))
			self.sleep(self.config[self.name]['interval'])

def init(stbar, parent_bar): return Clock(stbar, parent_bar)