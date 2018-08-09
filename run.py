
import numpy as np
import cv2


def main():

    # default cam matrix rows and columns
    cap = cv2.VideoCapture(0)  # use external cam
    
    #create video
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640,480))
    # get the background and resize it.
    img_back = cv2.imread('background.jpg')
    vidcap = cv2.VideoCapture('bg1Trim.mp4')
    success,image = vidcap.read()
    while True:

        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_limit = np.array([50,90,70])
        upper_limit = np.array([90,255,255])

        cols, rows = frame.shape[:2]
        success, img_back=vidcap.read()
        if(not success):
            vidcap = cv2.VideoCapture('bg1.mp4')
            success,img_back = vidcap.read()
        background = img_back[120:cols+120, 319:rows+319]

        #create the mask
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        #smooth the mask
        #kernel = np.ones((5,5),np.float32)/25
        #mask = cv2.filter2D(mask,-1,kernel)
        #mask  = cv2.inRange(mask, 0,0.4 )

        #apply the mask
        bground   = cv2.bitwise_and(background,background, mask= mask)

        res = cv2.bitwise_and(frame,frame, mask= cv2.bitwise_not(mask))        
        res= np.add(res , bground)
        res=cv2.flip(res,1)
        out.write(res)
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.namedWindow('res', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res', 1280,960)
        cv2.imshow('res',res)

        k = cv2.waitKey(33)
        if k == 27:  # ESC
            break
    cap.release()
    out.release()

if __name__ == "__main__":
    main()
