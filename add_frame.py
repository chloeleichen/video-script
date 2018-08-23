# USAGE
# python script_name.py --video video_example.mp4
# python script_name.py

# python script_name.py -o savedvideo.avi --picamera 1

# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import imutils 								# "tool box" for handling videos
import cv2
import datetime                             # used to put the timestamp



# construct the argument parse and parse the arguments
# the switch --video is the optional path to the video
# if the switch is not supplied, OpenCV will try accessing the webcam
# the argument --buffer is the maximum size of the deque (i.e. list of previous (x,y) coordinates of the ball)
# small deque leads to a shorter "contrail" (i.e. tail of the tracked object)
# --picamera : specify if we want to use the RSBPi camera module
# --output : path to where the output video fill will be stores on disk
# --fps : the desired FPS of the output video (idealy should be similar to the FPS of the videoprocessing pipeline)
# --codec: supply the FourCC ("four character code"),  an an identifier for the video codec,
# compression format, color/pixel format of the video . could be MJPG, etc
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-o", "--output", required=True,
    help="path to output video file")
ap.add_argument("-p", "--picamera", type=int, default=-1,
    help="whether or not the Raspberry Pi camera should be used")
ap.add_argument("-f", "--fps", type=int, default=25,
    help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="MJPG",
    help="codec of output video")
args = vars(ap.parse_args())


# initialize the FourCC, using cv2.VideoWriter_fourcc function,
# video writer, dimensions of the frame
fourcc = cv2.VideoWriter_fourcc(*args["codec"])

# variables for writing the videos
writer = None
(h, w) = (None, None)
# set the counter for the frame numbers
fnumber = 0

# if a video path was not supplied, grab the reference to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture(0)
# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# keep looping until(1) we press the q key to terminate the script or
# (2) the video files reaches to its end
while True:
	# grab the current frame by calling the .read() method
	# returns two values: (1) grabbed (boolean indicating whether reading the frame was successful)
	# (2) frame, which is the frame itself
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# pre-processing: resize the frame, blur it, etc
	frame = imutils.resize(frame, width=800) # resize with width of 600pixels

	# draw the timestamp an the frame
	#timestamp = datetime.datetime.now()
	#ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
	#cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
    	#    0.35, (0,0, 255), 1)

	# draw the frame number an the frame
	fnumber = fnumber + 1
	frameNumber = "Frame nb = {}".format(fnumber)
	cv2.putText(frame, frameNumber , (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0,0, 255), 1)

	# show the frame to our screen
	cv2.imshow("Frame", frame)


### get everthing ready to write the video ##################################################################
# check if the writer is None (if it is, we need to initialize it)
	if writer is None:
		# store the image dimensions, initialzie the video writer,
		# and construct the zeros array
		(h, w) = frame.shape[:2] # grab the spatial dimension of the frame
		# instantiate the cv2.VideoWriter (parameters: path to output video; ourCC codec;
		# desired FPS of output video; width & height of output video, True/False for color frames)
		writer = cv2.VideoWriter(args["output"], fourcc, args["fps"],
			(w * 1, h * 1), True) # use  (w * 1, h * 1) to write only one image
		# construct the final output frame
		output = frame
		# write the output frame to file
	writer.write(output)




	# if the 'q' key is pressed, stop the loop
	key = cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break
# Get the outputs I need
print("[INFO] originalvideo.avi has been written...")

# cleanup the camera and close any open windows
print("[INFO] cleaning up...")
camera.release()
cv2.destroyAllWindows()
writer.release() # ensure the output video file pointer is released
