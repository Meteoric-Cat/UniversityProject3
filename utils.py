import numpy as np
import cv2
from math import acos, pi, sqrt
from collection import deque

ROUNDX = [-1, -1, -1, 0, 0, 0, 1, 1, 1]
ROUNDY = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
STEPX = [-1, 0, 0, 1]
STEPY = [0, -1, 1, 0]

def convert_between_bgr_and_rgb(image, m, n, tempX, tempY):
	for i in tempX:
		for j in tempY:
			temp = image[i, j, 0]
			image[i, j, 0] = image[i, j, 2]
			image[i, j, 2] = temp			

def balance_color(image, m, n, tempX, tempY):
	sumRed = 0
	sumGreen = 0
	sumBlue = 0

	for i in tempX:
		for j in tempY:
			sumRed += image[i, j, 0]
			sumGreen += image[i, j, 1]
			sumBlue += image[i, j, 2]

	sumRed = sumRed / (m * n)
	sumGreen = sumGreen / (m * n)
	sumBlue = sumBlue / (m * n)

	tempSum = sumRed + sumBlue + sumGreen
	tempRed = tempSum / (3 * sumRed)
	tempGreen = tempSum / (3 * sumGreen)
	tempBlue = tempSum / (3 * sumBlue)

	for i in tempX:
		for j in tempY:
			image[i, j, 0] = image[i, j, 0] * tempRed
			image[i, j, 1] = image[i, j, 1] * tempGreen
			image[i, j, 2] = image[i, j, 2] *  tempBlue

def white_balance(image):
	image = image.astype(np.uint8)
	result = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
	
	avgAChannel = np.average(result[:, :, 1])
	avgBChannel = np.average(result[:, :, 2])

	result[:, :, 1] = result[:, :, 1] - ((avgAChannel - 128) * (result[:, :, 0] / 255.0) * 1.1)
	result[:, :, 2] = result[:, :, 2] - ((avgBChannel - 128) * (result[:, :, 0] / 255.0) * 1.1)

	result = cv2.cvtColor(result, cv2.COLOR_LAB2RGB)
	return result

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
						if (0 <= i + ROUNDX[k] < m):
							if (0 <= j + ROUNDY[k] < n):
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

def get_connected_regions(image, m, n, tempX, tempY, region_info, region_value):	
	steps = np.zeros((m, n))
	temp = range(0, 4)
	pixels = deque()

	for i in tempX:
		for j in tempY:
			if (image[i, j] == region_value):
				if (steps[i, j] == 0):
					region = [i, j, i, j, 1]
					pixels.append([i, j])					
					count = 1

					while (count > 0):
						count -= 1
						current = pixels.popleft()
						steps[current[0], current[1]] = 1

						#update region information
						region[4] += 1
						region[0] = min(current[0], region[0])
						region[1] = min(current[1], region[1])
						region[2] = max(current[0], region[2])
						region[3] = max(current[1], region[3])

						for k in temp:
							valuex = current[0] + STEPX[k] 
							valuey = current[1] + STEPY[k]

							if (0 <= valuex < m):
								if (0 <= valuey < n):
									if (image[valuex, valuey] == region_value):
										if (steps[valuex, valuey] == 0):
											count += 1
											pixels.append([valuex, valuey])

					region_info(region)

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
					if (image[valuex, valuey] == region_value):
						scan_region(image, steps, m, n, valuex, valuey, region_value, region_info, temp)

def split_image_into_images(image, region_info, directory = "face_database/%s.jpg"):
	temp = range(0, len(region_info))

	for i in temp:
		subImage = image[region_info[i][0] : region_info[i][2], region_info[i][1] : region_info[i][3]]		
		cv2.imwrite(directory % i, subImage)

def find_angle_between_two_vectors(vector1, vector2):
	v1dist = sqrt(vector1[0]**2 + vector1[1]**2)
	v2dist = sqrt(vector2[0]**2 + vector2[1]**2)

	return acos((vector1[0] * vector2[0] + vector1[1] * vector2[1]) / (v1dist * v2dist)) * 180 / pi

def reverse_binary_image(image, m, n, tempX, tempY):
	for i in tempX:
		for j in tempY:
			image[i, j] = 0 if (image[i, j] == 1) else 1

def check_binary_border(image, m, n, i, j, temp):
	if (i == 0 or i == m - 1):
		return True
	if (j == 0 or j == n - 1):
		return True

	for k in temp:
		if (image[i, j] != image[i + STEPX[k], j + STEPY[k]]):
			return True

	return False 

def find_binary_border(image, steps, m, n, i, j, border, border_value, temp, temp1):
	steps[i, j] = 1
	border.append([i, j])

	for k in temp:
		valuex = i + ROUNDX
		valuey = j + ROUNDY

		if (0 <= valuex < m):
			if (0 <= valuey < n):
				if (image[valuex, valuey] == border_value):
					if (steps[valuex, valuey] == 0):
						if (check_binary_border(image, m, n, valuex, valuey, temp1)):
							find_binary_border(image, steps, m, n, valuex, valuey, border, border_value, temp, temp1)

def find_line(x, y):
	'''a, b, c of the line ax + by + c = 0 that contains 2 specified points'''
	return [y[1] - x[1], x[0] - y[0], x[1] * (y[0] - x[0]) - x[0] * (y[1] - x[1])]

def find_the_farthest_point(line, point_list):
	maxDist = 0
	result = None
	temp = sqrt(line[0]**2 + line[1]**2)

	for point in point_list:
		dist = abs(line[0] * point[0] + line[1] * point[1] + line[2]) / temp
		if (dist > maxDist):
			maxDist = dist
			result = point

	return result