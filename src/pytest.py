'''
Run tests on the entire system from here, or specify particular subtests to run.
Reprot results to stdout.
'''

import unittest as ut
import subprocess as sp
import os

# When running tests, make sure we have test files
cwd   = os.getcwd()
media = os.path.join(cwd, '..', 'media')
dl    = os.path.join(media, 'download.sh')

sp.run('cd {} && {} -s'.format(media, dl), shell=True)

# XXX: assume we have test file name ../media/sampler.mp3. This should be
# verified

sampler = os.join(media, 'sampler.mp3')


