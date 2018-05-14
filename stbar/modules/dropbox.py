from .module import Module
import re

DEFAULT_CONFIG = {
	'Dropbox': {
		'interval': 1,
		'disabled-icon': '!',
		'starting-icon': '',
		'syncing-icon': '',
		'normal-icon': '',
		'script-path': 'dropbox'
	}
}

class Dropbox(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Dropbox', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText(self.config[self.name]['normal-icon'])

	def run(self):
		while True:
			self.sleep(self.config[self.name]['interval'])

			output, error = self.exec('{} status'.format(self.config[self.name]['script-path']))
			if error:
				self.setText('Dropbox not found!')
			else:
				status = re.search(r'(not started|starting|syncing|up to date)', output.lower())
				if status:
					if status[0] == 'not started':
						self.setText(self.config[self.name]['disabled-icon'])
					elif status[0] == 'starting':
						self.setText(self.config[self.name]['starting-icon'])
					elif status[0] == 'syncing':
						self.setText(self.config[self.name]['syncing-icon'])
					elif status[0] == 'up to date':
						self.setText(self.config[self.name]['normal-icon'])
				else:
					self.setText(status)


def init(stbar, parent_bar): return Dropbox(stbar, parent_bar)