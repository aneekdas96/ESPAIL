import cv2
import os
import numpy as np
from PIL import Image
# # Read the images
# while True:
# 	print(timer() - start)
# 	_, foreground = fg.read()
#
# 	_, background = bg.read()
#
# 	if background is None:
# 		print("background is none")
# 		break
#
# 	if foreground is None:
# 		print("foreground is none")
# 		break
#
# 	f = foreground.copy()
# 	b = background.copy()
#
# 	alpha = np.zeros_like(foreground)
# 	alpha_b = np.zeros_like(background)
#
# 	gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
# 	gray_b = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
#
# 	alpha[:, :, 0] = gray
# 	alpha[:, :, 1] = gray
# 	alpha[:, :, 2] = gray
#
# 	alpha_b[:, :, 0] = gray_b
# 	alpha_b[:, :, 1] = gray_b
# 	alpha_b[:, :, 2] = gray_b
#
# 	# Convert uint8 to float
# 	foreground = foreground.astype(float)
# 	background = background.astype(float)
#
# 	# Normalize the alpha mask to keep intensity between 0 and 1
# 	alpha = alpha.astype(float) / 255
# 	alpha_b = alpha_b.astype(float) / 255
# 	# Multiply the foreground with the alpha matte
# 	foreground = cv2.multiply(alpha, foreground)
#
# 	# Multiply the background with ( 1 - alpha )
# 	background = cv2.multiply(1.0 - alpha, background)
#
# 	# Add the masked foreground and background.
# 	outImage = cv2.add(foreground, background)
#
# 	# Display image
# 	cv2.namedWindow('foreground', cv2.WINDOW_NORMAL)
# 	cv2.namedWindow('background', cv2.WINDOW_NORMAL)
# 	cv2.namedWindow('outImg', cv2.WINDOW_NORMAL)
# 	cv2.resizeWindow('outImg', 300, 300)
# 	cv2.resizeWindow('background', 300, 300)
# 	cv2.resizeWindow('foreground', 300, 300)
#
# 	cv2.imshow('foreground', f)
# 	cv2.imshow('background', b)
# 	cv2.imshow("outImg", outImage / 255)
# 	k = cv2.waitKey(1) & 0xFF
#
# 	if k == ord('q'):
# 		break
for i in os.listdir(os.getcwd()):
	if i[:5]=="frame":
		foreground = Image.open(i)
		background = Image.open("harvard_style_2.jpg")
		if background is None:
			print("background is none")
			break

		if foreground is None:
			print("foreground is none")
			break

		f = foreground.copy()
		b = background.copy()

		alpha = np.zeros_like(foreground)
		alpha_b = np.zeros_like(background)

		gray = cv2.cvtColor(foreground, cv2.COLOR_BGR2GRAY)
		gray_b = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

		alpha[:, :, 0] = gray
		alpha[:, :, 1] = gray
		alpha[:, :, 2] = gray

		alpha_b[:, :, 0] = gray_b
		alpha_b[:, :, 1] = gray_b
		alpha_b[:, :, 2] = gray_b

		# Convert uint8 to float
		foreground = foreground.astype(float)
		background = background.astype(float)

		# Normalize the alpha mask to keep intensity between 0 and 1
		alpha = alpha.astype(float) / 255
		alpha_b = alpha_b.astype(float) / 255
		# Multiply the foreground with the alpha matte

		alpha = alpha.resize((256, 256,3), Image.ANTIALIAS)
		foreground = foreground.resize((256, 256,3), Image.ANTIALIAS)
		background = background.resize((256, 256,3), Image.ANTIALIAS)

		alpha = numpy.array(alpha)
		foreground = numpy.array(foreground)
		background = numpy.array(background)

		alpha = alpha[:, :, ::-1].copy()
		foreground = foreground[:, :, ::-1].copy()
		background = background[:, :, ::-1].copy()

		foreground = cv2.multiply(alpha, foreground)

		# Multiply the background with ( 1 - alpha )
		background = cv2.multiply(1.0 - alpha, background)

		# Add the masked foreground and background.
		outImage = cv2.add(foreground, background)

		cv2.imwrite('out_imgi[-6:].jpg',outImage)

