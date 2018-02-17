#!/bin/bash

ver="1.7"

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

pyconfigfile="./settings.py"
filename_conf="./settings.conf"
filename_temp="./settings.conf.temp"

#------------------------------------------------------------------------------
function do_anykey ()
{
   echo ""
   echo "######################################"
   echo "#          Review Output             #"
   echo "######################################"
   read -p "  Press Enter to Return to Main Menu"
}

#------------------------------------------------------------------------------
function init_status ()
{
  if [ -z "$( pgrep -f webserver.py )" ]; then
     WEB_1="START"
     WEB_2="webserver.py in Background"
  else
     webserver_pid=$( pgrep -f webserver.py )
     WEB_1="STOP"
     WEB_2="webserver.py - PID is $webserver_pid"
  fi

  if [ -z "$( pgrep -f picamera-motion.py )" ]; then
     PICAM_1="START"
     PICAM_2="picamera-motion.py in Background"
  else
     picamera_motion_pid=$( pgrep -f picamera-motion.py )
     PICAM_1="STOP"
     PICAM_2="picamera-motion.py - PID is $picamera_motion_pid"
  fi

}

#------------------------------------------------------------------------------
function do_picamera_motion ()
{
  if [ -z "$( pgrep -f $DIR/picamera-motion.py )" ]; then
     $DIR/picamera-motion.py >/dev/null 2>&1 &
     if [ -z "$( pgrep -f $DIR/picamera-motion.py )" ]; then
         whiptail --msgbox "Failed to Start picamera-motion.py   Please Investigate Problem " 20 70
     fi
  else
     picamera_motion_pid=$( pgrep -f $DIR/picamera-motion.py )
     sudo kill $picamera_motion_pid
      if [ ! -z "$( pgrep -f $DIR/picamera-motion.py )" ]; then
          whiptail --msgbox "Failed to Stop picamera-motion.py   Please Investigate Problem" 20 70
      fi
  fi
  do_main_menu
}

#------------------------------------------------------------------------------
function do_webserver ()
{
  if [ -z "$( pgrep -f $DIR/webserver.py )" ]; then
     $DIR/webserver.py >/dev/null 2>&1 &
     if [ -z "$( pgrep -f $DIR/webserver.py )" ]; then
        whiptail --msgbox "Failed to Start webserver.py   Please Investigate Problem." 20 70
     else
       myip=$(ifconfig | grep 'inet ' | grep -v 127.0.0 | cut -d " " -f 12 | cut -d ":" -f 2 )
       myport=$( grep "web_server_port" settings.py | cut -d "=" -f 2 | cut -d "#" -f 1 | awk '{$1=$1};1' )
       whiptail --msgbox --title "Webserver Access" "Access picamera-motion web server from another network computer web browser using url http://$myip:$myport" 15 50
     fi
  else
     webserver_pid=$( pgrep -f $DIR/webserver.py )
     sudo kill $webserver_pid
     if [ ! -z "$( pgrep -f $DIR/webserver.py )" ]; then
        whiptail --msgbox "Failed to Stop webserver.py   Please Investigate Problem." 20 70
     fi
  fi
  do_main_menu
}

#------------------------------------------------------------------------------
function do_nano_main ()
{
  cp $pyconfigfile $filename_conf
  nano $filename_conf
  if (whiptail --title "Save Nano Edits" --yesno "Save nano changes to $filename_conf\n or cancel all changes" 8 65 --yes-button "Save" --no-button "Cancel" ) then
    cp $filename_conf $pyconfigfile
  fi
}

#------------------------------------------------------------------------------
function do_settings_menu ()
{
  SET_SEL=$( whiptail --title "Settings Menu" --menu "Arrow/Enter Selects or Tab Key" 0 0 0 --ok-button Select --cancel-button Back \
  "a EDIT" "nano Edit settings.py" \
  "b VIEW" "settings.py" \
  "d BACK" "Return to Main Menu" 3>&1 1>&2 2>&3 )

  RET=$?
  if [ $RET -eq 1 ]; then
    clear
    rm -f $filename_temp
    rm -f $filename_conf
    do_main_menu
  elif [ $RET -eq 0 ]; then
    case "$SET_SEL" in
      a\ *) do_nano_main
            do_settings_menu ;;
      b\ *) more -d settings.py
            do_anykey
            do_settings_menu ;;
      d\ *) clear
            rm -f $filename_temp
            rm -f $filename_conf
            do_main_menu ;;
      *) whiptail --msgbox "Programmer error: unrecognised option" 20 60 1 ;;
    esac || whiptail --msgbox "There was an error running selection $SELECTION" 20 60 1
  fi

}

#------------------------------------------------------------------------------
function do_upgrade ()
{
  if (whiptail --title "GitHub Upgrade webserver" --yesno "Upgrade webserver files from GitHub" 8 65 --yes-button "upgrade" --no-button "Cancel" ) then
    curl -L https://raw.github.com/pageauc/picamera-motion/master/install.sh | bash
    do_anykey
  fi
}

#------------------------------------------------------------------------------
function do_about ()
{
  whiptail --title "About" --msgbox " \

    Manage picamera-motion operation and settings

          written by Claude Pageau

           for more information

    View Readme.md (use menubox.sh help option)
    or
    visit web repo at https://github.com/pageauc/picamera-motion
    Raise a github issue for issues or questions

\
" 0 0 0
}

#------------------------------------------------------------------------------
function do_main_menu ()
{
  init_status
  SELECTION=$(whiptail --title "Main Menu" --menu "Arrow/Enter Selects or Tab Key" 0 0 0 --cancel-button Quit --ok-button Select \
  "a $PICAM_1" "$PICAM_2" \
  "b $WEB_1" "$WEB_2" \
  "c SETTINGS" "Edit/View Settings" \
  "d UPGRADE" "Upgrade Files from GitHub.com" \
  "e HELP" "View Readme.md" \
  "f ABOUT" "Information about this program" \
  "q QUIT" "Exit menubox.sh"  3>&1 1>&2 2>&3)

  RET=$?
  if [ $RET -eq 1 ]; then
    exit 0
  elif [ $RET -eq 0 ]; then
    case "$SELECTION" in
      a\ *) do_picamera_motion ;;
      b\ *) do_webserver ;;
      c\ *) do_settings_menu ;;
      d\ *) do_upgrade ;;
      e\ *) more -d Readme.md
            do_anykey ;;
      f\ *) do_about ;;
      q\ *) clear
            exit 0 ;;
         *) whiptail --msgbox "Programmer error: unrecognized option" 20 60 1 ;;
    esac || whiptail --msgbox "There was an error running selection $SELECTION" 20 60 1
  fi
}

#------------------------------------------------------------------------------
#                                Main Script
#------------------------------------------------------------------------------
if [ $# -eq 0 ] ; then
  while true; do
     do_main_menu
  done
fi