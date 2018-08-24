import numpy as np
import cv2
import imutils
import matplotlib
import scipy.ndimage


fish_thresh = 526
door_thresh = 572

def parseVideo(input, output):
    global door_open
    global framecount
    global fish_array
    global door_open_frame

    door_open = 0
    framecount = 0
    fish_array = []
    door_open_frame = 0

    cap = cv2.VideoCapture(input)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    kernel = np.ones((2,2),np.uint8)
    fgbg= cv2.createBackgroundSubtractorMOG2(600, 400 ,0)
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video_writer = cv2.VideoWriter(output, fourcc, 30.0, size, True)


    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret==True:
            fgmask = fgbg.apply(frame)
            # fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

            rgb_split = np.empty(fgmask.shape, 'uint8')
            rgb_split = cv2.merge([fgmask, fgmask, fgmask])

            framecount = framecount + 1

            detectObject(rgb_split, framecount)

            frameNumber = "Frame nb = {}".format(framecount)

            cv2.putText(rgb_split,
                        frameNumber,
                        (10, rgb_split.shape[0] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.35,
                        (0,0, 255),
                        1)

            # draw fish threshhold
            cv2.line(rgb_split,
                     (fish_thresh,0),
                     (fish_thresh,
                     rgb_split.shape[0]),
                     (255,0,0),
                     1)

            #draw door threshhold
            cv2.line(rgb_split,
                     (door_thresh,0),
                     (door_thresh,rgb_split.shape[0]),
                     (241, 196, 15),
                     1)

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




def detectObject(image, framecount):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    thresh = cv2.adaptiveThreshold(gray,
                                   255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY,
                                   115,
                                   1)
    _, contours, hierarchy = cv2.findContours(thresh,
                                              cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)
    objects = np.zeros([gray.shape[0], gray.shape[1], 3], 'uint8')
    global door_open
    global fish_array
    for c in contours:
        # cv2.drawContours(objects, [c], -1, (255, 0, 255), -1)
        M = cv2.moments(c)
        cx = 0
        area = cv2.contourArea(c)

        if(M['m00'] >0):
          cx = int(M['m10']/M['m00'])
        #identify fish and door
        # we only get the fish data after door is open
        if(cx == fish_thresh and door_open == 1):
            print ("fish detected at frame", framecount)
            fish_array.append(framecount)
        elif(cx ==door_thresh and door_open == 0):
            if(area > 3500):
              door_open = 1
              print ("door open detected at frame", framecount)
              break
    return

parseVideo('./trial/trial2.mov', 'output.m4v')
