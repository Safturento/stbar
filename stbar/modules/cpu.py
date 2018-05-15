from .module import Module
from psutil import cpu_percent
import re

DEFAULT_CONFIG = {
	'Cpu': {
		'interval': 5,
		'icon': '',
		'format': '[icon] [percent]'
	}
}

class Cpu(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Cpu', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText(self.get_text())

	def get_text(self):
		text = self.config[self.name]['format']
		text = re.sub(r'\[icon\]', self.config[self.name]['icon'], text)
		text = re.sub(r'\[percent\]', str(int(cpu_percent())), text)

		return text

	def run(self):
		while True:
			self.setText(self.get_text())
			self.sleep(self.config[self.name]['interval'])


def init(stbar, parent_bar): return Cpu(stbar, parent_bar)