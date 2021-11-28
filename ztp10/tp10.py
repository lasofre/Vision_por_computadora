import cv2
import cv2.aruco as aruco
import numpy as np
from random import randrange

def afin(output_pts,img_insert,frame_markers):
    (h,w,dim) = np.shape(img_insert)
    input_pts = np.float32([[0, h],[0,0],[w, 0]])
    output_pts=np.float32(output_pts)
    (rows, cols,dim2) = np.shape(frame_markers)
    mask = np.ones((h,w,dim),np.uint8)
    mask[:,:,:]=255
    M = cv2.getAffineTransform(input_pts, output_pts)
    img_dst = cv2.warpAffine(img_insert, M, (cols, rows))
    mask= cv2.warpAffine(mask, M, (cols, rows))
    return  mask , img_dst

def get_vert_markers(frame):
    vert=list()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    frame_markers = aruco.drawDetectedMarkers(frame.copy(), corners, ids)
    if corners !=[]:
        for i in range(4):
                vert.append([int(corners[0][0][i][0]),int(corners[0][0][i][1])])
    return vert,frame_markers

def game():
    global ancho
    global largo
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    color = (255, 0, 255)
    thickness = 1
    img5 = np.zeros((largo,ancho,dim),np.uint8)
    img3 = np.zeros((largo,ancho,dim),np.uint8)
    img4 = np.zeros((largo,ancho,dim),np.uint8)
    img6 = np.zeros((largo,ancho,dim),np.uint8)
    mask = np.zeros((largo,ancho,dim),np.uint8)
    red = (0,0,255)
    obs=list()
    cont=0
    j=0
    end=0
    while True:
        ret, frame = vid.read()
        vert,frame_markers=get_vert_markers(frame)
        imgt=frame
        if j>10 :
            obs.insert(0,[randrange(ancho-100),0,randrange(10,100)])
            j=0
        else:
            img4[:]= 0
            img6[:]= 0
            for i in range(0,len(obs)):
                if obs[i][1]>largo:
                    obs = obs[:-1]
                else:
                    obs[i][1]=obs[i][1]+10
                    img4=cv2.rectangle(img4,(obs[i][0],obs[i][1]),(obs[i][0]+obs[i][2],obs[i][1]+obs[i][2]),red,-1)
                    mask2,img5 = afin(np.float32([(obs[i][0]+obs[i][2],obs[i][1]+obs[i][2]),(obs[i][0]+obs[i][2],obs[i][1]),(obs[i][0],obs[i][1])]),obstaculo,img4)
                    img6+=img5
        j+=1
        if vert !=[]:         
            mask,img3 = afin(np.float32([vert[0], vert[1], vert[2]]),img_insert,frame_markers)
            mask[:,:,:]=mask[:,:,:]/255
            mask[:,:,:]=mask[:,:,:]*[0,255,0]
        lower_color = np.array([0, 100,100])
        upper_color = np.array([0, 255, 255])
        img_full=img4+mask
        detect=cv2.inRange(img_full, lower_color, upper_color)
        cont+=1
        imgt=img6+img3
        imgt=cv2.flip(imgt,1)
        cv2.putText(imgt, 'contador: '+str(cont), (10,20), font,fontScale, color, thickness, cv2.LINE_AA)
        if np.sum(detect)>100:
            while True:
                imgt[:]= 0
                x=int(ancho/4)
                y=int(largo/2)
                cv2.putText(imgt, 'Perdiste',(x,y), font,fontScale, color, thickness, cv2.LINE_AA)
                cv2.putText(imgt, 'interacciones: '+str(cont), (x,y+20), font,fontScale, color, thickness, cv2.LINE_AA)
                cv2.putText(imgt, 'Preione R para voler a jugar...', (x,y+40), font,fontScale, color, thickness, cv2.LINE_AA)
                cv2.putText(imgt, 'Preione Q para salir ...', (x,y+60), font,fontScale, color, thickness, cv2.LINE_AA)
                cv2.imshow('frame',imgt)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q'):
                    end=1
                    break
                if k == ord('r'):
                    imgt[:]= 0
                    detect[:]= 0
                    img4[:]= 0
                    img5[:]= 0
                    img6[:]= 0
                    cont=0
                    obs=list()
                    break                
        cv2.imshow('frame',imgt)
        cv2.imshow('detect',detect)
        cv2.imshow('matrix',img_full)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        if end:
            break
def video():
    cap = cv2.VideoCapture("alien.mp4")
    while True:
        ret, frame = vid.read()
        ret2,frame2 = cap.read()
        vert,frame_markers=get_vert_markers(frame)
        imgt=frame
        if ret2:
            if vert !=[]:         
                mask,img3 = afin(np.float32([vert[0], vert[1], vert[2]]),frame2,frame_markers)
                mask=cv2.bitwise_not(mask)
                img2[:,:,:]=mask[:,:,:]/255
                imgt=img2*frame_markers
                imgt=imgt+img3
        else:
            cap = cv2.VideoCapture("alien.mp4")
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
            break
        imgt=cv2.flip(imgt,1)
        cv2.imshow('frame',imgt)

img_insert = cv2.imread('nave.jpg',1)
obstaculo = cv2.imread('asteroid.jpg',1)
vid = cv2.VideoCapture(0)
ret, frame = vid.read()
largo,ancho,dim= np.shape(frame)
img3 = np.zeros((largo,ancho,dim),np.uint8)
img2 = np.ones((largo,ancho,dim),np.uint8)
img4 = np.zeros((largo,ancho,dim),np.uint8)
type=0
dib=False
vert=list()
points = list()
while True :  
    ret, frame = vid.read()
    vert,frame_markers=get_vert_markers(frame)
    imgt=frame
    if vert !=[] and dib:
        x=int((vert[0][0]-vert[1][0])/2)+vert[1][0]
        y=int((vert[0][1]-vert[3][1])/2)+vert[3][1]
        cv2.circle(img3, (x,y), 1, (0, 0, 255), 10)
        cv2.circle(img2, (x,y), 1, (0, 0, 0), 10)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    if k == ord('r'):
        img2[:]= 1
        img3[:]= 0
    if k == ord('d'):
        if dib:
            dib=False
        else:
            dib=True
    if k == ord('v'):
        type=0
    if k == ord('w'):
        type=1
    if k == ord('m'):
        if type!=2:
            type=2
        else:
            type=0
            img2[:]= 1
            img3[:]= 0
    if k == ord('n'):
        if type!=3:
            type=3
        else:
            type=0
            img2[:]= 1
            img3[:]= 0
    if k== ord('a'):
        video()
        img2[:]= 1
        img3[:]= 0
    if k == ord('g'):
        game()
        img2[:]= 1
        img3[:]= 0
    if type == 1:
        cv2.imshow('frame',img2+img3)
    if type == 2:
        if vert !=[]:
            img2[:]= 1
            img3[:]= 0
            x=int((vert[0][0]-vert[1][0])/2)+vert[1][0]
            y=int((vert[0][1]-vert[3][1])/2)+vert[3][1]
            cv2.circle(img3, (x,y), 1, (0, 0, 255), 10)
            cv2.circle(img2, (x,y), 1, (0, 0, 0), 10)
    if type == 3:
        if vert !=[]:         
            mask,img3 = afin(np.float32([vert[0], vert[1], vert[2]]),img_insert,frame_markers)
            lower_color = np.array([0, 0, 0])
            upper_color = np.array([255, 255, 255])
            mask=cv2.bitwise_not(mask)
            img2[:,:,:]=mask[:,:,:]/255
            cv2.imshow('frame',imgt)
    imgt=img2*frame_markers
    imgt=imgt+img3
    imgt=cv2.flip(imgt,1)
    cv2.imshow('frame',imgt)
vid.release()
cv2.destroyAllWindows()
