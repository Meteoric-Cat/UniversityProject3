from cv2 import imwrite, imread

import os

import database_manager as db

IMAGE_PATH = "image_storage"
OUTPUT_SIZE = (100, 100)

def read_facial_images_into_matrix(personCount, directory, as_rows = True, image_size = OUTPUT_SIZE):
	imageCount = 0
	temp = None
	imagePerPerson = []

	if (directory is None):
		directory = IMAGE_PATH + "/facial_images/person%s"

	if (personCount is None):
		personCount = db.get_people_count()
		temp = range(1, personCount + 1)		
		for i in temp:
			imageCount += len(list(os.scandir(directory % i)))

	result = None
	fileInfo = []

	if (as_rows):
		result = np.zeros((imageCount, image_size[0] * image_size[1]))
		count = 0
		for i in temp:
			entries = os.scandir(directory % i)
			for entry in entries:
				tempImage = imread(entry.path)
				tempImage = tempImage.flatten()				

				result[count, :] = tempImage[:]
				fileInfo.append([i, str(entry.path)])
				count += 1
	else:
		result = np.zeros((image_size[0] * image_size[1], imageCount))
		count = 0
		for i in temp:
			entries = os.scandir(directory % i)
			for entry in entries:
				tempImage = imread(entry.path)
				tempImage = tempImage.flatten()

				result[:, count] = tempImage[:]
				fileInfo.append([i, str(entry.path)])
				count += 1

	return (result, fileInfo)

def clean_eigenface_images_up(directory = IMAGE_PATH + "/eigenface_images"):
	os.remove(directory + '/mean.jpg')

	entries = os.scandir(directory)
	for entry in entries:
		os.remove(entry.path)

def write_meanface_and_eigenfaces(mean, eigenfaces, directory, output_size = OUTPUT_SIZE):
	check = True

	if (directory is None):
		directory = IMAGE_PATH + "/eigenface_images"		
	if (os.path.exists(directory + "/mean.jpg")):
		clean_eigenface_images_up()
		check = False

	temp = mean.reshape(output_size)
	imwrite(directory + "/mean.jpg", temp)
	
	count = 0
	directory = directory + "/eigenface_%s.jpg"

	for face in eigenfaces:
		temp = face.reshape(output_size)
		count += 1
		imwrite(directory % count, temp)

	return check

def read_meanface_and_eignfaces(directory, eigenface_count = 10):
	if (directory is None):
		directory = IMAGE_PATH + "/eigenface_images"

	mean = imread(directory + "/mean.jpg").flatten()

	eigenfaces = np.zeros((eigenface_count, mean.shape[1]))
	temp = range(0, eigenface_count)
	directory = directory + "/eigenface_%s.jpg"

	for i in temp:
		tempImage = imread(directory % i).flatten()
		eigenfaces[i, :] = tempImage[:]

	return mean, eigenfaces
		
def write_facial_image_to_file(new_directory = False, personId = -1, image = None):
	directory = (IMAGE_PATH + '/people_image/person%s') % personId
	imageId = 0

	if (new_directory):
		os.mkdir(directory)
	else:
		imageId = len(list(os.scandir(directory)))

	imwrite(((directory + "/%s.jpg") % imageId), image)
