#!/usr/bin/env python3

try:
    from setuptools import setup
except:
    print("[!] Warning: unable to import setuptools.setup. Attempting to continue with distutils.core.setup")
    from distutils.core import setup


setup( name         = 'musicvisualizer'
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
