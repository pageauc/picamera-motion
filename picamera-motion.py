#!/usr/bin/python
#
#     Lightweight Motion Detection using python picamera libraries
#        based on code from raspberry pi forum by user utpalc
#        modified by Claude Pageau for this working example
#     ------------------------------------------------------------
# original code on github https://github.com/pageauc/picamera-motion

# This is sample code that can be used for further development
ver = "ver 1.8"

import os
mypath = os.path.abspath(__file__)
baseDir = mypath[0:mypath.rfind("/")+1]
baseFileName = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = baseFileName
print("%s %s  written by Claude Pageau" % (progName, ver))
print("---------------------------------------------")

try:
    from settings import *
except:
    print("ERROR : Could Not import settings.py")
    exit(1)

if verbose:
    print("INFO  : Loading python libraries .....")
else:
    print("INFO  : verbose output has been disabled verbose=False")

import picamera
import picamera.array
import datetime
import time

#------------------------------------------------------------------------------
def checkImagePath():
    # if imagePath does not exist create the folder
    if not os.path.isdir(imagePath):
        if verbose:
            print("INFO  : Creating Image Storage folder %s" % (imagePath))
        try:
            os.makedirs(imagePath)
        except:
            print("ERROR : Could Not Create Folder %s" % imagePath)
    return imagePath

#------------------------------------------------------------------------------
def getFileName(imagePath, imageNamePrefix, currentCount):
    rightNow = datetime.datetime.now()
    if imageNumOn :
        # could use os.path.join to construct file image path
        filename = imagePath + "/" + imageNamePrefix + str(currentCount) + ".jpg"
    else:
        filename = "%s/%s%04d%02d%02d-%02d%02d%02d.jpg" % ( imagePath, imageNamePrefix ,rightNow.year, rightNow.month, rightNow.day, rightNow.hour, rightNow.minute, rightNow.second)
    return filename

#------------------------------------------------------------------------------
def takeDayImage(filename):
    with picamera.PiCamera() as camera:
        camera.resolution = (imageWidth, imageHeight)
        # camera.rotation = cameraRotate #Note use imageVFlip and imageHFlip variables
        if imagePreview:
            camera.start_preview()
        camera.vflip = imageVFlip
        camera.hflip = imageHFlip
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'
        time.sleep(1)
        camera.capture(filename)
    if verbose:
        print("INFO  : takeDayImage (%ix%i) - Saved %s" % (imageWidth, imageHeight, filename))
    return filename

#------------------------------------------------------------------------------
def takeStreamImage():
    with picamera.PiCamera() as camera:
        camera.resolution = (streamWidth, streamHeight)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

#------------------------------------------------------------------------------
def scanMotion():
    motionFound = False
    data1 = takeStreamImage()
    while True:
        data2 = takeStreamImage()
        diffCount = 0;
        for h in range(0, streamHeight):
            for w in range(0, streamWidth):
                # get the diff of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if  diff > threshold:
                    diffCount += 1
                    if diffCount > sensitivity:
                        return w, h
        data1 = data2

#------------------------------------------------------------------------------
def motionDetection():
    print("INFO  : Scan for Motion threshold=%i (diff)  sensitivity=%i (num px's)..."  % (threshold, sensitivity))
    currentCount = imageNumStart
    while True:
        x, y = scanMotion()
        print("INFO  : Motion Found At xy(%i,%i) in stream wh(%i,%i)"
                                  %(x, y, streamWidth, streamHeight))
        filename = getFileName(imagePath, imageNamePrefix, currentCount)
        if imageNumOn:
            currentCount += 1
        takeDayImage( filename )

# Start Main Program Logic
if __name__ == '__main__':
    try:
        checkImagePath()
        motionDetection()
    except KeyboardInterrupt :
        print("")
        print("########################")
        print("# User Pressed ctrl-c")
        print("# Exiting %s" % progName)
        print("########################")





