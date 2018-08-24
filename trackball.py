import cv2
cap = cv2.VideoCapture('./trial/trial1.mov')
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

fish_thresh = 516
door_thresh = 572


framecount = 0

def draw_line(frame, framecount):
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
    pass

def onChange(trackbarValue):
    cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,frame = cap.read()
    draw_line(frame, trackbarValue)
    cv2.imshow("refvideo", frame)
    pass

cv2.namedWindow('refvideo')
cv2.createTrackbar( 'start', 'refvideo', 0, length, onChange )

onChange(0)
cv2.waitKey(0)

start = cv2.getTrackbarPos('start','refvideo')


cap.set(cv2.CAP_PROP_POS_FRAMES,start)
while cap.isOpened():
    err,frame = cap.read()
    draw_line(frame, start)
    cv2.imshow("refvideo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()
print("\n\nBye bye\n")
