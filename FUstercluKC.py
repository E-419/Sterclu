#!/usr/local/bin/python34
# ## Notepad++ Run Path:
# ##   C:\Python34\python34.exe -i "$(FULL_CURRENT_PATH)"
# ##
# ## Build Commands: (run PowerShell as Admin, highlight-copy/right-click-to-paste)
# ##   cd "C:\Users\chadc\Dropbox\projects\FusterKluck"
# ##   python34 AppFreeze_exe.py py2exe



##########################
#### LAUNCHER SCRIPT #####
##########################


# These imports are in order, don't change them around.
import os
os.chdir(os.getcwd())

import src.Model as model
import src.View as view
import src.Controller as controller



## ****** CHANGE LOG ****** ##
#
#yyyy-mm-dd:
#   Description of stuff done to this file
#
#
#
#2017-06-05:
#	Obviously a well maintained documentation...



## ***** APPLICATION ENTRY ***** ## 

if __name__ == '__main__':
	root = view.tk.Tk()
	

	

	# Create objects
	mainView = view.ProjectViewer(root)

	status = view.StatusBar(root)
	
	# Grid objects
	mainView.grid(sticky=view.tkSticky.fill)
	status.grid(sticky=view.tkSticky.horizontal + view.tkSticky.bottom)
	
	# Root window defaults
	# -> To Do: make these values read from a file that saved from the last session
	root.grid_propagate(0)
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	root.configure(width=800, height=600)
	
	'''
	Add an app icon
	Taken from:
	http://stackoverflow.com/questions/16081201/setting-application-icon-in-my-python-tk-base-application-on-ubuntu

	This works on Windows and Ubuntu only
	'''
	
	img = view.tk.PhotoImage('photo', file=os.path.join(os.getcwd(),'res', 'icon_appicon.gif'))
	root.tk.call('wm','iconphoto',root._w,img)
	
	
	# Create Controllers with info from appdata
	
	
	
	
	
	
	
	
	# The following three commands are needed so the window pops
	# up on top on Windows...
	root.iconify()
	root.update()
	root.deiconify()
	
	# Enter the Tkinter run-loop	
	root.mainloop()
	
















#	# Standard application run code:
#	appView = MainApplication()
#	path = None
#	rootCDS = ESM.rootCDS
#	
#	# Development junk, this needs to be replaced with a filepath that's stored in a local directory (WRT the .exe file)
#	if atHome:
#		rootPath = ESM.domainPath_home			 
#	if atWork:
#		rootPath = ESM.domainPath
#	
#	# Set the path to the root .cds file to load
#	path = os.path.join(rootPath, rootCDS)
#	
#	# Create a root cds() object to run the program
#    #    -> this needs to be redone at some point.
#	cdsMain = cds(path, isRoot = True)
#	
#	# Create the UI object and set the delegates for the views
#	appView.setDelegate(	JobBrowser = JobBrowserDelegate(cdsMain, appView.JobBrowser), 
#							FileBrowser = FileBrowserDelegate('', appView.FileBrowser) )
#	
#	# This will force-refresh the JobBrowser upon the 
#	# Button.Click event in the DataDisplay placeholder:
#	#f = appView.FileBrowserDelegate.clearView
#	def dataDisplayHandler():
#		appView.FileBrowserDelegate.clearView()
#	
#	# this doesn't work most likely due to the not registering the function first
#	appView.DataDisplay.config(command=dataDisplayHandler)
#	
#	# Enter the Tkinter run-loop
#	appView.mainloop()
