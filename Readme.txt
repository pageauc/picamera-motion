                  Lightweight python Motion Detection
                         picamera Lite version
                  -----------------------------------
Summary
-------
based on original code written by brainflakes and modified by pageauc
This code uses the picamera python libraries rather than raspistill.
Posted on Raspberry Pi forum under Lightweight Python Motion Detection
Sample video posted at http://youtu.be/ZuHAfwZlzqY
Code modified to exit image scanning loop as soon as the sensitivity value
is exceeded. This speeds taking larger photo if motion detected early in scan
This code is available on github at https://github.com/pageauc/picamera-motion
Note:
This version does not uses picamera python libraries but does not integrate
give synchronization.

Install Instructions
--------------------
1. Log in to RPI using putty ssh or raspberry pi console terminal session
2. To install perform the following commands

cd ~
mkdir pimotion
cd pimotion
mkdir images
sudo apt-get install python imaging
wget https://raw.github.com/pageauc/picamera-motion/master/picamera-motion.py
wget https://raw.github.com/pageauc/picamera-motion/master/Readme.txt
python ./picamera-motion.py


Tuning
------
To change motion detection settings edit the pimotion.py file using nano
it is recommended you make a backup copy just in case.
from a logged in putty ssh or console terminal session perform.  You
can also use IDLE if desired.
   
That's it
Please note this code is pretty basic but a good learning tool if
you need to implement a simple python only motion detection application.

Claude Pageau