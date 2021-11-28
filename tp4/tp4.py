#Nota: Presionando r de nuevo se borra la seleccion y se puede hacer una nueva.
# g para guardar.
# q para salir.
import cv2
import numpy as np
blue = (255,0,0);green = (0,255,0);red = (0,0,255);black=(0,0,0)
drawing = False # true si el botón está presionado
mode = True # si True, rectángulo, sino línea, cambia con
save=False
xybutton_down= -1,-1
xybutton_up= -1,-1
def dibuja (event , x , y , flags ,param) :
	global xybutton_down,drawing , mode, xybutton_up , save
	if event == cv2 .EVENT_LBUTTONDOWN and mode:
		drawing = True
		xybutton_down = x , y
	elif event == cv2.EVENT_MOUSEMOVE and mode:
		if drawing is True :
			img2[:]= 1
			img3[:]= 0
			cv2.rectangle(img2,xybutton_down,(x,y),black,2)
			cv2.rectangle(img3,xybutton_down,(x,y),red,2)
	elif event == cv2.EVENT_LBUTTONUP and mode:
		save=mode
		drawing = False
		mode = False
		xybutton_up= x , y
img = cv2.imread ('imagen.jpg',1)
largo,ancho,dim= np.shape(img)
img2 = np.ones((largo,ancho,dim),np.uint8)
img3 = np.zeros((largo,ancho,dim),np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image',dibuja)
while(1):
	imgt=img2*img
	imgt=imgt+img3
	cv2.imshow('image',imgt)
	k = cv2.waitKey(1) & 0xFF
	if k == ord('m'):
		mode = not mode
	elif k == ord('q') :
		break
	elif k==ord('r'):
		mode = True
		img2[:]= 1
		img3[:]= 0
	elif k==ord('g'):
		if xybutton_down[1] < xybutton_up[1]:
			x1= xybutton_down[1]
			x2= xybutton_up[1]
		else:
			x1= xybutton_up[1]
			x2= xybutton_down[1]
		if xybutton_down[0]< xybutton_up[0]:
			y1= xybutton_down[0]
			y2= xybutton_up[0]
		else:
			y1= xybutton_up[0]
			y2= xybutton_down[0]
		if(save):
			img4=img[x1:x2,y1:y2,:]
			cv2.imwrite ('resultado.jpg', img4)
			save=False
cv2.destroyAllWindows()
