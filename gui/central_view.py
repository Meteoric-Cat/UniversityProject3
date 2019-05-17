import sys
from PySide2 import QtCore as qtcore
from PySide2 import QtWidgets as qtw 
from PySide2 import QtGui as qtgui 

import child_layout1 as cl1 
import child_layout2 as cl2
import child_layout3 as cl3 

from constants import CHILD_LAYOUT_W, CHILD_LAYOUT_H, IMAGE_W, IMAGE_H
from constants import CHILD1_TO_CHILD2, CHILD2_TO_CHILD1

import find_face_candidate3 as fl 
import file_system_manager as fm 

class CentralView(qtw.QHBoxLayout):
	def __init__(self):
		super().__init__()

		self.dataReference = None
		
		self.create_components()

	def create_components(self):
		self.create_layout1()
		self.create_layout2()

	def create_layout1(self):	
		self.image = qtw.QLabel()
		self.image.setMinimumSize(IMAGE_W, IMAGE_H)
		self.image.setMaximumSize(IMAGE_W, IMAGE_H)		
		self.addWidget(self.image)
		self.image.setAlignment(qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		self.image.show()

		self.childLayout1 = cl1.ChildLayout1(self)
		self.childLayout1.setMinimumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout1.setMaximumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)		
		self.addWidget(self.childLayout1)
		self.childLayout1.show()

	def create_layout2(self):
		self.imageBoard = cl3.ImageBoard()
		self.imageBoard.hide()

		self.childLayout2 = cl2.ChildLayout2(self)
		self.childLayout2.setMinimumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout2.setMaximumSize(CHILD_LAYOUT_W, CHILD_LAYOUT_H)
		self.childLayout2.hide()

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
			self.remove_widget(self.image)
			self.add_widget(self.imageBoard)
			self.add_widget(self.childLayout2)
		else:
			self.remove_widget(self.childLayout2)
			self.remove_widget(self.imageBoard)
			self.add_widget(self.image)
			self.add_widget(self.childLayout1)			

		self.update()

	def handle_system_updating(self):
		fileName = qtw.QFileDialog.getOpenFileName(None, self.tr("Choose Image"), "./input")[0]
		faceInfo = fl.detect_faces_to_update_system(fileName, self.dataReference, new_threshold = 3600)

		self.imageBoard.update_images(faceInfo)