#!/usr/local/bin/python3
#   C:\Python34\python34.exe -i "$(FULL_CURRENT_PATH)"
from distutils.compressed import setup
import sys, os

try:
	import py2exe
except:
	import pip
	pip.main(['install', 'py2exe'])
	import py2exe


path = os.path.join(os.getcwd(), 'FUstercluCK', 'FUstercluCK.py')

setup(
    options = {'py2exe': {'bundle_files': 2, 'compressed': True}},
    windows = [{'script': path}],
    zipfile = None,
)
