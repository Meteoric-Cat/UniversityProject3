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
		directory = IMAGE_PATH + "/people_images/person%s"

	if (personCount is None):
		personCount = db.get_people_count()
		temp = range(1, personCount + 1)
		for i in temp:
			imageCount += len(list(os.scandir(directory % i)))

	result = None
	if (as_rows):
		result = np.zeros((imageCount, image_size[0] * image_size[1]))
		count = 0
		for i in temp:
			entries = os.scandir(directory % i)
			for entry in entries:
				tempImage = imread(entry.path)
				tempImage = tempImage.flatten()				

				result[count, :] = tempImage[:]
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
				count += 1

	return result

def write_mean_face_and_eigenfaces(mean, eignfaces, directory, output_size = OUTPUT_SIZE):
	if (directory is None):
		directory = IMAGE_PATH + "/data_images"		

	if (os.path.exists(directory + "/mean.jpg")):
		clean_data_images_up()

	temp = mean.reshape(output_size)
	imwrite(directory + "/mean.jpg", temp)

	count = 0
	for face in eignfaces:
		temp = face.reshape(output_size)
		count += 1
		imwrite((directory + "/eignface%s.jpg") % count, temp)

def read_mean_face_and_eignfaces(mean, eignfaces, directory, output_size = OUTPUT_SIZE):
	pass
		
def write_facial_image_to_file(new_directory = False, personId = -1, image = None):
	directory = (IMAGE_PATH + '/people_image/person%s') % personId
	imageId = 0

	if (new_directory):
		os.mkdir(directory)
	else:
		imageId = len(list(os.scandir(directory)))

	imwrite(((directory + "/%s.jpg") % imageId), image)
