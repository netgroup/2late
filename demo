#!/bin/bash

LOOP_REC_TIME=120
RE_ENC_TIME=5

CURR_DATE=$(date +"%Y-%m-%d-%H:%M")
CURR_FOLDER=$(date +"%Y-%m-%d-%H_"$(( $(date +"%M") / $RE_ENC_TIME )))

mkdir -p /home/pi/webcam/imgs
find /home/pi/webcam/imgs -type d -mindepth 1 -mmin +$LOOP_REC_TIME -exec rm -rf {} \;

if [ $(( $(date +"%M") % $RE_ENC_TIME )) -eq 0 ]
then
	# ENCRYPTION PROCEDURE
	python3 $1 /home/pi/webcam/imgs
	mkdir -p /home/pi/webcam/imgs/$CURR_FOLDER
fi

EXTENSION=".png"
IMG_FILE_NAME=$CURR_DATE$EXTENSION

mkdir -p /home/pi/webcam/imgs/$CURR_FOLDER
fswebcam /home/pi/webcam/imgs/$CURR_FOLDER/$IMG_FILE_NAME
