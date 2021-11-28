#! /usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import cv2
if(len(sys.argv) > 1 ) :
	filename= sys.argv[1]
else:
	print(' Pasar el nombre del video como argumento ')
	sys.exit(0)
cap = cv2.VideoCapture(filename)
print("fps: "+str(cap.get(cv2.CAP_PROP_FPS)))

while(cap.isOpened()) :
	ret,frame = cap.read()
	gray = cv2.cvtColor(frame,cv2 .COLOR_BGR2GRAY)
	cv2.imshow('frame',gray )
	if((cv2.waitKey(33) & 0xFF ) == ord('q')) :
		break
cap.release()
cv2.destroyAllWindows()
