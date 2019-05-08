import find_face_candidate as ffc 
import utils as ut 
import cv2
from sys import setrecursionlimit

if (__name__ == "__main__"):
	setrecursionlimit(10000)

	temp = input("Input id:")
	image1 = cv2.imread("./face_database/hello%s.jpg" % temp)
	image2 = cv2.imread("./face_database/gray%s.jpg" % temp)

	image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
	m, n, tempX, tempY = ut.get_size_and_ranges(image2)
	
	eyeBlockInfo = []

	ffc.find_possible_eye_blocks(image2, m, n, tempX, tempY, eyeBlockInfo, 
		aspect_ratio = (0.2, 1.67), width_ratio = (0.028, 0.4), occupancy_ratio = 0.3)

	eyeBlockInfo = ffc.match_eyes(image2, m, n, eyeBlockInfo)
	print(ffc.check_and_transform_region(image2))
	print(eyeBlockInfo)

	cv2.imshow("gray", image2)
	cv2.waitKey(0)