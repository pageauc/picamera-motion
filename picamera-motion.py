#!/usr/bin/python
"""
 Lightweight Motion Detection using python picamera libraries.
 Requires a Raspberry Pi computer with a picamera module.
 This code is based on a raspberry pi forum post by user utpalc
 modified by Claude Pageau for this working example.

 This project can be used for further development
 and is located on GitHub at
 https://github.com/pageauc/picamera-motion

 For a full featured program see my GitHub pi-timolo project at
 https://github.com/pageauc/pi-timolo
"""

import os
import datetime
import time
import picamera
import picamera.array
if not os.path.exists('settings.py'):
    print("ERROR : File Not Found - settings.py")
    print("        Cannot import program variables.")
    print("        To Repair Run menubox.sh UPGRADE menu pick.")
    exit(1)
try:
    from settings import *
except ImportError:
    print("ERROR : Could Not Import settings.py")
    exit(1)

PROG_VER = "ver 2.5"
SCRIPT_PATH = os.path.abspath(__file__)
# get script file name without extension
PROG_NAME = SCRIPT_PATH[SCRIPT_PATH.rfind("/")+1:SCRIPT_PATH.rfind(".")]
SCRIPT_DIR = SCRIPT_PATH[0:SCRIPT_PATH.rfind("/")+1] # get script directory
# conversion from stream coordinate to full image coordinate
X_MO_CONV = imageWidth/float(streamWidth)
Y_MO_CONV = imageHeight/float(streamHeight)

#------------------------------------------------------------------------------
def get_now():
    """ Get datetime and return formatted string"""
    right_now = datetime.datetime.now()
    now = ("%04d%02d%02d-%02d:%02d:%02d"
           % (right_now.year, right_now.month, right_now.day,
              right_now.hour, right_now.minute, right_now.second))
    return now

#------------------------------------------------------------------------------
def check_image_dir(image_dir):
    """ if image_dir does not exist create the folder """
    if not os.path.isdir(image_dir):
        if verbose:
            print("INFO  : Creating Image Storage folder %s" % (image_dir))
        try:
            os.makedirs(image_dir)
        except OSError as err:
            print("ERROR : Could Not Create Folder %s %s" % (image_dir, err))
            exit(1)

#------------------------------------------------------------------------------
def get_file_name(image_dir, image_name_prefix, current_count):
    """
    Create a file name based on settings.py variables
    Note image numbering will not be saved so restarting
    will restart image numbering and overwrite previous images.
    Set imageNumOn=False to save image in datetime format to
    make image name unique and avoid overwriting previous image.

    See pi-timolo.py getCurrentCount function for using glob to
    extract the most recent number counter from saved images.
    """
    if imageNumOn:
        # you could also use os.path.join to construct image path file_path
        file_path = image_dir+ "/"+image_name_prefix+str(current_count)+".jpg"
    else:
        right_now = datetime.datetime.now()
        file_path = ("%s/%s%04d%02d%02d-%02d%02d%02d.jpg"
                     % (image_dir, image_name_prefix,
                        right_now.year, right_now.month, right_now.day,
                        right_now.hour, right_now.minute, right_now.second))
    return file_path

#------------------------------------------------------------------------------
def take_day_image(image_path):
    """ Take a picamera image """
    with picamera.PiCamera() as camera:
        camera.resolution = (imageWidth, imageHeight)
        # camera.rotation = cameraRotate
        # Note use imageVFlip and imageHFlip settings.py variables
        if imagePreview:
            camera.start_preview()
        camera.vflip = imageVFlip
        camera.hflip = imageHFlip
        camera.exposure_mode = 'auto'
        camera.awb_mode = 'auto'
        time.sleep(1)
        camera.capture(image_path)
        camera.close()
    return image_path

#------------------------------------------------------------------------------
def get_stream_array():
    """ Take a stream image and return the image data array"""
    with picamera.PiCamera() as camera:
        camera.resolution = (streamWidth, streamHeight)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.vflip = imageVFlip
            camera.hflip = imageHFlip
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto'
            camera.capture(stream, format='rgb')
            camera.close()
            return stream.array

#------------------------------------------------------------------------------
def scan_motion():
    """ Loop until motion is detected """
    data1 = get_stream_array()
    while True:
        data2 = get_stream_array()
        diff_count = 0
        for y in range(0, streamHeight):
            for x in range(0, streamWidth):
                # get pixel differences. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[y][x][1]) - int(data2[y][x][1]))
                if  diff > threshold:
                    diff_count += 1
                    if diff_count > sensitivity:
                        # x,y is a very rough motion position
                        return x, y
        data1 = data2

#------------------------------------------------------------------------------
def do_motion_detection():
    """
    Loop until motion found then take an image,
    and continue motion detection. ctrl-c to exit
    """
    current_count = imageNumStart
    while True:
        x_pos, y_pos = scan_motion()
        file_name = get_file_name(imagePath, imageNamePrefix, current_count)
        if imageNumOn:
            current_count += 1
        take_day_image(file_name)
        # Convert xy movement location for full size image
        mo_x = x_pos * X_MO_CONV
        mo_y = y_pos * Y_MO_CONV
        if verbose:
            print("%s INFO  : Motion xy(%d,%d) Saved %s (%ix%i)"
                  % (get_now(), mo_x, mo_y, file_name,
                     imageWidth, imageHeight,))

# Start Main Program Logic
if __name__ == '__main__':
    print("%s %s  written by Claude Pageau" % (PROG_NAME, PROG_VER))
    print("---------------------------------------------")
    check_image_dir(imagePath)
    print("%s INFO  : Scan for Motion "
          "threshold=%i (diff)  sensitivity=%i (num px's)..."
          % (get_now(), threshold, sensitivity))
    if not verbose:
        print("%s WARN  : Messages turned off per settings.py verbose = %s"
              % (get_now(), verbose))
    try:
        do_motion_detection()
    except KeyboardInterrupt:
        print("")
        print("INFO  : User Pressed ctrl-c")
        print("        Exiting %s %s " % (PROG_NAME, PROG_VER))
