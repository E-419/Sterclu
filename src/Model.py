import os
if 'src' in os.getcwd():
	from Node import *
	from CDS import *
	from Columbus import *
	from JBNode import *
else:
	from src.Node import *
	from src.CDS import *
	from src.Columbus import *
	from src.JBNode import *

if __name__ == '__main__':
	from JBNode import JBNode as Node

	# Create Nodes:
	n1 = Node('test label 1', 'esm8\\engr\\esm-jobs\\1234\\001\\016\\Project.cds')
	n2 = Node('test label 2', 'esm8\\engr\\esm-jobs\\1235\\567\\013\\Project.cds')
	n3 = Node('child node 3', 'esm8\\engr\\esm-jobs\\1234\\002\\016\\Project.cds')
	n4 = Node('Bonaventure', 'esm8\\engr\\esm-jobs\\1236\\001\\016\\Project.cds')
	n5 = Node('test label 5', 'esm8\\engr\\esm-jobs\\1234\\003\\017\\Project.cds')
	n6 = Node('511 Minor Ave S', 'esm8\\engr\\esm-jobs\\1234\\004\\014\\Project.cds')
	n7 = Node('1532 NE 32nd St', 'esm8\\engr\\esm-jobs\\1234\\005\\016\\Project.cds')
	
	# Arrarge Nodes using the .move() method (which handles the surrounding node connections internally):
	#	build using Node.after and Node.child, the other relations are taken care of by the Node class
	n2.move(after=n1)
	n3.move(under=n1)
	n4.move(after=n2)
	n5.move(before=n3) # This call should be avoided in the initial loading under normal circumstances
	n6.move(under=n3)
	n7.move(after=n6)
	
	# Set additional properties (this should be part of the CDS.py script to extract the data):
	n1.set('clientID', '1707')
	n3.set('clientID', '1707')
	n1.set('yearID', '016')
	n4.set(Node.yearID, '016') # this is a JBNode property
	n4.set(Node.clientID, '1234')
	n5.set(Node.clientID, '1707')
	n6.set(Node.clientID, '1707')
	n7.set(Node.clientID, '1707')