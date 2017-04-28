#!/bin/bash

# setup.sh: install MusicVisualizer on this system (assuming that it is
# Ubuntu/Debian and uses the apt package manager). Currently this has been
# tested on Lubuntu 16.04.

add-apt-repository ppa:kivy-team/kivy
apt-get update
apt-get install python3-kivy

# Install dependencies

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


pip3 install --upgrade pip  # Upgrade pip
pip3 install numpy          # Get numpy
./setup.py install          # Run the setup script
