import sys
from PySide2 import QtCore as qtcore
from PySide2 import QtWidgets as qtw 
from PySide2 import QtGui as qtgui 

import child_layout1 as cl1 

IMAGE_W = 1200
IMAGE_H = 1000

CHILD_LAYOUT_W = 400
CHILD_LAYOUT_H = 1000

class CentralView(qtw.QHBoxLayout):
	def __init__(self):
		super().__init__()

		self.create_components()

	def create_components(self):
		# self.layout = qtw.QBoxLayout(qtw.QBoxLayout.LeftToRight)
		# self.setLayout(self.layout)

		self.create_image()
		self.create_child_layout()

	def create_image(self):
		self.image = qtw.QLabel()
		self.image.setMinimumSize(IMAGE_W, IMAGE_H)
		self.image.setMaximumSize(IMAGE_W, IMAGE_H)		
		self.addWidget(self.image)
		self.image.setAlignment(qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		self.image.show()

		#self.pixmap = qtgui.QPixmap(1200, 1000)
		#self.image.setPixmap(self.pixmap)

	def create_child_layout(self):	
		self.childLayout = cl1.ChildLayout1(self)
		self.childLayout.setMinimumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout.setMaximumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.addWidget(self.childLayout)

	def display_image(self, image):
		#self.pixmap.swap(qtgui.QPixmap(image))	
		self.image.setPixmap(qtgui.QPixmap(image))
		self.image.update()




