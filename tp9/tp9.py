#Nota: 
# h para hacer transformación .
# Luego de apretar la tecla h en el teclado, se pueden hacer medidas haciendo click en la imagen y moviendo el mouse.
# r borra las medidas.
# g para guardar las medidas.
import cv2
import numpy as np
color=(18, 255, 255)
drawing = False # true si el botón está presionado
mode=False

points = list()
def dibuja (event , x , y , flags ,param) :
    global xy_init,mode, hold,img_aux,imnt,color
    if event == cv2.EVENT_LBUTTONDOWN and hold:
        xy_init=x , y
        mode=True
    elif event == cv2.EVENT_MOUSEMOVE and mode :
        img_aux=imnt.copy()
        pts_init=(x+3,y+3),(x+3,y-3),(x-3,y-3),(x-3,y+3)
        pts_end=(xy_init[0]+3,xy_init[1]+3),(xy_init[0]+3,xy_init[1]-3),(xy_init[0]-3,xy_init[1]-3),(xy_init[0]-3,xy_init[1]+3)
        cv2.line(img_aux, (xy_init), (x , y),  color,2)
        dist_cm=get_dist(xy_init,(x , y))
        cv2.polylines(img_aux, np.array([pts_init]), True, color, 4)
        cv2.polylines(img_aux, np.array([pts_end]), True, color, 4)
        cv2.putText(img_aux,  "{:.2f}[cm]" .format(dist_cm), (x+20, y+20), cv2.FONT_HERSHEY_SIMPLEX,0.5,color, 1 , cv2.LINE_AA)
    if event == cv2.EVENT_LBUTTONUP:    
        xy_init=[-1,-1]
        imnt=img_aux
        mode=False
def get_dist(xy_init,xy_fin):
    x_dist=xy_fin[0]-xy_init[0]
    y_dist=xy_fin[1]-xy_init[1]
    module=abs(np.sqrt(x_dist**2 + y_dist**2)*aspect)
    return module

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
    H = round(max(int(H21), int(H30))*1.47)
    p_dst = np.float32([[0,0],[0,W],[H,0],[H,W]])
    M    = cv2.getPerspectiveTransform(points_ord,p_dst)
    imga = cv2.warpPerspective(img,M,(H,W))
    return imga

points=[[70, 338],[63, 173],[342, 67],[343, 444]]    
aspect=0.65
img = cv2.imread('frente.png',1)
cv2.namedWindow('image')
cv2.setMouseCallback('image',dibuja)
imgt=img.copy()
xy_init=0
hold=0  
while(1):
    k = cv2.waitKey(1) & 0xFF
    if k==ord('q'):
        break
    if k==ord('g') and hold:
        cv2.imwrite ('resultado.jpg', img_aux)
    elif k==ord('h') :  #Transformacion Rectificando. 
        if not hold:
            hold=1  
            imnt=rectificar(img,points)
            img_aux=imnt.copy()             
        else:
            hold=0 
    if k==ord('r') and hold:
        imnt=rectificar(img,points)
        img_aux=imnt.copy()
    if not hold:
        img_aux=img.copy()
    cv2.imshow('image',img_aux)
cv2.destroyAllWindows()
