# MusicVisualizer (or MV)

## What is MV?
MusicVisualizer is a project written in Python that visualizes mp3s and outputs
mp4 videos.  This is currently in alpha development but is showing promise,
executing it's main goal of visualizing music.

## Installing
Currently our install script ain't perfect. First, make sure you have `pip3`
installed with

    sudo apt-get install python3-pip    # Get pip3
    sudo pip3 install --upgrade pip     # Get the latest version of pip
    sudo apt-get install ffmpeg         # Does stuff with mpegs
    sudo pip3 install numpy             # Numpy has to be installed seperately
    sudo setup.py install               # Run the install script

You should be good (hopefully). However, if for whatever reason this _doesn't_
work (and you don't feel like fiddling) you can run this on a 
[sanitized install of Lubuntu](http://benkushigian.com/musicvisualizer/virtualbox-snapshots/mvp-installer.tar.gz)
through Virtual Box.

## Running
There are two ways to run MV; the first is through a command line interface, and
this gives you the maximal flexibility. The second is through the GUI and this
gives restricted access.

### Running From Command Line
Assuming that we installed everything correctly, we can run `visualize
input.mp3` and after some crunching an `output.mp4` will appear in the directory
that you called `visualize` from. Additonally you can pass an output argument
`-o path/to/destination/file.mp4` to specify where you would like the output to
end up. For more information run `visualize --help`.

### Running from GUI

