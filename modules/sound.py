from .module import Module

DEFAULT_CONFIG = {
	"Sound": {
		'exec': 'pavucontrol'
	}
}

class Sound(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Sound', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText('')

	def on_click(self):
		self.stbar.exec(self.config[self.name]['exec'])

def init(stbar, parent_bar): return Sound(stbar, parent_bar)