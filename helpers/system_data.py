import file_system_manager as fm 

class RunningSystemData():
	def __init__():
		self.mean, self.eigenfaces = fm.read_meanface_and_eigenfaces(eigenface_count = 50)
		self.eigenfaceCount = len(self.eigenfaces)

		self.subspaceImages = db.get_subspace_images()
		self.subspaceImageWeights = dbut.aggregate_subspaceimage_weights(self.subspaceImages)
