import os, sys, pathlib
# if __name__ == '__main__':
# 	from Node import *
# else:
if 'src' in os.getcwd():
	from Node import Node
else:
	from src.Node import Node

class FBNode(Node):
	'''
	This class should be a capsule for all the data that can be extracted from the
	.din and .his files, in addition to the file's metadata.

	The head of the list should keep a reference to the JBNode that it belongs to
		-> Likewise the JBNode counterpart should keep a ref to the head of the  
		   list of FBNodes that it needs to display (upon focus).
	
	
	'''
	pass