#Nota: Presionando r de nuevo se borra la seleccion y se puede hacer una nueva.
# g para guardar.
# q para salir.
# e para aplicar transformación euclidiana y guardar. Si se apreta e de nuevo se vuelve a la imagen principal.
# s para aplicar transformación de similaridad  y guardar. Si se apreta s de nuevo se vuelve a la imagen principal.
# a para incrustar imagen.
# h para hacer rectificacion de imagenes y luego para volver. Se puede guardar con la letra g.
import cv2
import numpy as np
blue = (255,0,0);green = (0,255,0);red = (0,0,255);black=(0,0,0)
drawing = False # true si el botón está presionado
lastmode = mode = 1 # si True, rectángulo, sino línea, cambia con
save=False
xybutton_down= -1,-1
xybutton_up= -1,-1
points = list()
def dibuja (event , x , y , flags ,param) :
    global xybutton_down,drawing , mode, xybutton_up , save,points,img_insert,img3,img2,img,lastmode
    if event == cv2.EVENT_LBUTTONDOWN and mode == 1:
        drawing = True
        xybutton_down = x , y
    elif event == cv2.EVENT_MOUSEMOVE and mode == 1:
        if drawing is True :
            img2[:]= 1
            img3[:]= 0
            cv2.rectangle(img2,xybutton_down,(x,y),black,2)
            cv2.rectangle(img3,xybutton_down,(x,y),red,2)
    elif event == cv2.EVENT_LBUTTONUP and mode == 1:
            save=True
            drawing = False
            lastmode=mode
            mode = 0
            xybutton_up= x , y
#
    elif (event == cv2.EVENT_LBUTTONUP and mode == 2):
        if(len(points)<3):
                img3 = cv2.circle(img3, (x, y), 1, (0, 0, 255), 2)
                img2 = cv2.circle(img2, (x, y), 1, (0, 0, 0), 2)
                points.append([x, y])
        if(len(points)==3):
                lastmode=mode
                mode=0
                save=True
    elif (event == cv2.EVENT_LBUTTONUP and mode == 3):
        if(len(points)<4):
                img3 = cv2.circle(img3, (x, y), 1, (0, 0, 255), 2)
                img2 = cv2.circle(img2, (x, y), 1, (0, 0, 0), 2)
                points.append([x, y])
        if(len(points)==4):
                lastmode=mode
                mode=0
                save = True

def euclidiano(img,anglee,x,y):
	angle=anglee*np.pi/180
	(h, w)= (img.shape[0], img.shape[1])
	M= np.float32 ([[ np.cos(angle), np.sin(angle), x],
					[-np.sin(angle), np.cos(angle), y]])
	shifted= cv2.warpAffine(img, M, (w, h))
	return shifted

def similar(img,anglee,x,y,s):
	angle=anglee*np.pi/180
	(h, w)= (img.shape[0], img.shape[1])
	M= np.float32 ([[ s*np.cos(angle), s*np.sin(angle), x],
					[s*-np.sin(angle), s*np.cos(angle), y]])
	shifted= cv2.warpAffine(img, M, (w, h))
	return shifted

def afin(output_pts,img_insert):
    (h,w,dim) = np.shape(img_insert)
    input_pts = np.float32([[0, h],[0,0],[w, 0]])
    output_pts=np.float32(output_pts)
    (rows, cols,dim2) = np.shape(img)
    mask = np.ones((h,w,dim),np.uint8)
    mask[:,:,:]=255
    M = cv2.getAffineTransform(input_pts, output_pts)
    img_dst = cv2.warpAffine(img_insert, M, (cols, rows))
    mask= cv2.warpAffine(mask, M, (cols, rows))
    return  mask , img_dst

def rectificar(img, points):
    mod=list()
    points_ord=list()
    i=0
    for x,y in points:
        mod.append([np.sqrt(x**2 +y**2),i])
        i+=1
    mod.sort()
    for i in mod:
        points_ord.append(points[i[1]])
    points_ord=np.float32(points_ord)
    d10  = points_ord [1] - points_ord [0] 
    d32  = points_ord [3] - points_ord [2]
    d21  = points_ord [2] - points_ord [1]
    d30  = points_ord [3] - points_ord [0]
    # Ancho y largo
    W10  = np.sqrt(d10[0]**2 + d10[1]**2)
    W32  = np.sqrt(d32[0]**2 + d32[1]**2)
    H21  = np.sqrt(d21[0]**2 + d21[1]**2)
    H30  = np.sqrt(d30[0]**2 + d30[1]**2)
    W = max(int(W10), int(W32))
    H = max(int(H21), int(H30))
    p_dst = np.float32([[0,0],[0,W],[H,0],[H,W]])
    M    = cv2.getPerspectiveTransform(points_ord,p_dst)
    imga = cv2.warpPerspective(img,M,(H,W))
    return imga
    
img = cv2.imread('rand.jpg',1)
img_insert = cv2.imread('ciiilogo.png',1)
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
    if k == ord('m'):                       #dibujar rectangulo
        mode=1
        img2[:]= 1
        img3[:]= 0
    elif k==ord('q'):
        break
    elif k==ord('r'):                       #resetea
        mode = lastmode
        img2[:]= 1
        img3[:]= 0
    elif k==ord('g'):                       #guarda recorte
        if lastmode == 1:
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
        elif lastmode ==2 :
                cv2.imwrite ('resultado.jpg', imgt)
                save=False
    elif k==ord('e'):                               #Aplica transformación euclidiana recorte
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
        img4=img[x1:x2,y1:y2,:]
        img4=euclidiano(img4,10,10,12)
        cv2.imwrite ('euclidiano.jpg', img4)
        while 1:
            cv2.imshow('image',img4)
            k=cv2.waitKey(1) & 0xFF
            if(k==ord('e')):
                break
    elif k==ord('s'):
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
            img4=img[x1:x2,y1:y2,:]
            img4=similar(img4,10,10,12,0.2)
            cv2.imwrite ('similar.jpg', img4)
            while 1:
                cv2.imshow('image',img4)
                k=cv2.waitKey(1) & 0xFF
                if(k==ord('s')):
                    break
    elif k==ord('a') or (save == True and len(points)== 3 and mode!=3):                   #Transformacion afin     
        mode=2
        img2[:]= 1
        img3[:]= 0
        if (len(points)== 3):
                mask,img3 = afin(np.float32([points[0], points[1], points[2]]),img_insert)
                lower_color = np.array([0, 0, 0])
                upper_color = np.array([255, 255, 255])
                mask=cv2.bitwise_not(mask)
                img2[:,:,:]=mask[:,:,:]/255
                points=list()
        save=False
    elif k==ord('h') or (save == True and len(points)== 4):               #Transformacion Rectificando.  
        mode=3
        img2[:]= 1
        img3[:]= 0
        if(len(points)==4):
            img4=rectificar(img,points)
            while 1:
                cv2.imshow('image',img4)
                k=cv2.waitKey(1) & 0xFF
                if(k==ord('s')):
                    cv2.imshow('image',img4)
                elif k==ord('h'):
                    break
            points=list()
            save=False
cv2.destroyAllWindows()
