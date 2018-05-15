from .module import Module
from psutil import virtual_memory
import re

DEFAULT_CONFIG = {
	'Memory': {
		'interval': 5,
		'icon': '',
		'format': '[icon] [percent]'
	}
}

class Memory(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Memory', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText(self.get_text())

	def get_text(self):
		text = self.config[self.name]['format']
		text = re.sub(r'\[icon\]', self.config[self.name]['icon'], text)
		text = re.sub(r'\[percent\]', str(int(virtual_memory().percent)), text)

		return text

	def run(self):
		while True:
			self.setText(self.get_text())
			self.sleep(self.config[self.name]['interval'])


def init(stbar, parent_bar): return Memory(stbar, parent_bar)