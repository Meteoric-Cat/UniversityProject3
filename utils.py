import numpy as np
import cv2
from math import acos, pi, sqrt

ROUNDX = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
ROUNDY = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
STEPX = [-1, 0, 0, 1]
STEPY = [0, -1, 1, 0]

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
			if (temp == 0.000000000):
				temp = 1		
			h[i, j] = acos(0.5 * (2 * image[i, j, 0] - image[i, j, 1] - image[i, j, 2]) / temp) * 180 / pi
			if (image[i, j, 2] > image[i, j, 1]):
				h[i, j] = 360 - h[i, j]

			tempMax = max(image[i, j, 0], image[i, j, 1], image[i, j, 2])
			tempMin = min(image[i, j, 0], image[i, j, 1], image[i, j, 2])

			s[i, j] = (tempMax - tempMin) / tempMax
			v[i, j] = tempMax / 255

	# cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2HSV)
	# h, s, v = cv2.split(image)
	# h = h.astype(np.float)
	# s = s.astype(np.float)
	# v = v.astype(np.float)

	return (h, s, v)			

def filter_with_binary_median_filter(image, m = None, n = None, tempX = None, tempY = None, filter_radius = 1):
	if (filter_radius != 1):
		print('this filter has not been supported')
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

def scan_useful_region(image, m, n, steps, region_info, regionCount, i, j, temp, temp1):
	# if (steps[i, j] != 0):
	# 	return

	for k in temp:
		if (image[i + ROUNDX[k], j + ROUNDY[k]] == 0):
			return 

	steps[i, j] = regionCount
	region_info[regionCount][4] += 1
	for k in temp:
		image[i + ROUNDX[k], j + ROUNDY[k]] += 1

	#if (i <= region_info[regionCount][0]):
	region_info[regionCount][0] = min(i, region_info[regionCount][0])
	region_info[regionCount][1] = min(j, region_info[regionCount][1])
	#else:
	#if (i >= region_info[regionCount][2]):
	region_info[regionCount][2] = max(i, region_info[regionCount][2])
	region_info[regionCount][3] = max(j, region_info[regionCount][3])

	# for k in temp1:
	# 	if (0 < i + STEPX[k] < m):
	# 		if (0 < j + STEPY[k] < n):				
	# 			scan_useful_region(image, m, n, steps, region_info, regionCount, i + STEPX[k], j + STEPY[k], temp, temp1)

	for k in temp1:
		valuex = i + STEPX[k]
		valuey = j + STEPY[k]

		if (0 < valuex < m):
			if (0 < valuey < n):
				if (steps[valuex, valuey] == 0):
					scan_useful_region(image, m, n, steps, region_info, regionCount, valuex, valuey, temp, temp1)

def transform_with_open_operator(image, region_info, m = None, n = None, tempX = None, tempY = None, filter_size = 3):
	if (filter_size != 3):
		print('this filter has not been supported')
		return

	if (m == None):
		m, n, tempX, tempY = get_size_and_ranges(image)
		if (m == -1):
			print('something wrong 5')
			return

	if (region_info == None):
		print('something wrong 6')
		return

	temp = range(0, 9)
	temp1 = range(0, 4)
	regionCount = 0
	steps = np.zeros((m, n))
	tempX = range(1, m - 1)
	tempY = range(1, n - 1)
	surround = True

	for i in tempX:
		for j in tempY:
			if (image[i, j] == 1):
				if (steps[i, j] == 0):
					surround = True
					for k in temp:
						if (image[i + ROUNDX[k], j + ROUNDY[k]] != 1):
							surround = False
							break
					if (surround):
						regionCount += 1
						region_info.append([i, j, i, j, 0])

						scan_useful_region(image, m - 1, n - 1, steps, region_info, regionCount, i, j, temp, temp1)

	for i in tempX:
		for j in tempY:
			if (image[i, j] <= 1):
				image[i, j] = 0
			else:
				image[i, j] = 1

def count_useful_pixels(image, region):
	tempX = range(region[0], region[2])
	tempY = range(region[1], region[3])

	count = 0
	for i in tempX:
		for j in tempY:
			if (image[i, j] != 0):
				count += 1

	return count

def scan_region(image, steps, m, n, i, j, region_value, region_info, temp):	
	steps[i, j] = 1
	region_info[4] += 1

	region_info[0] = min(i, region_info[0])
	region_info[1] = min(j, region_info[1])

	region_info[2] = max(i, region_info[2])
	region_info[3] = max(j, region_info[3])

	for k in temp:
		valuex = i + STEPX[k]
		valuey = j + STEPY[k]

		if (0 <= valuex < m):
			if (0 <= valuey < n):
				if (steps[valuex, valuey] == 0):
					if (image[valuex, valuey] < 125):
						scan_region(image, steps, m, n, valuex, valuey, region_value, region_info, temp)

def split_image_into_images(image, region_info, directory = "face_database/%s.jpg"):
	temp = range(0, len(region_info))

	for i in temp:
		subImage = image[region_info[i][0] : region_info[i][2], region_info[i][1] : region_info[i][3]]		
		cv2.imwrite(directory % i, subImage)

def find_angle_between_two_vectors(vector1, vector2):
	v1dist = sqrt(vector1[0]**2 + vector1[1]**2)
	v2dist = sqrt(vector2[0]**2 + vecotr2[1]**2)

	return acos((vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (v1dist * v2dist)) * 180 / pi