import numpy as np
import cv2
import imutils
import matplotlib
import scipy.ndimage


cap = cv2.VideoCapture('./trial/trial2.mov')
kernel = np.ones((2,2),np.uint8)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Define the codec and create VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video_writer = cv2.VideoWriter('output.m4v', fourcc, 30.0, size, True)
fgbg= cv2.createBackgroundSubtractorMOG2(600, 400 ,0)
door_open = 0

#xcord at which fish is considered to be "crossing"
fish_thresh = 526

#xcord at which fish is considered to be "opening"

#Since door is openen manually, and fish starts moving as soon as door open a little bit, we consider door open as soon as
# there is a movement detected with the door

#This threshhold is not working sometimes
door_thresh = 574
fish_array = []

def detectObject(image, framecount):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    _, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    objects = np.zeros([gray.shape[0], gray.shape[1], 3], 'uint8')
    global door_open
    global fish_array
    for c in contours:
        # cv2.drawContours(objects, [c], -1, (255, 0, 255), -1)
        M = cv2.moments(c)
        cx = 0

        if(M['m00'] >0):
          cx = int(M['m10']/M['m00'])
        #identify fish and door

        # we only get the fish data after door is open
        if(cx == fish_thresh and door_open == 1):
            # The fish detectin works pretty well, but the door detection is very dodgy
            print ("fish detected at frame", framecount)
            fish_array.append(framecount)
        elif(cx ==door_thresh and door_open == 0):
            door_open = 1
            print ("door open detected at frame", framecount)
            break
    return

framecount = 0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        fgmask = fgbg.apply(frame)
        np_image_data = np.asarray(fgmask)
        rgb_split = np.empty(fgmask.shape, 'uint8')
        fgmask.shape
        rgb_split.shape
        rgb_split = cv2.merge([fgmask, fgmask, fgmask])


        framecount = framecount + 1

        detectObject(rgb_split, framecount)

        frameNumber = "Frame nb = {}".format(framecount)

        cv2.putText(rgb_split, frameNumber, (10, rgb_split.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0, 255), 1)

        cv2.line(rgb_split,(fish_thresh,0),(fish_thresh,rgb_split.shape[0]),(255,0,0),1)

        # also record a video to check correctness of detection
        video_writer.write(rgb_split)

        cv2.imshow('frame',rgb_split)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        print(fish_array)
        break

# cleanup the camera and close any open windows
cap.release()
video_writer.release()
cv2.destroyAllWindows()
print("\n\nBye bye\n")
