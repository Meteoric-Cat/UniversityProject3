from sys import setrecursionlimit

import cv2
import find_face_candidate as ffc 
import numpy as np
import gc

if (__name__ == "__main__"):
	setrecursionlimit(100000)

	#imageName = input("Input name of the image:")
	imageName = './friend5.jpg'
	image = cv2.imread(imageName)
	image = cv2.resize(image, dsize = None, fx = 0.7, fy = 0.7).astype(np.float)

	#convert channel color
	m, n, p = image.shape
	tempX = range(0, m)
	tempY = range(0, n)	

	for i in tempX:
		for j in tempY:
			temp = image[i, j, 0]
			image[i, j, 0] = image[i, j, 2]
			image[i, j, 2] = temp

	ffc.get_possible_face_regions(image)
	gc.collect()