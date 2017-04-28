#!/bin/bash

 add-apt-repository ppa:kivy-team/kivy
 apt-get update
 apt-get install python3-kivy

apt-get install -y \
python3-pip \
build-essential \
python3 \
python3-dev \
ffmpeg \
libsdl2-dev \
libsdl2-image-dev \
libsdl2-mixer-dev \
libsdl2-ttf-dev \
libportmidi-dev \
libswscale-dev \
libavformat-dev \
libavcodec-dev \
zlib1g-dev

apt-get upgrade

./setup.py install
