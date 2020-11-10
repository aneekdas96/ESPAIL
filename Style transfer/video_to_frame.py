import cv2

cam = cv2.VideoCapture('input_video.mp4')
counter = 0
while True:
	ret,frame = cam.read()
	counter+=1
	renanme_counter = str(counter)
	while len(renanme_counter)<4:
		renanme_counter = '0'+renanme_counter
		
	print (ret,renanme_counter)
	if frame is None:
		break
	cv2.imwrite('frame_'+renanme_counter+'.jpg',frame)


