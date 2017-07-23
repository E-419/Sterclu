import os
# This import sequence requires the other modules to be in the same /src directory
# if __name__ == '__main__':
# 	from CommonView import *
# 	from CustomView import *
	
# else:
if 'src' in os.getcwd():
	from tkExt import *
	# from SearchView import *
	# from ProjectViewer import *

else:
	from src.tkExt import *
	# from src.SearchView import *
	from src.ProjectViewer import *
