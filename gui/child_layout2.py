from PySide2 import QtCore as qtcore 
from PySide2 import QtWidgets as qtw 

from constants import BUTTON_H, BUTTON_W, CHILD2_TO_CHILD1

import database_manager as db 
import file_system_manager as fm 
import system_updater as su 

LAYER2_SIZE = (400, 600)
LAYER2_EDITOR_SIZE = (300, 50)

class ChildLayout2(qtw.QWidget):
	def __init__(self, parent):
		super().__init__()

		self.parent = parent
		self.facesInfo = -1
		self.doneSaving = False

		self.create_layer1()
		self.create_layer2()

	def create_layer1(self):
		self.layout1 = qtw.QVBoxLayout()
		self.setLayout(self.layout1)

		self.layer2 = qtw.QWidget()
		self.layout2 = qtw.QGridLayout()
		self.layer2.setMinimumSize(LAYER2_SIZE[0], LAYER2_SIZE[1])
		self.layer2.setMaximumSize(LAYER2_SIZE[0], LAYER2_SIZE[1])	
		self.layer2.setLayout(self.layout2)
		self.layout1.addWidget(self.layer2)

		self.create_buttons()
		self.create_distlabels()

	def create_buttons(self):
		self.saveButton = qtw.QPushButton("Save")
		self.saveButton.setMaximumSize(BUTTON_W, BUTTON_H)
		self.saveButton.setMinimumSize(BUTTON_W, BUTTON_H)
		self.layout1.addWidget(self.saveButton)
		self.layout1.setAlignment(self.saveButton, qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		# self.layout1.setAlignment(self.saveButton, qtcore.Qt.AlignTop)

		self.cancelButton = qtw.QPushButton("Cancel")
		self.cancelButton.setMinimumSize(BUTTON_W, BUTTON_H)
		self.cancelButton.setMaximumSize(BUTTON_W, BUTTON_H)
		self.layout1.addWidget(self.cancelButton)
		self.layout1.setAlignment(self.cancelButton, qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		# self.layout1.setAlignment(self.cancelButton, qtcore.Qt.AlignTop)

		self.saveButton.clicked.connect(self.handle_saving)
		self.cancelButton.clicked.connect(self.handle_canceling)

	def create_distlabels(self):
		self.detectionDistLabel = qtw.QLabel()
		self.detectionDistLabel.setText("Detection dist")
		self.layout1.addWidget(self.detectionDistLabel)
		self.layout1.setAlignment(self.detectionDistLabel, qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		# self.layout1.setAlignment(self.detectionDistLabel, qtcore.Qt.AlignTop)

		self.recognizationDistLabel = qtw.QLabel()
		self.recognizationDistLabel.setText("Recognization dist")
		self.layout1.addWidget(self.recognizationDistLabel)
		self.layout1.setAlignment(self.recognizationDistLabel, qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		# self.layout1.setAlignment(self.recognizationDistLabel, qtcore.Qt.AlignTop)

	def create_layer2(self):
		self.create_infolabels()
		self.create_infoeditors()

	def create_infolabels(self):
		labels = ["Person ID", "Name", "Age", "Occupation"]
		self.infoLabels = []

		for i in range(0, 4):
			self.infoLabel = qtw.QLabel()
			self.infoLabel.setText(labels[i])
			self.infoLabels.append(self.infoLabel)

			self.layout2.addWidget(self.infoLabel, i, 0, 1, 1)

	def create_infoeditors(self):
		self.infoEditors = []

		for i in range(0, 4):
			self.infoEditor = qtw.QLineEdit()
			self.setMinimumSize(LAYER2_EDITOR_SIZE[0], LAYER2_EDITOR_SIZE[1])
			self.infoEditors.append(self.infoEditor)

			self.layout2.addWidget(self.infoEditor, i, 1, 1, 3)

	def get_editors_data(self, start, end):
		result = []
		for i in range(start, end + 1):
			result.append(self.infoEditors[i].text())
		return result

	@qtcore.Slot()
	def handle_saving(self):
		if (self.infoEditors[0].text() == "" or self.imageId == -1):
			print("nothing to do")
			return

		if (self.facesInfo[self.imageId][0] <= -1):
			db.create_people(self.get_editors_data(1, 3))
			self.facesInfo[self.imageId][0] = db.get_max_personid()
			print(self.facesInfo[self.imageId][0])
		else:
			db.update_people(self.get_editors_data(0, 3))

		fm.write_facial_image_to_file(self.facesInfo[self.imageId][0], self.facesInfo[self.imageId][1])
		self.doneSaving = True

	qtcore.Slot()
	def handle_canceling(self):
		if (self.doneSaving):
			self.doneSaving = False
			su.update(self.parent.dataReference)

		self.parent.switch_child_layout(CHILD2_TO_CHILD1)

	def save_faces_info(self, faces_info):
		self.facesInfo = faces_info

	def display_data(self, imageId):
		if (self.facesInfo is None):
			print("something wrong")
			return

		self.imageId = imageId

		if (self.facesInfo[imageId][0] <= 0):
			self.clean_editors_up()
			self.infoEditors[0].setText(str(self.facesInfo[imageId][0]))
		else:
			person = db.get_people(self.facesInfo[imageId][0]).first()
			if not (person is None):
				self.infoEditors[0].setText(str(person.Id))
				self.infoEditors[1].setText(person.Name)
				self.infoEditors[2].setText(str(person.Age))
				self.infoEditors[3].setText(person.Occupation)

		self.detectionDistLabel.setText("Detection dist:" + str(self.facesInfo[imageId][2]))
		self.recognizationDistLabel.setText("Recognization dist:" + str(self.facesInfo[imageId][3]))

	def clean_editors_up(self):
		for editor in self.infoEditors:
			editor.setText("")

		self.detectionDistLabel.setText("")
		self.recognizationDistLabel.setText("")