import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
# if __name__ == '__main__':
# 	from CommonView import *
# 	from CustomView import *
	
# else:
if 'src' in os.getcwd():
	from CommonView import *
	from CustomView import *

else:
	from src.CommonView import *
	from src.CustomView import *
