import numpy as np
import cv2
import imutils
import matplotlib
import scipy.ndimage

cap = cv2.VideoCapture('/Users/chloe/sites/ml/test.mov')
kernel = np.ones((2,2),np.uint8)

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define the codec and create VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video_writer = cv2.VideoWriter('output.m4v', fourcc, 30.0, size, True)
fgbg= cv2.createBackgroundSubtractorMOG2(600, 400 ,0)


def detectObject(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("Binary", thresh)

    objects = np.zeros([gray.shape[0], gray.shape[1], 3], 'uint8')

    detected = 0
    for c in contours:
        # cv2.drawContours(objects, [c], -1, (255, 0, 255), -1)
        M = cv2.moments(c)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.circle(objects, (cx, cy), 4, (0, 0, 255), -1)

        if(cx > 550 and cx < 560):
            detected = 1
    return detected



framecount = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        fgmask = fgbg.apply(frame)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        # frame_san_bg = cv2.erode(frame_san_bg,kernel,iterations = 1)
        # frame_san_bg = cv2.erode(frame_san_bg,kernel,iterations = 1)
        # write the substrated frame

        np_image_data = np.asarray(fgmask)
        rgb_split = np.empty(fgmask.shape, 'uint8')
        fgmask.shape
        rgb_split.shape
        rgb_split = cv2.merge([fgmask, fgmask, fgmask])

        #identify fish and door

        framecount = framecount + 1

        if detectObject(rgb_split) > 0:
            print (framecount)

        # break
        #
        video_writer.write(rgb_split)
        cv2.imshow('frame',rgb_split)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# cleanup the camera and close any open windows
cap.release()
video_writer.release()
cv2.destroyAllWindows()
print("\n\nBye bye\n")
