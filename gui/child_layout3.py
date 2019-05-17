from PySide2 import QtCore as qtcore
from PySide2 import QtWidgets as qtw 
from PySide2 import QtGui as qtgui 

import file_system_manager as fm 

IMAGE_SIZE=(100, 100)
SCROLL_SIZE=(1200, 1000)
BOARD_SIZE=(1200, 2000)

class ImageBoard(qtw.QScrollArea):
	def __init__(self):
		super().__init__()
		
		self.images = []
		self.spacer = qtw.QSpacerItem(IMAGE_SIZE[0], IMAGE_SIZE[1])
		
		self.setMinimumSize(SCROLL_SIZE[0], SCROLL_SIZE[1])
		self.setMaximumSize(SCROLL_SIZE[0], SCROLL_SIZE[1])

		self.create_content_area()

	def create_content_area(self):
		self.content = qtw.QWidget()
		self.content.setMinimumSize(BOARD_SIZE[0], BOARD_SIZE[1])
		self.content.setMinimumSize(BOARD_SIZE[0], BOARD_SIZE[1])

		self.contentLayout = qtw.QGridLayout()
		self.content.setLayout(self.contentLayout)

		self.setWidget(self.content)

	def update_images(self, images_info):
		count = 0
		for imageInfo in images_info:			
			path = fm.write_temp_image(imageInfo[1])
			if (len(self.images) <= count):
				image = Image(imageInfo[0])
				self.images.append(image)

			self.images[count].add_image(path)
			self.contentLayout.addWidget(self.images[count], int(count / 12), count % 12, 1, 1)
			self.contentLayout.setAlignment(self.images[count], qtcore.Qt.AlignTop | qtcore.Qt.AlignLeft)
			count += 1
		
		spacerColumn = 12 - count % 12
		if (spacerColumn != 0):
			self.spacer.changeSize(IMAGE_SIZE[0] * spacerColumn, IMAGE_SIZE[1])
			self.contentLayout.addItem(self.spacer, int(count / 12), count % 12, 1, spacerColumn)

class Image(qtw.QLabel):
	def __init__(self, person_id):
		super().__init__()

		self.personId = person_id

		self.setMaximumSize(IMAGE_SIZE[0], IMAGE_SIZE[1])
		self.setMinimumSize(IMAGE_SIZE[0], IMAGE_SIZE[1])

	def add_image(self, file_name):
		self.setPixmap(qtgui.QPixmap(file_name))
		self.update()