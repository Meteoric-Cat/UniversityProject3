import sys
from PySide2 import QtCore as qtcore 
from PySide2 import QtWidgets as qtw

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Hello world")
		self.layout = qtw.QBoxLayout(qtw.QBoxLayout.LeftToRight)
		self.setLayout(self.layout)

if (__name__ == "__main__"):
	app = qtw.QApplication()

	mainWindow = MainWindow()
	mainWindow.resize(1400, 1000)
	mainWindow.show()

	sys.exit(app.exec_())

