# Tracking skeleton and exporting live feed to Unity
# https://www.youtube.com/watch?v=icS2yforZpw

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--tracker", type=str, default="kcf",
	help="OpenCV object tracker type")
args = vars(ap.parse_args())

# extract the OpenCV version info
(major, minor) = cv2.__version__.split(".")[:2]
# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker
if int(major) == 3 and int(minor) < 3:
	tracker = cv2.Tracker_create(args["tracker"].upper())
# otherwise, for OpenCV 3.3 OR NEWER, we need to explicitly call the
# appropriate object tracker constructor:
else:
	# initialize a dictionary that maps strings to their corresponding
	# OpenCV object tracker implementations
	OPENCV_OBJECT_TRACKERS = {
		"csrt": cv2.TrackerCSRT_create,
		"kcf": cv2.TrackerKCF_create,
		#"boosting": cv2.TrackerBoosting_create,
		"mil": cv2.TrackerMIL_create,
		#"tld": cv2.TrackerTLD_create,
		#"medianflow": cv2.TrackerMedianFlow_create,
		#"mosse": cv2.TrackerMOSSE_create
	}
	# grab the appropriate object tracker using our dictionary of
	# OpenCV object tracker objects
	tracker = OPENCV_OBJECT_TRACKERS[args["tracker"]]()
# initialize the bounding box coordinates of the object we are going
# to track
initBB = None

cap = cv2.VideoCapture(0)

fps = None

# loop over frames from the video stream
while True:
	ret, frame = cap.read()
	#width = int(cap.get(3))
	#height = int(cap.get(4))
	
    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
	frame = imutils.resize(frame, width=500)
	(H, W) = frame.shape[:2]

	# check to see if we are currently tracking an object
	if initBB is not None:
	    # grab the new bounding box coordinates of the object
		(success, box) = tracker.update(frame)

	    # check to see if the tracking was a success
		if success:
			(x, y, w, h) = [int(v) for v in box]
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
	    # update the FPS counter
		fps.update()
		fps.stop()
	    # initialize the set of information we'll be displaying on
	    # the frame
		info = [
		    ("Tracker", args["tracker"]),
		    ("Success", "Yes" if success else "No"),
		    ("FPS", "{:.2f}".format(fps.fps())),
	    ]
	    # loop over the info tuples and draw them on our frame
		for (i, (k, v)) in enumerate(info):
			text = "{}: {}".format(k, v)
			cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
		        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
		
	cv2.imshow("Frame", frame)

	key = cv2.waitKey(1) & 0xFF

	# if 's' key, "select" a bounding box to track
	if key == ord('s'):
		# select the bounding box of obj to track
		# make sure press ENTER or SPACE after selecting ROI
		intitBB = cv2.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)

		# start OpenCV obj tracker using the supplied
		# bounding box coordinates, then start the FPS
		tracker.init(frame, initBB)
		fps = FPS().start()
	elif key == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()