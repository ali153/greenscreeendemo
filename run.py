
import numpy as np
import cv2


def main():

    # default cam matrix rows and columns
    cap = cv2.VideoCapture(0)  # use external cam

    # get the background and resize it.
    img_back = cv2.imread('background.jpg')
    vidcap = cv2.VideoCapture('bg1.mp4')
    success,image = vidcap.read()
    while True:

        _, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_limit = np.array([50,50,20])
        upper_limit = np.array([90,255,255])
        weight=len(hsv)
        height=len(hsv[1])
        cols, rows = frame.shape[:2]
        success, img_back=vidcap.read()
        if(not success):
            vidcap = cv2.VideoCapture('bg1.mp4')
            success,img_back = vidcap.read()
        background = img_back[200:cols+200, 120:rows+120]

        #create the mask
        mask = cv2.inRange(hsv, lower_limit, upper_limit)
        #smooth the mask
        kernel = np.ones((3,3),np.float32)/9
        #mask = cv2.filter2D(mask,-1,kernel)



        #apply the mask
        bground   = cv2.bitwise_and(background,background, mask= mask)

        res = cv2.bitwise_and(frame,frame, mask= cv2.bitwise_not(mask))
        res= np.add(res , bground)
        cv2.imshow('frame',frame)
        cv2.imshow('mask',mask)
        cv2.namedWindow('res', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('res', 1280,960)
        cv2.imshow('res',res)

        k = cv2.waitKey(33)
        if k == 27:  # ESC
            break

if __name__ == "__main__":
    main()
