import os, sys, pathlib

# This import sequence requires the other modules to be in the same /src directory
# if __name__ == '__main__':
# 	from Columbus import Columbus
# 	from JBNode import JBNode
# else:
if 'src' in os.getcwd():
	from Columbus import Columbus
	from JBNode import JBNode
	from FBNode import FBNode
else:
	from src.Columbus import Columbus
	from src.JBNode import JBNode
	from src.FBNode import FBNode

	###############################
	### ***** NEEDS REWORK **** ###
	###############################
	
					
	###############################
	### ***** END - REWORK **** ###
	###############################
	

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# cds Class:
#   Primary use is to read and parse .cds files
#
#	Secondary usage (not coded yet) is to convert and write 
#	the 
#
# Usage:
#   Call CDS.build() with a file-path to the .cds file
#		-> returns the head node to the linked list structure
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class CDS():
	'''
	This class is purely for creating the JBNode linked list that 
	will populate the JobBrowser of Columbus. As such, it's return
	will be the head of the linked list.
	
	This class will also maintain a dict() of CDS files that have
	been loaded, hashable by absFilePath.
	
	As such, this class should not be instantiated directly. It's purely
	a container for the methods and data associated with CDS parsing.
	
	Public Methods:
		.build(filePath)						# Primary use
		.store(folderPath, Node(), fileName) 	# Secondary use, Not written yet
	
	'''
	count = 0
	iids = dict()
	
	def build(cdsPath = None):
		'''
		Pre:	cdsPath is passed in as an absFilePath (one path, not a list)
		
		Post:	A JBNode is returned that is the root Node
				of the .cds file that was parsed.

		Deflt:	Uses the filepath specified in the .\appdata\Root.txt file.
		'''
		if not cdsPath:
			cdsPath = CDS.get_root_cds_location()
			# return None
		
		rootNode = None
		floatNode = None
		label = value = None
		indentLevel = 0
		oldIndentLevel = indentLevel
		
		lines = CDS.readfiles(cdsPath)
		
		for line, cdskey in lines:
			
			# Parse line
			label, value, indentLevel = CDS.parse(line)
			
			# Process tags and skip comments:
			if indentLevel == -1:
				'''
				Do Tag processing {CMC Future Dev}
				'''
				continue # or pass, {CMC Future Dev}
			
			elif label == None:
				continue
			
			# Create a new node:
			node = JBNode(label, value, cdskey)

			# Set root node:
			if rootNode == None:
				rootNode = node
				floatNode = rootNode
				continue		
			
			# Place node in the linked list:
				# As a child to the last node created:
			if indentLevel > oldIndentLevel:
				node.move(under=floatNode)
				oldIndentLevel = indentLevel
				floatNode = node	
				continue
			
				# After last node created:
			if indentLevel == oldIndentLevel:
				node.move(after=floatNode)
				floatNode = node
				continue
			
				# After some parent:
			while indentLevel < oldIndentLevel:
				oldIndentLevel -= 1
				floatNode = floatNode.get(Node.parent)
			node.move(after=floatNode)
			floatNode = node
			continue
		return rootNode


	def appendIid(filepath):
		# Keep a dict() of iids in the class
		if filepath in CDS.iids.values():
			for key, value in CDS.iids.items():
				if filepath == value:
					return key
		else:
			CDS.iids[CDS.count] = filepath
			iid = CDS.count
			CDS.count += 1
			return iid
	
	def readfiles(filenames):
		'''
		While it's awesome and cool to read a list of files in,
		for the purpose of this app only one .cds should be read
		at a time.
		
		If this is to be used elsewhere then it should be moved 
		to a different class and returned here (since it's just 
		returning a generator object).
		'''
		if type(filenames) == list:
			pass
		else:
			filenames = [filenames]
		for f in filenames:
			cdskey = CDS.appendIid(f)
			with open(f, 'r') as fil:
				for line in fil:
					yield line, cdskey
				

			
	def parse(line = None):
		'''
		if CDS.ext in line:
		
		Before:	 str(NumberOfLeadingTabs*'\t') + str(nodeLabel) + ' = ' + str(nodeValue)
		After:	(str, 			str, 		int) 
				 nodeLabel, 	nodeValue, 	NumberOfLeadingTabs
		'''	
		label = value = None
		indentLevel = 0
		
		# Test if line is blank, a tag of my own invention, or just a plain old comment (in that order):
		if line.isspace() or len(line) == 0:
			return label, value, indentLevel
		
		elif Columbus.tag in line:
			'''
			Do Tag processing and return an appropriate tuple for additional processing => (None, tagValue, -1)
			'''
			indentLevel = -1
			value = line.split(Columbus.tag)[-1].strip()
			return label, value, indentLevel
		
		elif Columbus.comment in line:
			return label, value, indentLevel
		
		# Parsing awesomeness happens here...
		# 'indentLevel' is the number of leading '\t' characters in the cds linefeed.
		
		# Set indent level, break on 1st non-white space character
		for char in line:
			if ord(char) > 32:
				break
			elif char == '\t':
				indentLevel += 1
			elif char == ' ':
				continue
			elif char == '\n':
				continue
		
		# Replace '\n' with '' and '\t' with ' '
		ln = line
		ln.replace('\t', ' ')
		ln.replace('\n', '')

		# 'label' is all characters after leading whitespace and before the '=' in the cds linefeed.
		ln = ln.split(Columbus.valueDeliminator)
		label = ln[0].strip()
		
		# 'value' includes everything after the '=' in the cds linefeed.
		if len(ln) > 1:
			value = ln[-1].lower().strip()

		return label, value, indentLevel	

	def get_root_cds_location():
		curdir = pathlib.Path(os.getcwd())
		
		root_loc = curdir.parent / 'appdata' / 'Root.txt'
		with root_loc.open() as fil:
			root = fil.readline()
		root = root.strip().split('\\')
		
		return root
		# with open(str(root_loc), 'r') as fil:
		# 	return fil[0]




	
				
################################
### ***** Unit - Tests ***** ###
################################


if __name__ == "__main__":
	from Node import *
	
	# # something is FUBAR in the build() method, the node.flatten() output list is all screwed up
	# # -> all better now =)


	# Read data in from the user's default values:
	RootCDS		= pathlib.Path( *CDS.get_root_cds_location() )
	
	# Iterate through a directory:
	for i in RootCDS.parent.iterdir(): 
		print(i)
	
		
	cdsPath1 	= RootCDS
	cdsPath2	= RootCDS.parent / 'Infrasource.cds'


	node  = CDS.build() # -> JBNode() as head of tree
	node2 = CDS.build( str(cdsPath2) )
	
	# node3 = CDS.build(cdsPath3)
	


	# Find the node that the second CDS should be inserted under and do the nasty:
	match = node.search('infrasource.cds', Node.value)[0]
	node2.move(under=match, allNodes=True)

	
	def search(text, node):
		matches = node.search(text, Node.label)
		for match in matches:
			print(match.get(Node.label))
		print()


	
	search('122', node)

	# print(len(node.flatten()))
	
	
#	for nd in node3.flatten():
#		print(nd.refs[Node.label], '\n\t', nd.refs[Node.value])
	nd = node2
	while nd.refs[Node.after] != None:
		print(nd.refs[Node.label])
		if nd.refs['child']:
			for child in nd.children():
				print('\t', child.refs['label'])
		nd = nd.refs['after']
	#
	#print('Printing ls.flatten():')
	#
	#for ln in ls:
	#	print(ln)
	#
	#print()
	#print(len(ls))
	#print('\n'* 10)
	#
	#def printAfter(node):
	#	print('Nodes in this level:')
	#	while node != None:
	#		print(node)
	#		node = node.get(Node.after)
	#
	#printAfter(node)
	#
	#print(r'Holland Construction'.split('\t'))
	#print(r'	1001 Minor   = <INCLUDE \\Esm8\engr\ESM-JOBS\1699\004\014\Project.cds>'.split('\t'))
	#print(r"	970 Denny Way; Ducky's Site = <INCLUDE \\Esm8\engr\ESM-JOBS\1699\003\014\Project.cds>".split('\t'))
	#print(CDS.parse(r'Holland Construction'))
	#print(CDS.parse(r'	1001 Minor   = <INCLUDE \\Esm8\engr\ESM-JOBS\1699\004\014\Project.cds>'))
	#print(CDS.parse(r"	970 Denny Way; Ducky's Site = <INCLUDE \\Esm8\engr\ESM-JOBS\1699\003\014\Project.cds>"))
	#
	#print(3*'\n')
	#print(CDS.parse(r'Holmaas,John'))
	#print(CDS.parse(r'	Creviston Drive	= <INCLUDE \\esm8\engr\ESM-JOBS\872\004\002\Project.cds>'))
	#print(CDS.parse(r'	Cushman Trail = <INCLUDE \\esm8\engr\ESM-JOBS\872\005\003\Project.cds>'))
	#print(CDS.parse(r'	Key Center 5 = <INCLUDE \\esm8\engr\esm-jobs\872\008\012\Project.cds>'))
	#
	#print(r'	Creviston Drive	= <INCLUDE \\esm8\engr\ESM-JOBS\872\004\002\Project.cds>')
	#
	#r'''
	#
	#Holmaas,John
	#	Creviston Drive	= <INCLUDE \\esm8\engr\ESM-JOBS\872\004\002\Project.cds>
	#	Cushman Trail = <INCLUDE \\esm8\engr\ESM-JOBS\872\005\003\Project.cds>
	#	Key Center 5 = <INCLUDE \\esm8\engr\esm-jobs\872\008\012\Project.cds>
	#InfraSource = <INCLUDE Infrasource.cds>
	#'''
	#
	#print(10*'\n')
	#print(r'American Classic Homes'.split('\t'))
	#print(r' 	Murray Property = <INCLUDE \\esm8\engr\ESM-JOBS\1352\021\015\Project.cds>'.split('\t'))
	#print(r'	Redmond 10 = <INCLUDE \\Esm8\engr\ESM-JOBS\1352\022\016\Project.cds>'.split('\t'))
	#
	#print(CDS.parse(r'American Classic Homes'))
	#print(CDS.parse(r' 	Murray Property = <INCLUDE \\esm8\engr\ESM-JOBS\1352\021\015\Project.cds>'))
	#print(CDS.parse(r'	Redmond 10 = <INCLUDE \\Esm8\engr\ESM-JOBS\1352\022\016\Project.cds>'))
	#
	#
	#print(len(''.strip()))

	#for i in range(0,255):
	#	print(i, '=>\t', chr(i))

	'''
	def printAfter(node):
		print('Nodes in this level:')
		while node != None:
			print(node)
			node = node.get(Node.after)

	node = node.get(Node.after)

	printAfter(node)
	print()
	for child in node.children():
		print()
		print(child)
		printAfter(child.get(Node.child))
	'''



	'''
	This is where I need to hard code a structure check for the Test.cds
	-> list all nodes in order of connection:
		child
		next
		parent.next
		
	=> Result:
		Controller2.py is correct, Model2.Node.flatten() is wrong
		
	'''


	#print('\n'* 10)
	#
	#for ln in ls:
	#	print(ln)

	#print('\n'* 10)
	#
	#n = node.children()
	#print(node)
	#for child in n:
	#	print(child)
		




	#for line in lines:
	##	print(line[0], ' -> came from:', CDS.iids[line[1]])
	#	print(line[0], line[1])
	#
		
	#for line in cdslines:
	#	print(line[0])
		
		
		


