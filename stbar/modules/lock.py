from .module import Module
from PySide2.QtWidgets import QMessageBox

DEFAULT_CONFIG = {
	'Lock': {
		'exec': '~/.config/i3/scripts/i3lock.sh',
	}
}

class Lock(Module):
	def __init__(self, stbar, parent_bar):
		Module.__init__(self, 'Lock', stbar, parent_bar, DEFAULT_CONFIG)

		self.setText('')

		self.init_menu()
		self.add_menu_action('Lock', self.on_click)
		self.add_menu_action('Shutdown', self.shutdown)
		self.add_menu_action('Restart', self.restart)
		self.add_menu_action('Logout', self.logout)

	def on_click(self):
		self.exec(self.config[self.name]['exec'])

	def shutdown(self):
		diag = QMessageBox()
		diag.setText("Shutdown computer?")
		diag.setDefaultButton(QMessageBox.No)
		diag.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		if diag.exec() == QMessageBox.Yes:
			self.exec('shutdown -h now')

	def restart(self):
		diag = QMessageBox()
		diag.setText("Restart computer?")
		diag.setDefaultButton(QMessageBox.No)
		diag.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		if diag.exec() == QMessageBox.Yes:
			self.exec('shutdown -r now')

	def logout(self):
		diag = QMessageBox()
		diag.setText("Logout?")
		diag.setDefaultButton(QMessageBox.No)
		diag.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
		if diag.exec() == QMessageBox.Yes:
			session = self.exec("loginctl session-status | head -n 1 | awk '{print $1}'")
			self.exec('loginctl terminate-session ' + session)

		

def init(stbar, parent_bar): return Lock(stbar, parent_bar)
