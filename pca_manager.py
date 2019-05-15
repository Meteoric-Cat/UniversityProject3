from cv2 import PCACompute, PCAProject, PCABackProject

import file_system_manager as fm
import numpy as np
import database_manager as db

def find_meanface_and_eigenfaces(component_count = 10):
	'''get matrix of images, calculate mean, eigenvectors and save them in file'''
	images, filePaths = fm.read_facial_images_into_matrix()
	
	meanface, eigenfaces = PCACompute(images, np.empty((0)), maxComponents = component_count)
	checkOld = fm.write_meanface_and_eigenfaces(meanface, eigenfaces)

	#perform projection and save data to the database
	projectionResult = PCAProject(images, meanface, eigenfaces)
	db.create_subspace_images(filePaths, projectionResult, remove = checkOld)

	return meanface, eigenfaces

def detect_face(image, mean, eigenfaces, dist_threshold = 5):
	if (mean is None):
		mean, eigenfaces = fm.read_meanface_and_eigenfaces(None)

	temp = image.flatten()
	tempImage = np.zeros((1, temp.shape[0]))
	tempImage[0, :] = temp[:]
	projectionResult = PCACompute(tempImage, mean, eigenfaces)

	reconstructedImage = PCABackProject(projectionResult, mean, eigenfaces)
	if (ut.euclid_dist(reconstructedImage, tempImage) < dist_threshold):
		return True
	return False

def recognize_face(image, mean = None, eigenfaces = None, dist_threshold = 5):
	if (mean is None):
		mean, eigenfaces = fm.read_meanface_and_eigenfaces(None)

	tempImage = image.flatten()
	projectionResult = PCAProject(tempImage, mean, eigenfaces)

	subspaceImages = db.get_subspace_images()
	weights = np.zeros((1, weight_count))
	weight_count = 10
	min_dist = 100000000
	personId = -1
	
	for image in subspaceImages:
		temp = image.get_weights_as_array(weight_count)
		weights[0, :] = temp[:]

		dist = ut.euclid_dist(weights, projectionResult)
		if (dist < min_dist):
			min_dist = dist
			personId = image.OwnerId

	if (min_dist > dist_threshold):
		personId = -1

	return personId
	
if (__name__ == '__main__'):
	find_meanface_and_eigenfaces()
	db.clean_up()









