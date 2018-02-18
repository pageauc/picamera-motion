#!/bin/bash
echo "picamera-motion  Install  written by Claude Pageau"
echo "INFO  : Create picamera-motion Folders ..."
cd ~
mkdir -p picamera-motion
cd picamera-motion
mkdir -p images
echo "INFO  : Install Dependencies ...."
sudo apt-get install -yq python-imaging
sudo apt-get install -yq python-picamera
sudo apt-get install -yq python3-picamera
sudo apt-get install -yq dos2unix
sudo apt-get install -yq pandoc # convert markdown to plain text for Readme.md

echo "INFO  : Download Project Files ..."
wget -O picamera-motion.py https://raw.github.com/pageauc/picamera-motion/master/picamera-motion.py
wget -O picamera-motion.sh https://raw.github.com/pageauc/picamera-motion/master/picamera-motion.sh
wget -O settings.py https://raw.github.com/pageauc/picamera-motion/master/settings.py
wget -O menubox.sh https://raw.github.com/pageauc/picamera-motion/master/menubox.sh
wget -O webserver.py https://raw.github.com/pageauc/picamera-motion/master/webserver.py
wget -O webserver.sh https://raw.github.com/pageauc/picamera-motion/master/webserver.sh
wget -O rclone-sync.sh https://raw.github.com/pageauc/picamera-motion/master/rclone-sync.sh
wget -O Readme.md https://raw.github.com/pageauc/picamera-motion/master/Readme.md

if [ ! -f /usr/bin/rclone ]; then
    mkdir -p rclone-tmp
    # Install rclone with latest version
    echo "INFO  : Install Latest Rclone from https://downloads.rclone.org/rclone-current-linux-arm.zip"
    wget -O rclone.zip -q --show-progress https://downloads.rclone.org/rclone-current-linux-arm.zip
    echo "INFO  : unzip rclone.zip to folder rclone-tmp"
    unzip -o -j -d rclone-tmp rclone.zip
    echo "INFO  : Install files and man pages"
    cd rclone-tmp
    sudo cp rclone /usr/bin/
    sudo chown root:root /usr/bin/rclone
    sudo chmod 755 /usr/bin/rclone
    sudo mkdir -p /usr/local/share/man/man1
    sudo cp rclone.1 /usr/local/share/man/man1/
    sudo mandb
    cd ..
    echo "INFO  : Deleting rclone.zip and Folder rclone-tmp"
    rm rclone.zip
    rm -r rclone-tmp
    echo "INFO  : /usr/bin/rclone Install Complete"
fi

chmod +x *py
chmod +x *sh
chmod -x settings.py
dos2unix -q *

echo "
Install Complete. For Details See Readme.txt
To Run

    cd ~/picamera-motion
    python ./picamera-motion.py

To Run menubox.sh

    cd ~/picamera-motion
    ./menubox.sh

To Sync Data To an Existing Remote Storage Service name Eg. gdmedia using rclone

    cd ~/picamera-motion
    ./rclone-sync.sh

Good Luck Claude ..
"
