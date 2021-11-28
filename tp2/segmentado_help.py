#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
img = cv2.imread ( 'hoja_arce.3.jpg',0)
height, width = img.shape
print(height)
print(width)
