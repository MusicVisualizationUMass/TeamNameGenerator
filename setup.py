#!/usr/bin/env python3

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
     , install_requires = [ 'aubio',
                            'pydub',
                            'moviepy',
                            'numpy'
                           ]
     )
