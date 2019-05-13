import os
from cv2 import imwrite, imread

IMAGE_PATH = "image_storage"

def write_facial_image_to_file(new_directory = False, personId = -1, image = None):
	directory = (IMAGE_PATH + '/person%s') % personId
	imageId = 0

	if (new_directory):
		os.mkdir(directory)
	else:
		imageId = len(list(os.scandir(directory)))

	imwrite(((directory + "/%s.jpg") % imageId), image)

