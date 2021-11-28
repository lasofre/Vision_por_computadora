#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
img = cv2.imread ( 'hoja_arce.3.jpg',0)
for row in img:
	for col in range(len(row)):
		if row[col]>120:
			row[col]=255
		else:
			row[col]=0
cv2.imwrite ('resultado.jpg', img)
