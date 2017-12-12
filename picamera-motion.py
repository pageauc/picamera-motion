#!/usr/bin/python
#
#     Lightweight Motion Detection using python picamera libraries
#        based on code from raspberry pi forum by user utpalc
#        modified by Claude Pageau for this working example
#     ------------------------------------------------------------
# original code on github https://github.com/pageauc/picamera-motion

# This is sample code that can be used for further development
ver = "ver 1.5"

import os
mypath = os.path.abspath(__file__)
baseDir = mypath[0:mypath.rfind("/")+1]
baseFileName = mypath[mypath.rfind("/")+1:mypath.rfind(".")]
progName = baseFileName
print("%s %s  written by Claude Pageau and utpalc" % (progName, ver))
print("---------------------------------------------")

verbose = True   # Display Logging Messages True=on False=off

# User Image Settings
# -------------------
imageDir = "images"
imagePath = baseDir + imageDir  # Where to save the images
imageNamePrefix = 'mo-'         # Prefix for all image file names. Eg front-
imageWidth = 1920    # Final image width
imageHeight = 1080   # Final image height
imageVFlip = False   # Flip image Vertically
imageHFlip = False   # Flip image Horizontally
imagePreview = False # Set picamera preview False=off True=on
imageNumOn = False   # Image Naming True=Number sequence  False=DateTime
imageNumStart = 1000 # Start of number sequence if imageNumOn=True

# User Motion Detection Settings
# ------------------------------
threshold = 10  # How Much pixel changes
sensitivity = 100  # How many pixels change
streamWidth = 128  # motion scan stream Width
streamHeight = 80

if verbose:
    print("Loading python libraries .....")
else:
    print("verbose output has been disabled verbose=False")

import picamera
import picamera.array
import datetime
import time

#------------------------------------------------------------------------------
def checkImagePath(imagedir):
    # if imagePath does not exist create the folder
    if not os.path.isdir(imagePath):
        if verbose:
            print("Creating Image Storage folder %s" % (imagePath))
        try:
            os.makedirs(imagePath)
        except:
            print("ERROR - Could Not Create Folder %s" % imagePath)
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
def takeDayImage(imageWidth, imageHeight, filename):
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
        print("takeDayImage - Captured %s" % (filename))
    return filename

#------------------------------------------------------------------------------
def takeStreamImage(width, height):
    with picamera.PiCamera() as camera:
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            return stream.array

#------------------------------------------------------------------------------
def scanMotion(width, height):
    motionFound = False
    data1 = takeStreamImage(width, height)
    while not motionFound:
        data2 = takeStreamImage(width, height)
        diffCount = 0;
        for w in range(0, width):
            for h in range(0, height):
                # get the diff of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if  diff > threshold:
                    diffCount += 1
            if diffCount > sensitivity:
                break; #break outer loop.
        if diffCount > sensitivity:
            motionFound = True
        else:
            data1 = data2
    return motionFound

#------------------------------------------------------------------------------
def motionDetection():
    print("Scanning for Motion threshold=%i sensitivity=%i ......"  % (threshold, sensitivity))
    currentCount = imageNumStart
    while True:
        if scanMotion(streamWidth, streamHeight):
            filename = getFileName(imagePath, imageNamePrefix, currentCount)
            if imageNumOn:
                currentCount += 1
            takeDayImage( imageWidth, imageHeight, filename )

# Start Main Program Logic
if __name__ == '__main__':
    try:
        checkImagePath(imageDir)
        motionDetection()
    except:
        print("")
        print("+++++++++++++++")
        print("Exiting %s" % progName)
        print("+++++++++++++++")





