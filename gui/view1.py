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

		self.create_image()
		self.create_child_layout()

	def create_image():
		self.image = qtw.QLabel("nothing")
		self.image.setMinimumSize(1200, 1000)
		self.image.setMaximumSize(1200, 1000)
		self.addWidget(self.image)

	def display_image(image):
		

	def create_child_layout()
		self.childLayout = qtw.QBoxLayout(qtw.QBoxLayout.TopToBottom)
		self.addWidget(self.childLayout)

		self.inputButton = qtw.QPushButton("Recognize")
		self.updateButton = qtw.QPushButton("Recognize")

		self.childLayout.addWidget(self.inputButton)
		self.childLayout.addWidget(self.updateButton)






