from .module import Module

DEFAULT_CONFIG = {
	'Lock': {
		'exec': '~/.config/i3/scripts/i3lock.sh',
	}
}

class Lock(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Lock', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText('')

	def on_click(self):
		self.stbar.exec(self.config[self.name]['exec'])

def init(stbar, parent_bar): return Lock(stbar, parent_bar)