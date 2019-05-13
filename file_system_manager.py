import os
from cv2 import imwrite, imread

IMAGE_PATH = "image_storage"

def write_facial_image_to_file(new_directory = False, personId, image):
	directory = (IMAGE_PATH + '/person%s') % personId
	imageId = None

	if (new_directory):
		os.mkdir(directory)
		imageId = 0
	else:
		entries = os.scandir()
		imageId = len(entries) + 1

	imwrite(((directory + "/%s.jpg") % imageId), image)

