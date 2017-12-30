#!/bin/bash
echo "picamera-motion  Install  written by Claude Pageau"
echo "Make picamera-motion Folders ..."
cd ~
mkdir -p picamera-motion
cd picamera-motion
mkdir -p images
echo "Install Dependencies ...."
sudo apt-get install python-imaging
sudo apt-get install python-picamera python3-picamera
echo "Download Project Files ..."
wget -O picamera-motion.py https://raw.github.com/pageauc/picamera-motion/master/picamera-motion.py
wget -O rclone-sync.sh https://raw.github.com/pageauc/picamera-motion/master/rclone-sync.sh
wget -O install.sh https://raw.github.com/pageauc/picamera-motion/master/install.sh
wget -O Readme.md https://raw.github.com/pageauc/picamera-motion/master/Readme.md
chmod +x picamera-motion.py
chmod +x *sh
if [ -f /usr/bin/rclone ]; then
   echo "Rclone already installed at /usr/bin/rclone"
else
   echo "Installing rclone to /usr/bin/rclone Please Wait ..."
   curl -L https://raw.github.com/pageauc/rclone4pi/master/rclone-install.sh | bash
fi
cd ..
echo "
Install Complete. For Details See Readme.txt
To Run

    cd ~/picamera-motion
    python ./picamera-motion.py

To Sync Data To an Existing Remote Storage Service name Eg. gdmedia using rclone

    cd ~/picamera-motion
    ./rclone-sync.sh

Good Luck Claude ..
"
