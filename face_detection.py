from sys import setrecursionlimit

import cv2
import find_face_candidate as ffc 
import numpy as np
import gc
import utils as ut

if (__name__ == "__main__"):
	setrecursionlimit(100000)

	#imageName = input("Input name of the image:")
	imageName = './input/hai/hai8.jpg'
	image = cv2.imread(imageName)
	#image = cv2.resize(image, dsize = None, fx = 1.0, fy = 1.0)
	m, n, tempX, tempY = ut.get_size_and_ranges(image)
	if (m > 1000 or n > 1000):
		image = cv2.resize(image, dsize = None, fx = 0.7, fy = 0.7)
		pass
	else:
		if (m > 2000 or n > 2000):
			image = cv2.resize(image, dsize = None, fx = 0.4, fy = 0.4)
	m, n, tempX, tempY = ut.get_size_and_ranges(image)

	#ut.convert_between_bgr_and_rgb(image, m, n, tempX, tempY)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.float)

	ffc.get_possible_face_regions(image, m, n, tempX, tempY)
	gc.collect()