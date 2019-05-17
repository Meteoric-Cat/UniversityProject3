from PySide2 import QtCore as qtcore 
from PySide2 import QtWidgets as qtw 

from constants import BUTTON_H, BUTTON_W, CHILD2_TO_CHILD1

LAYER2_SIZE = (400, 600)
LAYER2_EDITOR_SIZE = (300, 50)

class ChildLayout2(qtw.QWidget):
	def __init__(self, parent):
		super().__init__()
		self.parent = parent

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
		self.detectionDistLabel.setText("Detection dist ")
		self.layout1.addWidget(self.detectionDistLabel)
		self.layout1.setAlignment(self.detectionDistLabel, qtcore.Qt.AlignHCenter | qtcore.Qt.AlignVCenter)
		# self.layout1.setAlignment(self.detectionDistLabel, qtcore.Qt.AlignTop)

		self.recognizationDistLabel = qtw.QLabel()
		self.recognizationDistLabel.setText("Recognization dist ")
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

	@qtcore.Slot()
	def handle_saving(self):
		pass

	qtcore.Slot()
	def handle_canceling(self):
		pass