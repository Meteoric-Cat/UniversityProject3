from sys import setrecursionlimit

import cv2
import find_face_candidate as ffc 
import numpy as np
import gc
import utils as ut

if (__name__ == "__main__"):
	setrecursionlimit(100000)

	#imageName = input("Input name of the image:")
	imageName = './friend3.jpg'
	image = cv2.imread(imageName)
	image = cv2.resize(image, dsize = None, fx = 1, fy = 1).astype(np.float)

	#convert channel color
	m, n, tempX, tempY = ut.get_size_and_ranges(image)

	ut.convert_between_bgr_and_rgb(image, m, n, tempX, tempY)

	ffc.get_possible_face_regions(image, m, n, tempX, tempY)
	gc.collect()