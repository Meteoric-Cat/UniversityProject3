import sys
from PySide2 import QtCore as qtcore 
from PySide2 import QtWidgets as qtw

import central_view

WINDOW_W = 1600
WINDOW_H = 1000

class MainWindow(qtw.QWidget):
	def __init__(self):
		super().__init__()

		self.setWindowTitle("Hello world")
		self.layout = central_view.CentralView()
		self.setLayout(self.layout)

app = qtw.QApplication()

mainWindow = MainWindow()
mainWindow.resize(WINDOW_W, WINDOW_H)
mainWindow.show()

sys.exit(app.exec_())

