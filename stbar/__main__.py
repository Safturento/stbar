from PySide2.QtWidgets import QApplication
from .stbar import stbar

def main():
	app = QApplication([])
	app.setApplicationDisplayName('stbar')
	print('stbar started')
	stbar(app).start()

if __name__ == '__main__':
	main()