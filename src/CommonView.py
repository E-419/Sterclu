import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
if __name__ == '__main__':
	from tkBase import *
else:
	if 'src' in os.getcwd():
		from tkBase import *
	else:
		from src.tkBase import *
