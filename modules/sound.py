from .module import Module

DEFAULT_CONFIG = {
	"Sound": {

	}
}

class Sound(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Sound', stbar, parent_bar, DEFAULT_CONFIG)
		self.setText('')


def init(stbar, parent_bar): return Sound(stbar, parent_bar)