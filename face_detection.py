from sys import setrecursionlimit

import cv2
import find_face_candidate3 as ffc 
import numpy as np
import gc
import utils as ut

if (__name__ == "__main__"):
	setrecursionlimit(100000)

	#imageName = input("Input name of the image:")
	imageName = './friend5.jpg'
	image = cv2.imread(imageName)
	image = cv2.resize(image, dsize = None, fx = 1, fy = 1)

	#convert channel color
	m, n, tempX, tempY = ut.get_size_and_ranges(image)

	#ut.convert_between_bgr_and_rgb(image, m, n, tempX, tempY)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float)

	ffc.get_possible_face_regions(image, m, n, tempX, tempY)
	gc.collect()