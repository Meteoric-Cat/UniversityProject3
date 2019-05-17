import sys
from PySide2 import QtCore as qtcore
from PySide2 import QtWidgets as qtw 
from PySide2 import QtGui as qtgui 

import child_layout1 as cl1 
import child_layout2 as cl2

from constants import CHILD_LAYOUT_W, CHILD_LAYOUT_H, IMAGE_W, IMAGE_H
from constants import CHILD1_TO_CHILD2, CHILD2_TO_CHILD1

class CentralView(qtw.QHBoxLayout):
	def __init__(self):
		super().__init__()

		self.dataReference = None
		
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
		self.childLayout1 = cl1.ChildLayout1(self)
		self.childLayout1.setMinimumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout1.setMaximumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)		

		self.childLayout2 = cl2.ChildLayout2(self)
		self.childLayout2.setMinimumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout2.setMaximumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)

		self.addWidget(self.childLayout1)

	def display_image(self, image):
		#self.pixmap.swap(qtgui.QPixmap(image))	
		self.image.setPixmap(qtgui.QPixmap(image))
		self.image.update()

	def remove_widget(self, widget):
		self.removeWidget(widget)
		widget.hide()

	def add_widget(self, widget):
		self.addWidget(widget)
		widget.show()

	def switch_child_layout(self, mode):
		if (mode == CHILD1_TO_CHILD2):
			self.remove_widget(self.childLayout1)
			self.add_widget(self.childLayout2)
		else:
			self.remove_widget(self.childLayout2)
			self.add_widget(self.childLayout1)

		self.update()

