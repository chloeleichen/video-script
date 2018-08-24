import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture('./trial/trial1.mov')

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fish_thresh = 516
door_thresh = 572

# Define the codec and create VideoWriter object to save the video
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
video_writer = cv2.VideoWriter('./trial/trial1.m4v', fourcc, 30.0, size, True)
framecount = 0

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        framecount = framecount + 1
        frameNumber = "Frame nb = {}".format(framecount)

        cv2.putText(frame,
                    frameNumber,
                    (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.35,
                    (0,0, 255),
                    1)
        # draw fish threshhold
        cv2.line(frame,
                 (fish_thresh,0),
                 (fish_thresh,frame.shape[0]),
                 (255,0,0),
                 1)

        #draw door threshhold
        cv2.line(frame,
                 (door_thresh,0),
                 (door_thresh,frame.shape[0]),
                 (241, 196, 15),
                 1)
        video_writer.write(frame)

        cv2.imshow('frame',frame)
        cv2.waitKey(0)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# cleanup the camera and close any open windows
cap.release()
video_writer.release()
cv2.destroyAllWindows()
print("\n\nBye bye\n")
