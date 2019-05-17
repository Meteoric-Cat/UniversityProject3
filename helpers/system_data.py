import file_system_manager as fm 
import database_manager as db
import db_utils as dbut

class RunningSystemData():
	def __init__(self):
		self.mean, self.eigenfaces = fm.read_meanface_and_eigenfaces(eigenface_count = 50)
		self.eigenfaceCount = len(self.eigenfaces)

		self.subspaceImages = db.get_subspace_images()
		self.subspaceImageWeights = dbut.aggregate_subspaceimage_weights(self.subspaceImages)

		self.detectionThreshold = 2000
		self.recognizationThreshold = 500

	def change_detection_threshold(value = None):
		'''
		this function will increase the detection threshold when updating the system data
		'''
		self.subDetectionThreshold = self.detectionThreshold
		if (value is None):
			self.detectionThreshold = 3500
		else:
			self.detectionThreshold = value

	def recover_detection_threshold():
		self.detectionThreshold = self.subDetectionThreshold