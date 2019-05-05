import numpy as np

from math import acos, pi, sqrt

ROUNDX = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
ROUNDY = [-1, 0, 1, -1, 0, 1, -1, 0, 1]

def get_size_and_ranges(image):
	if (len(image.shape) == 3):
		m, n, k = image.shape		
	elif (len(image.shape) == 2):
		m, n = image.shape
	else:
		return (-1, -1, -1, -1)

	tempX = range(0, m)
	tempY = range(0, n)
	return (m, n, tempX, tempY)


def normalize_rgb(image, m = None, n = None, tempX = None, tempY = None, channel = 2):
	if (m == None):
		m, n, tempX, tempY = get_size_and_ranges(image)
		if (m == -1):
			print("something wrong 1")
			return

	r = np.zeros((m, n))
	g = np.zeros((m, n))

	#print(image.shape)
	#count = 0
	for i in tempX:
		for j in tempY:
			tempSum = image[i, j, 0] + image[i, j, 1] + image[i, j, 2]
			if (tempSum == 0):
				image[i, j, 0] = image[i, j, 1] = image[i, j, 2] = 1
				tempSum = 3
				#continue
			r[i, j] = image[i, j, 0] / tempSum
			g[i, j] = image[i, j, 1] / tempSum
	#print(count)
	return (r, g)

def convert_rgb_to_hsv(image, m = None, n = None, tempX = None, tempY = None):
	if (m == None):
		m, n, tempX, tempY = get_size_and_ranges(image)
		if (m == -1):
			print("something wrong 2")
			return

	h = np.zeros((m, n))
	s = np.zeros((m, n))
	v = np.zeros((m, n))

	for i in tempX:
		for j in tempY:
			temp = sqrt((image[i, j, 0] - image[i, j, 1])**2 + \
					(image[i, j, 0] - image[i, j, 2]) * (image[i, j, 1] - image[i, j, 2]))
			if (temp == 0.0):
				temp = 1		
			h[i, j] = acos(0.5 * (2 * image[i, j, 0] - image[i, j, 1] - image[i, j, 2]) / temp) * 180 / pi
			if (image[i, j, 2] > image[i, j, 1]):
				h[i, j] = 360 - h[i, j]

			tempMax = max(image[i, j, 0], image[i, j, 1], image[i, j, 2])
			tempMin = min(image[i, j, 0], image[i, j, 1], image[i, j, 2])

			s[i, j] = (tempMax - tempMin) / tempMax
			v[i, j] = tempMax / 255

	return (h, s, v)			

def filter_with_binary_median_filter(image, m = None, n = None, tempX = None, tempY = None, filter_radius = 1):
	if (filter_radius != 1):
		print('filter radius has not supported yet')
		return

	if (m == None):
		m, n, tempX, tempY = get_size_and_ranges(image)
		if (m == -1):
			print("something wrong 4")
			return

	temp = range(0, 9)

	count0 = count1 = 0
	tx = ty = 0
	
	for i in tempX:
		for j in tempY:
			count0 = count1 = 0
			for k in temp:
				tx = i + ROUNDX[k]
				ty = j + ROUNDY[k]
				if ((0 <= i + ROUNDX[k] < m) and (0 <= j + ROUNDY[k] < n)):				
					if (image[tx, ty] == 0):
						count0 += 1
					else:
						count1 += 1
				else:
					count0 += 1

			image[i, j] = 0 if (count0 > count1) else 1

	return image

def transform_with_binary_erosion(image, m = None, n = None, tempX = None, tempY = None, filter_size = 3):
	if (filter_size != 3):
		print('filter size has not been supported')
		return

	if (m == None):
		m, n, tempX, tempY = get_size_and_ranges(image)
		if (m == -1):
			print("something wrong 5")
			return

	#continue here