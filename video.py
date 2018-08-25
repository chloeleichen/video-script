import numpy as np
import cv2
import imutils
import matplotlib
import pandas as pd
import scipy.ndimage



def parseVideo(input, output, offset):
    global door_open
    global framecount
    global fish_array
    global door_open_frame
    global fish_thresh
    global door_thresh

    framecount = 0
    fish_array = []
    door_open_frame = 0
    fish_thresh = 514 + offset
    door_thresh = 570 + offset

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
            detectObject(rgb_split, framecount)


            framecount = framecount + 1
            frameNumber = 'Frame nb = {}'.format(framecount)

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
                     (fish_thresh,rgb_split.shape[0]),
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
            fish_np_array = np.array(fish_array)
            break

    # cleanup the camera and close any open windows
    cap.release()
    video_writer.release()
    cv2.destroyAllWindows()
    print('\n\nBye bye\n')

    return fish_np_array/door_open_frame


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
    # objects = np.zeros([gray.shape[0], gray.shape[1], 3], 'uint8')

    global fish_array
    global door_open_frame

    for c in contours:
        # cv2.drawContours(objects, [c], -1, (255, 0, 255), -1)
        M = cv2.moments(c)
        cx = 0
        area = cv2.contourArea(c)

        if(M['m00'] >0):
          cx = int(M['m10']/M['m00'])
        #identify fish and door
        # we only get the fish data after door is open
        if(cx == fish_thresh and door_open_frame > 0):
            print ('fish detected at frame', framecount)
            fish_array.append(framecount)

        elif(cx ==door_thresh and door_open_frame == 0):
            if(area > 3500):
              door_open_frame = framecount
              print ('door open detected at frame', framecount)
              break
    return



def main():
    source = {'trial1': {'id': 1, 'offset': 2},'trial3': {'id': 3, 'offset': 4}, 'trial4': {'id': 4, 'offset': 4}, 'trial5': {'id': 5, 'offset': 0}, 'trial6': {'id': 6, 'offset': -5}, 'trial7': {'id': 7, 'offset': -2}, 'trial8': {'id': 8, 'offset': -1}, 'trial9': {'id': 9, 'offset': -4}}
    data = np.empty([0, 2])

    for key in source:
        input = './trial/' + key +'.mov'
        output = './trial/' + key +'.m4v'
        location_array = parseVideo(input, output, source[key]['offset'])
        table = np.reshape(location_array, (len(location_array), 1))
        table_w_id = np.insert(table, 0, source[key]['id'], axis = 1)
        data = np.append(data, table_w_id, axis=0)

    print(data)

    df = pd.DataFrame({'id':data[:,0],'value':data[:,1]})
    df.to_csv('output.csv')


if __name__ == '__main__': main()
