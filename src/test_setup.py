'''
Run tests on the entire system from here, or specify particular subtests to run.
Reprot results to stdout.
'''

import unittest as ut
import subprocess as sp
import os

# When running tests, make sure we have test files

class TestEnviron(ut.TestCase):
    def test_downloads(self):
        cwd   = os.getcwd()
        media = os.path.join(cwd, '..', 'media')
        dl    = os.path.join(media, 'download.sh')

        sp.run('cd {} && {} -s'.format(media, dl), shell=True)
        print('Downloading sample inputs')
        sampler = os.path.join(media, 'sampler.mp3')
        # TODO: assert that file '../media/sampler.mp3' exists



