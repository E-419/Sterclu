import os, pathlib, sys

### ****** DATA CLASSES ****** ##
## Helper classes that contain general/hard-coded application options:

def docinfo(somepath):
	# Usage:
	#	di docinfo(someDirectoryPathObject)
	#	if di.exists():
	#		do_stuff()
	return pathlib.Path(str(somepath), 'docinfo')
	


class Columbus():
	def __init__(self):
		pass
	
	#	/Users/Admin/.. || /Users/godswillbedone/..
	rootCDSPath_Mac		= os.path.join('/Users/Admin/Dropbox/ESM/Project Management Logistics/Columbus Database Source/DomainSettings/Current projects.cds')
	rootCDSPath_Work	= os.path.join('//Esm8/ENGR/Program Files/Oasys/DomainSettings/Current projects.cds')
	
	valueDeliminator	= '='
	comment				= '//'
	dirSeparator		= '\\'
	labelTag			= '#'
	tag					= '//-> '
	filterChar			= '*'
	cdsExt				= '.cds'
	dinExt				= '.din'
	hisExt				= '.his'
	include				= '<INCLUDE'.lower()


	###############################
	### ***** NEEDS REWORK **** ###
	###############################
	
					
	###############################
	### ***** END - REWORK **** ###
	###############################

'''
This ESM() class needs to be converted to an appdata file of some sort.
This is the hard-coded version of application settings that should be changed 
depending on the end user.
'''
#class ESM():
#	def __init__(self):
#		pass
#	#rootPath   		= '//Esm8/ENGR/Program Files/Oasys/DomainSettings'
#	domainPath_home		= os.path.join( atHomePath + '/ESM/Project Management Logistics/Columbus Database Source/DomainSettings')
#	#domainPath_home 	= os.path.join( atHomePath + '\\ESM/Project Management Logistics\\Columbus Database Source\\DomainSettings')
#	esm8				= '\\\\esm8'
#	esm4				= '\\\\esm4'
#	engr				= 'engr'
#	
#	root				= os.path.join(esm8, engr)
#	jobs				= 'ESM-JOBS'.lower()
#	wordProc			= 'WORD-PROC'.lower()
#	domainSettings		= 'DomainSettings'
#	oasys				= 'Oasys'
#	programFiles		= 'Program Files'
#	domainSettingsPath	= os.path.join(esm8, engr, programFiles, oasys, domainSettings)
#	mDrive				= os.path.join(esm8, wordProc)
#	rootCDS				= 'Current projects.cds'
#	domainPath			= os.path.join('//Esm8/engr/Program Files/Oasys/DomainSettings/')
#	
#	if atWork:
#		domainPath  = os.path.join('//Esm8/engr/Program Files/Oasys/DomainSettings/')
#		domainPath  = os.path.join(root, domainSettingsPath)
#	else:
#		domainPath  = domainPath_home
#


