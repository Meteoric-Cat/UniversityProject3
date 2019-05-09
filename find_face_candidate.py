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

def get_useful_regions_base_on_ratio(image, region_list, area_size = (30, 30), aspect_ratio = (0.8, 2.6), occupancy_ratio = 0.4):
	temp = range(1, len(region_list))
	result = []
	width = height = 0
	
	for i in temp:
		region = region_list[i]
		#print(region)
		width = region[3] - region[1]
		height = region[2] - region[0]

		if (width * height == 0):
			continue
		if (width > area_size[0]) and (height > area_size[1]):
			if (aspect_ratio[0] <= height / width <= aspect_ratio[1]):
				if ((region[4] / (width * height)) >= occupancy_ratio):
					result.append(region)
	return result

def find_possible_eye_blocks(image, m, n, tempX, tempY, possible_eye_info, 
		aspect_ratio = (0.2, 1.67), width_ratio = (0.028, 0.4), occupancy_ratio = 0.3):
	steps = np.zeros((m, n))	
	temp = range(0, 4)

	for i in tempX:
		for j in tempY:
			if (steps[i, j] == 0):
				if (image[i, j] == 0):
					regionInfo = [i, j, i, j, 0]					
					ut.scan_region(image, steps, m, n, i, j, 1, regionInfo, temp)

					height = abs(regionInfo[0] - regionInfo[2])
					width = abs(regionInfo[1] - regionInfo[3])
					if (width * height == 0):
						continue

					if (aspect_ratio[0] <= (height / width) <= aspect_ratio[1]):
						if (occupancy_ratio <= (regionInfo[4] / (width * height))):
							if (width_ratio[0] <= (width / n) <= width_ratio[1]):
								possible_eye_info.append(regionInfo)

def match_eyes(image, m, n, possible_eye_info, pair_size_error = 5, dist_ratio = (0.2, 0.65)):
	infoLength = len(possible_eye_info)
	temp = range(0, infoLength)
	result = []

	for i in temp:
		height1 = possible_eye_info[i][2] - possible_eye_info[i][0]
		width1 = possible_eye_info[i][3] - possible_eye_info[i][1]
		centroid1y = (possible_eye_info[i][1] + possible_eye_info[i][3]) / 2

		temp1 = range(i + 1, infoLength)

		for j in temp1:
			height2 = possible_eye_info[j][2] - possible_eye_info[j][0]
			width2 = possible_eye_info[j][3] - possible_eye_info[j][1]

			if (abs(width1 - width2) <= pair_size_error):
				if (abs(height2 - height1) <= pair_size_error):
					centroid2y = (possible_eye_info[j][1] + possible_eye_info[j][3]) / 2
					dist = abs(centroid2y - centroid1y)

					if ((dist / n) <= dist_ratio[1]):
						result.append(possible_eye_info[i])
						result.append(possible_eye_info[j])		
						#return result				
	return result

def check_and_transform_region(region_skin_image):
	m, n, tempX, tempY = ut.get_size_and_ranges(region_skin_image)
	eyeBlockInfo = [["hello"]]	

	ut.reverse_binary_image(region_skin_image, m, n, tempX, tempY)
	ut.transform_with_open_operator(region_skin_image, eyeBlockInfo, m, n, tempX, tempY)
	
	eyeBlockInfo = []
	find_possible_eye_blocks(region_skin_image, m, n, tempX, tempY, eyeBlockInfo)

	eyeBlockInfo = match_eyes(region_skin_image, m, n, eyeBlockInfo)
	print(eyeBlockInfo)
	if (len(eyeBlockInfo) == 0):
		return False
 
	return True


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
	# kernel = np.ones((3,3))
	# skinMap = cv2.morphologyEx(skinMap, cv2.MORPH_OPEN, kernel)
	ut.transform_with_open_operator(skinMap, regionInfo, m, n, tempX, tempY)	

	regionInfo = get_useful_regions_base_on_ratio(skinMap, regionInfo, area_size = (40, 40), aspect_ratio = (0.8, 2.6), occupancy_ratio = 0.4)

	result = []	
	for region in regionInfo:
		tempImage = skinMap[region[0]:region[2], region[1]:region[3]]
		if (check_and_transform_region(tempImage) == True):
			result.append(region)		
	regionInfo = result

	#display image to check the bounding box
	# image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_RGB2GRAY)
	# image[:, :] = skinMap[:, :] * 255
	
	image = image.astype(np.uint8)
	temp = len(regionInfo)
	if (temp > 0):
		for i in range(0, temp):
			cv2.rectangle(image, (regionInfo[i][1], regionInfo[i][0]), (regionInfo[i][3],regionInfo[i][2]), (0, 255, 0), 2)
	
	cv2.imshow('friend', image)
	cv2.waitKey(0)
	cv2.destroyWindow('friend')

	#divide image and save it to database
	#ut.split_image_into_images(image.astype(np.uint8), regionInfo, directory = "face_database/gray%s.jpg")


