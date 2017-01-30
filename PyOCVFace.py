"""

    A demonstration for face and object detection using haar-like features.
    Faces are found in a video stream and a red box is drawn around them.
    
    Because of a bug in OpenCV on Mac OS X, the camera window may not close
    after the program is ended, in which case you will need to
    "Force Quit" Python.

Modified (26 January 2016) to opencv 3.1.0 and Python 3 by Simon Oliver

    from the example by Donald J. Woodbury and David C. Bailey (dbailey@physics.utoronto.ca)
    which is from Jo Vermeulen retrieved from
    http://blog.jozilla.net/2008/06/27/fun-with-python-opencv-and-face-detection/,(License: Not known)
    which in turn is based on a script by Nirav Patel from
    http://eclecti.cc/olpc/face-detection-on-the-olpc-xo (License: http://creativecommons.org/licenses/by/3.0/us/)
    which is derived from the facedetect.py example by Roman Stanchak & James Bowman,
         available from http://sourceforge.net/projects/opencvlibrary/.
    OpenCV is available under the BSD License (http://opencv.willowgarage.com/wiki/).
    The modifications by Woodbury and Bailey are released
        under the MIT License - http://www.opensource.org/licenses/mit-license.php.

"""

import sys
import cv2
import os
import serial

cascPath = os.path.abspath('C:\Users\Simon\TurretPython\haarcascade_frontalface_alt.xml')
faceCascade = cv2.CascadeClassifier(cascPath)


def detect_and_draw(image):
    cv2.namedWindow("Camera")
    # convert color input image to grayscale
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # equalize histogram
    cv2.equalizeHist(grayscale, grayscale)
    # detect objects
    faces = faceCascade.detectMultiScale(
        grayscale,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    if len(faces) > 0:
        print('face detected!    Press Escape to exit program.')
        for (x, y, w, h) in faces:
            print(x, y, w, h)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 1)
            cv2.circle(image, (x+w/2, y+h/2), abs(w/4), (0, 255, 0), 1)
            # calculate offsets
            x1 = x+w
            y1 = h+y
            x2 = x
            y2 = y
            # pan tilt new location
            xx = int((x1+x2)/2)
            yy = int((y1+y2)/2)
            output = "X{0:d}Y{1:d}Z".format(xx, yy)
            print("output = '" + output + "'")
            # tell arduino where to point
            serialConnection.write(output)
 
if __name__ == "__main__":
    print(cv2.__version__)
    print("Press ESC to exit ...")
    # configure the serial connections (the parameters differs on the device you are connecting to)
    serialConnection = serial.Serial('COM3', 9600)
    # create window
    cv2.namedWindow('Camera')
    # create capture device
    capture = cv2.VideoCapture(1)
    # check if capture device is OK
    if not capture:
        print("Error opening capture device")
        sys.exit(1)
    if not serialConnection:
        print("Error connecting to serial device")
        sys.exit(1)
    while True:
        # do forever
        # capture the current frame
        ret, frame = capture.read()
        if frame is None:
            break
        # mirror
        cv2.flip(frame, 0)
        # face detection
        detect_and_draw(frame)
        # display webcam image
        cv2.imshow('Camera', frame)
        # handle events
        # As long as camera window has focus (e.g. is selected), this will intercept
        # pressed key; it will not work if the python terminal window has focus
        k = cv2.waitKey(50)
        if k == 0x1b:
            print('ESC pressed. Exiting ...')
            cv2.destroyWindow("Camera")  # This may not work on a Mac
            capture.release()
            serialConnection.close()
            break
