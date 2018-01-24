#  Lightweight python Motion Detection

## Summary
Based on original code written by brainflakes and modified by pageauc
user utpalc rewrote motion detection using picamera stream and pageauc
modified this sample code to this example application
This code uses the picamera python libraries rather than raspistill.
Posted on Raspberry Pi forum under Lightweight Python Motion Detection
Sample video posted at http://youtu.be/ZuHAfwZlzqY
Code modified to exit image scanning loop as soon as the sensitivity value
is exceeded. This speeds taking larger photo if motion detected early in scan
Code is python3 compatible.
This code is available on github at https://github.com/pageauc/picamera-motion

***Note:*** This is basically sample code to assist development. For a full feature app
see my pi-timolo repo at https://github.com/pageauc/pi-timolo

## Install Instructions
Log in to RPI using putty ssh or raspberry pi console terminal session
then Cut and Paste curl command below into RPI console

    curl -L https://raw.github.com/pageauc/picamera-motion/master/install.sh | bash

## How To Test Run

    cd ~/picamera-motion
    ./picamera-motion.py

## How To Change Settings
Use menubox.sh to Edit and/or Start/Stop picamera-motion.py and/or webserver.py in Background

    ./menubox.sh

Edit settings.py using nano or python IDLE.

    nano settings.py

ctrl x y to Save Changes and Exit nano

## How to Upload Images
Uploading images to a Remote Storage Service. For Details
See https://github.com/pageauc/rclone4pi/wiki

To Run rclone sync (You Must have a Remote Service Name Configured)

    ./rclone-sync.sh

Review output for further details or trouble shooting

That's it
Please note this code is pretty basic but a good learning tool if
you need to implement a simple python only motion detection application
using the picamera python libraries.

Claude Pageau