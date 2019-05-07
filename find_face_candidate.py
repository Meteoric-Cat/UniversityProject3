import cv2

import utils as ut 
import numpy as np

def build_binary_skin_map(image, r, g, h, s, v, height = None, width = None, tempX = None, tempY = None):
	if (height == None):
		height, width, tempX, tempY = ut.get_size_and_ranges(image)
		if (height == -1):
			print("something wrong 3")			
			return

	result = np.zeros((height, width))

	for i in tempX:
		for j in tempY:
			if ((image[i, j, 0] > image[i, j, 1]) and (abs(image[i, j, 0] - image[i, j, 1]) >= 11)):
				if ((0.33 <= r[i, j] <= 0.6) and (0.25 <= g[i, j] <= 0.37)):
					if ((340 <= h[i, j] <= 359) or (0 <= h[i, j] <= 50)):
						if (0.12 <= s[i, j] <= 0.7):						
							if (0.3 <= v[i, j] <= 1.0):
								result[i, j] = 1

	return result

def get_useful_regions_base_on_ratio(region_list, area_size = (30, 30), aspect_ratio = (0.8, 2.6), occupancy_ratio = 0.4):
	temp = range(1, len(region_list))
	result = []
	width = height = 0
	
	for i in temp:
		region = region_list[i]
		#print(region)
		width = abs(region[3] - region[1])
		height = abs(region[2] - region[0])

		if (width * height == 0):
			continue
		if (width > area_size[0]):
			if (height > area_size[1]):
			#if (aspect_ratio[0] <= height / width <= aspect_ratio[1]):
				if ((region[4] / (width * height)) >= occupancy_ratio):
					result.append(region)
	return result


def get_possible_face_regions(image):
	m, n, tempX, tempY = ut.get_size_and_ranges(image)
	if (m == -1):
		print("something wrong 0")
		return

	r, g = ut.normalize_rgb(image, m, n, tempX, tempY)
	h, s, v = ut.convert_rgb_to_hsv(image, m, n, tempX, tempY)	
 
	skinMap = build_binary_skin_map(image, r, g, h, s, v, m, n, tempX, tempY)
	ut.filter_with_binary_median_filter(skinMap, m, n, tempX, tempY)

	regionInfo = [['hello world']]
	ut.transform_with_open_operator(skinMap, regionInfo, m, n, tempX, tempY)	

	regionInfo = get_useful_regions_base_on_ratio(regionInfo, area_size = (40, 40), aspect_ratio = (0.8, 2.6), occupancy_ratio = 0.4)

	#image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2GRAY)
	#image[:, :] = skinMap[:, :] * 255

	image = image.astype(np.uint8)
	temp = len(regionInfo)
	#print(temp)
	if (temp > 0):
		for i in range(0, temp):
			cv2.rectangle(image, (regionInfo[i][1], regionInfo[i][0]), (regionInfo[i][3],regionInfo[i][2]), (0, 255, 0), 2)
	
	cv2.imshow('friend', image)
	cv2.waitKey(0)
