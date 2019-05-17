from PySide2 import QtCore as qtcore 
from PySide2 import QtWidgets as qtw 

import sys

BUTTON_W = 200
BUTTON_H = 40	

class ChildLayout1(qtw.QWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

		self.create_views()
		self.connect_handlers()

	def create_views(self):
		self.layout = qtw.QVBoxLayout()
		self.setLayout(self.layout)

		self.create_recognization_button()
		self.create_update_button()

	def create_recognization_button(self):
		self.recognizationButton = qtw.QPushButton("Recognize")
		self.recognizationButton.setMinimumSize(BUTTON_W, BUTTON_H)
		self.recognizationButton.setMaximumSize(BUTTON_W, BUTTON_H)
		self.layout.addWidget(self.recognizationButton)
		
	def create_update_button(self):
		self.updateButton = qtw.QPushButton("Update database")
		self.updateButton.setMaximumSize(BUTTON_W, BUTTON_H)
		self.updateButton.setMinimumSize(BUTTON_W, BUTTON_H)
		self.layout.addWidget(self.updateButton)

	def connect_handlers(self):
		self.recognizationButton.clicked.connect(self.handle_recognization)				
		self.updateButton.clicked.connect(self.handle_update)

	@qtcore.Slot()
	def handle_recognization(self):
		fileName = qtw.QFileDialog.getOpenFileName(None, self.tr("Choose Image"), "../input")[0]
		self.parent.display_image(fileName)

	@qtcore.Slot()
	def handle_update(self):
		pass


