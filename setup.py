#!/usr/bin/env python3

from distutils.core import setup

setup( name         = 'musicvisualizer'
     , version      = '1.0'
     , description  = 'Visualizer for mp3s'
     , author       = 'Fedore Arkhipov, Ben Guinsburg, Ben Kushigian, Thomas Peck, Sam Remis, Ivan Siryk'
     , author_email = 'bkushigian@gmail.com'
     , packages     = ['pipeline', 'ui', 'test']
     , package_dir =  { 'pipeline' : 'src/pipeline'
                      , 'ui'       : 'src/ui'
                      , 'test'     : 'src/test'
                      }
     )
