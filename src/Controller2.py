import os, sys, pathlib

from src.View2 import *
from src.Model3 import *



##  ******** CONTROLLER ********  ##

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Delegate Classes:
#   Handle all interactions between the Model and View objects
#       -> Method calls should be done with an explicite 
#          "controller" object
#
# Usage:
#   To be determined...
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class NotebookController():
	def __init__(self, model = None, view = None):
		pass

class TreeviewController():
	def __init__(self, model = None, view = None):
		pass
	
	def loadView(self):
		pass
			
	def loadTempView(self, nodeList):
		pass
	
	def search(self, searchValue = None, searchRef = None):
		self.view.detach_all()
		matches = self.model.search(searchValue, searchRef)
		self.loadTempView(matches)

class ProjectViewerController():
	pass
	



#
## Current Working Directory:
#os.path.abspath( os.path.curdir )
#
## Who am I?
#print(os.path.abspath(os.path.curdir).split('\\')[-1])
#


	
## ****** CODE SNIPPETS ****** ##
#Open in Explorer:
#   # Taken from http://stackoverflow.com/questions/281888/open-explorer-on-a-file
#   
#   import subprocess
#   # Folders:
#   subprocess.Popen(r'explorer /open, "C:\Users\chadc\Desktop"')
#   
#   # Opens files with the system default application:
#   subprocess.Popen(r'explorer /open, "C:\Users\chadc\Desktop\test.text"')
#   
#   # Selects the item in the parent folder (local only):
#   subprocess.Popen(r'explorer /select, "C:\Users\chadc\Desktop\test.text"')
#   subprocess.Popen(r'explorer /select, "C:\Users\chadc\Desktop"')
#
#   # Retrieving file names from the server:
#   for item in os.listdir( os.path.join('\\\\Esm8\\ENGR\\')):
#	   print(item)
#
#
#   # Opening a file from the server:
#   http://stackoverflow.com/questions/434597/open-document-with-default-application-in-python
#   import pathlib
#   p = pathlib.Path(r'\\esm8\engr\esm-jobs\1905\001\016\Office\Letter-019.pdf')
#   os.startfile(os.path.join('\\\\esm8\\engr\\esm-jobs\\1905\\001\\016\\Office\\Letter-019.pdf'))
#
#   # or (if there are no escape characters... better to just break on "\" and replace with "\\")
#   os.startfile(os.path.join( r'\\esm8\engr\esm-jobs\1905\001\016\document\Rprt-001.docx' ))
#
#   # File filter usage:
#   p = pathlib.Path(r'\\esm8\engr\esm-jobs\1905\001\016\Office\')
#   listOfFilesFromFilter = sorted(p.glob('*.pdf'))
#   FileBrowserDelegate.updateView(listOfFilesFromFilter)


