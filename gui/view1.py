import sys
from PySide2 import QtCore as qtcore
from PySide2 import QtWidgets as qtw 

class View1(qtw.QHBoxLayout):
	def __init__(self):
		super().__init__()

		self.create_components()
		self.add_handlers()

	def create_components():
		# self.layout = qtw.QBoxLayout(qtw.QBoxLayout.LeftToRight)
		# self.setLayout(self.layout)

		self.image = qtw.QLabel("nothing")
		self.addWidget(self.image)

		self.childLayout = qtw.QBoxLayout(qtw.QBoxLayout.TopToBottom)
		self.addWidget(self.childLayout)

		self.inputButton = qtw.QPushButton("Recognize")
		self.updateButton = qtw.QPushButton("Recognize")

		self.childLayout.addWidget(self.inputButton)
		self.childLayout.addWidget(self.updateButton)

	def add_handlers():





