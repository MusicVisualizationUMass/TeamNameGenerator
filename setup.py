#!/usr/bin/env python3

try:
    from setuptools import setup
    from setuptools.command.build_ext import build_ext as _build_ext
except:
    print(
'''
[!] Warning: unable to import setuptools.setup. Please visit your package
manager and install pip3 (or setuptools for python3, thought this hasn't been
tested. On Debian-based Linux distros it will be

    $ sudo apt-get install python3-pip

and on Mac OS run

    $ brew install pip3       # Double check this - I'm just guessing :)

As always, good luck and happy visualizing!
'''
)

# XXX: This is from a stack exchange post and should be inspected at some point
# when someone has time/gumption. For more info, checkout:
# http://stackoverflow.com/questions/19919905/how-to-bootstrap-numpy-installation-in-setup-py

class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is sill in its setup process
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


setup( name         = 'musicvisualizer'
     , cmdclass     = {'build_ext':build_ext}
     , version      = '1.0'
     , description  = 'Visualizer for mp3s'
     , author       = 'Fedore Arkhipov, Ben Guinsburg, Ben Kushigian, Thomas Peck, Sam Remis, Ivan Siryk'
     , author_email = 'bkushigian@gmail.com'
     , url          = 'https://github.com/MusicVisualizationUMass/TeamNameGenerator'
     , packages     = [ 'musicvisualizer', 'pipeline', 'ui']
     , package_dir =  { 'musicvisualizer' : 'src/musicvisualizer',
                        'pipeline'        : 'src/musicvisualizer/pipeline'
                      , 'ui'              : 'src/musicvisualizer/ui'
                      }
     , install_requires = [ 'numpy',
                            'aubio',
                            'moviepy',
                            'pydub'
                           ]
     )
