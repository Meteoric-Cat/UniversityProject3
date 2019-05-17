from cv2 import imwrite, imread, IMREAD_GRAYSCALE

import os
import numpy as np
import database_manager as db
import csv

IMAGE_PATH = "image_storage"
OUTPUT_SIZE = (100, 100)

def read_facial_images_into_matrix(personCount = None, directory = None, as_rows = True, image_size = OUTPUT_SIZE):
	imageCount = 0
	temp = None
	imagePerPerson = []

	if (directory is None):
		directory = IMAGE_PATH + "/facial_images/person_%s"

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
				tempImage = imread(entry.path, IMREAD_GRAYSCALE)
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
				tempImage = imread(entry.path, IMREAD_GRAYSCALE)
				tempImage = tempImage.flatten()

				result[:, count] = tempImage[:]
				fileInfo.append([i, str(entry.path)])
				count += 1

	return (result, fileInfo)

def clean_eigenface_images_up(directory = IMAGE_PATH + "/eigenface_images"):
	os.remove(directory + '/mean.jpg')
	os.remove(directory + '/eigenfaces.csv')

	# entries = os.scandir(directory)
	# for entry in entries:
	# 	os.remove(entry.path)

def write_meanface_and_eigenfaces(mean, eigenfaces, directory = None, output_size = OUTPUT_SIZE):
	check = False

	if (directory is None):
		directory = IMAGE_PATH + "/eigenface_images"		
	if (os.path.exists(directory + "/mean.jpg")):
		clean_eigenface_images_up()
		check = True

	temp = mean.reshape(output_size)
	imwrite(directory + "/mean.jpg", temp)
	
	# count = 0
	# directory = directory + "/eigenface_%s.jpg"

	# # print(eigenfaces[0])
	# for face in eigenfaces:	
	# 	temp = face.reshape(output_size)
	# 	count += 1
	# 	imwrite(directory % count, temp)

	with open(directory + "/eigenfaces.csv", "w") as csvFile:
		csvWriter = csv.writer(csvFile, delimiter = ",", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

		for eigenface in eigenfaces:
			csvWriter.writerow(list(eigenface))

	return check

def read_meanface_and_eignfaces(directory = None, eigenface_count = 11):
	if (directory is None):
		directory = IMAGE_PATH + "/eigenface_images"

	mean = imread(directory + "/mean.jpg").flatten()
	entries = os.scandir(directory) 

	eigenfaces = None
	with open(directory + "/eigenfaces.csv") as csvFile:
		csvReader = csv.reader(csvFile, delimiter=",")

		rowCount = sum(1 for row in csvReader)
		eigenface_count = int(min(eigenface_count, rowCount))
		eigenfaces = np.zeros([eigenface_count, OUTPUT_SIZE[0] * OUTPUT_SIZE[1]])

		r = 0
		for row in csvReader:
			c = 0
			for value in row:
				eigenfaces[r, c] = float(value)
				c += 1
			r += 1

	return mean, eigenfaces
		
def write_facial_image_to_file(personId = -1, image = None):
	directory = (IMAGE_PATH + '/facial_images/person_%s') % personId
	imageId = 0

	if not (os.path.isdir(directory)):
		os.mkdir(directory)
	else:
		imageId = len(list(os.scandir(directory)))

	imwrite(((directory + "/%s.jpg") % imageId), image)

def read_test_image(name, directory = IMAGE_PATH + "/test_images/"):
	return imread(directory + name, IMREAD_GRAYSCALE)
