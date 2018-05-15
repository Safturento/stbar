from .module import Module
from PySide2.QtCore import QProcess
import re
import pulsectl

DEFAULT_CONFIG = {
	"Sound": {
		'exec': 'pavucontrol',
		'interval': .1,
		'format': '[icon] [percent]',

		'icon-muted': '',
		'icon-speakers': '',
		'icon-bluetooth': '',
		'icon-headphones': ''
	}
}

class Sound(Module):
	proc = QProcess()

	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Sound', stbar, parent_bar, DEFAULT_CONFIG)

	def get_default_sink(self):
		default_sink_name = self.pulse.server_info().default_sink_name

		return self.pulse.get_sink_by_name(default_sink_name)

	def get_volume_percent(self, force_single = False):
		'''
		If channels are at different volumes this returns
		a bar separated string of the volumes, otherwise
		it just returns the volume percent
		'''
		default_sink = self.get_default_sink()
		volume = ['{:.0f}'.format(x*100) for x in default_sink.volume.values]

		if len(set(volume)) == 1 or force_single:
			return volume[0]			

		return '|'.join(volume)

	def get_icon(self):
		'''
		Returns the correct icon based on source information
		and muted status
		'''
		default_sink = self.get_default_sink()

		icon = self.config[self.name]['icon-speakers']

		if re.search('bluez', default_sink.name):
			icon = self.config[self.name]['icon-bluetooth']

		if re.search('headphone', default_sink.port_active.name.lower()):
			icon = self.config[self.name]['icon-headphones']

		if default_sink.mute:
			icon = self.config[self.name]['icon-muted']

		return icon

	def get_string(self):
		'''
		Creates a string based on config format
		'''
		text = self.config[self.name]['format']
		text = re.sub(r'\[icon\]', self.get_icon(), text)
		text = re.sub(r'\[percent\]', self.get_volume_percent(), text)

		return text

	def on_click(self):
		self.proc.start(self.config[self.name]['exec'])

	def update(self, event):
		'''
		Doing this allows pulsectl to pause and run the rest of the loop
		without having thread issues. More info can be found at
		https://github.com/mk-fg/python-pulse-control#usage
		'''
		raise pulsectl.PulseLoopStop

	def run(self):
		self.pulse = pulsectl.Pulse('stbar')
		while True:
			self.setText(self.get_string())
			
			self.pulse.event_mask_set('all')
			self.pulse.event_callback_set(self.update)
			self.pulse.event_listen(.1)


def init(stbar, parent_bar): return Sound(stbar, parent_bar)