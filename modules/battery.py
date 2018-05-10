from .module import Module
import re

PATH_TO_BATTERY = '/sys/class/power_supply/BAT1/'

DEFAULT_CONFIG = {
	'Battery': {
		'charging-icon': '',
		'10%-icon':  '',
		'25%-icon':  '',
		'50%-icon':  '',
		'75%-icon':  '',
		'100%-icon': '',
		
		'charging-format': '[icon] [percent]',
		'draining-format': '[icon] [percent]',

		'interval': 1,
		'exec': 'xfce4-power-manager -c'
	}
}

class Battery(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Battery', stbar, parent_bar, DEFAULT_CONFIG)

	def get_icon(self, percent, discharging):
		icon_name = 'charging-icon'

		if discharging:
			if percent > 75:
				icon_name = '100%-icon'
			elif percent > 50:
				icon_name = '75%-icon'
			elif percent > 25:
				icon_name = '50%-icon'
			elif percent > 10:
				icon_name = '25%-icon'
			else:
				icon_name = '10%-icon'

		return self.config[self.name][icon_name]

	def run(self):
		while True:
			items = ['energy_now', 'energy_full', 'status']

			script = 'cat {}{}'.format(PATH_TO_BATTERY, 'uevent')

			output, error = self.exec(script)
			if error:
				print(error)
			else:

				'''
				dumps a bunch of battery info into a dictionary

				POWER_SUPPLY_NAME, POWER_SUPPLY_STATUS, POWER_SUPPLY_PRESENT, POWER_SUPPLY_TECHNOLOGY,
				POWER_SUPPLY_CYCLE_COUNT, POWER_SUPPLY_VOLTAGE_MIN_DESIGN, POWER_SUPPLY_VOLTAGE_NOW, 
				POWER_SUPPLY_POWER_NOW, POWER_SUPPLY_ENERGY_FULL_DESIGN, POWER_SUPPLY_ENERGY_FULL,
				POWER_SUPPLY_ENERGY_NOW, POWER_SUPPLY_CAPACITY, POWER_SUPPLY_CAPACITY_LEVEL,
				POWER_SUPPLY_MODEL_NAME, POWER_SUPPLY_MANUFACTURER, POWER_SUPPLY_SERIAL_NUMBER
				'''
				info = dict([(x.split('=')) for x in output.strip('\n').split('\n')])
				
				percentage = int(int(info['POWER_SUPPLY_ENERGY_NOW']) / int(info['POWER_SUPPLY_ENERGY_FULL']) * 100)
				
				text = ''
				
				discharging = info['POWER_SUPPLY_STATUS'] == 'Discharging'

				text = self.config[self.name]['draining-format' if discharging else 'charging-format']
				text = re.sub(r'\[icon\]', self.get_icon(percentage, discharging), text)
				text = re.sub(r'\[percent\]', str(percentage), text)

				self.setText(text)

			self.sleep(self.config[self.name]['interval'])

	def on_click(self):
		self.exec(self.config[self.name]['exec'])

def init(stbar, parent_bar): return Battery(stbar, parent_bar)
