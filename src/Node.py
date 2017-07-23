import os, sys, pathlib

# Musings...
#	This whole class needs to be refactored into a pair: Node and TreeList
#		The Node is a data container and the TreeList is a means of managing
#		the data containers (and their subclasses).
#
#	Maybe even contained in an un-gridded tk.Treeview() with a clever controller
#	to do the heavy lifting of sorting and searching.
#
# 

class Node():
	'''
	Description:
		This is an Abstract Data Type for a dual-direction, doubly linked list
		(a.k.a. the data type that feeds a tree_view object)
		
	Factory Methods:
		init(label, value, after=Node.ref , before= , under= )
	
	Method Prototypes:
			
		move(after=Node.ref , before= , under= )
		flatten()
		tree() # generator that returns the next Node() in the list 
		_pluck()
		_insert(after=Node.ref , before= , under= )
		search(textValue, Node.ref, [options])
		
		-> 	The following are generic accessor methods because  
			the iVars are stored in a dict (i.e. self.refs) and
			the key string is passing into the method.
		remove(Node.ref)
		set(Node.ref, value)
		get(Node.ref)
		
		children()
		lastChild()
		
		destroy()
		
		
	'''
	# Static Ref index list is dynamically enumerated
	#	-> 	that allows for subclasses to extend ref
	#		implementation in a similar fashion to this
	#		class using psuedo templates. 
	#	Subclasses must append the ref list to the list
	#	allocated in this class. 
	#
	#	Use extreme caution: this is a totally unorthodox
	#	workaround in Python to create generic methods.
	#
	# ***** UPDATE *****
	# self.refs is now a dict() object and behaves much better 
	# in general.
	#
	
	after 	= 'after' 	# next
	before 	= 'before' 	# prev
	parent 	= 'parent'
	child 	= 'child'
	label 	= 'label'
	value 	= 'value'
	iid		= 'iid'
	_temp	= '_temp'

	# For Tkinter:
	iids = dict() # empty dictionary for iids
	
	def refInv(ref):
		if ref == Node.after:
			return Node.before
		elif ref == Node.before:
			return Node.after
		elif ref == Node.parent:
			return Node.child
		elif ref == Node.child:
			return Node.parent
		else:
			raise Exception('Node.ref "' + str(ref) + '" not invertable')
	
	def init(label, value, after = None, before = None, under = None):
		node = Node(label, value)
		if after:
			node._insert(after=after)
		elif before:
			node._insert(before=before)
		elif under:
			node._insert(under=under)
		return node
	
	def __init__(self, label, value):
		# These are the iVars available to all subclasses:
		self.label 		= label # To be displayed by the View
		self.value 		= value # To be used by the Controller, absolute filePath or fileFilter
		self.iid		= None	# Value given by the View
			
		# This iVar is just a Python dict() and can be adjusted accordingly:
		self.refs = dict()
		self.refs[Node.after] = None
		self.refs[Node.before] = None
		self.refs[Node.parent] = None
		self.refs[Node.child] = None
		self.refs[Node.label] = label
		self.refs[Node.value] = value
		self.refs[Node._temp] = False
												
	def __lt__(self, other):
		# if type(other) != Node:
		# 	raise Exception('{0} must be a Node() object'.format(str(other)))
		try:
			result = self.refs[Node.iid] < other.refs[Node.idd]
		except:
			result = False
		return result

	def __gt__(self, other):
		try:
			result = self.refs[Node.iid] > other.refs[Node.idd]
		except:
			result = False
		return result

	def copy(NodeIn):
		node = Node(NodeIn.refs[Node.label], NodeIn.refs[Node.value])
		return node
	
	# ***** ************** ***** #
	#		Public Methods		 #
	# ***** ************** ***** #
	#
	# These methods should be the one's used for data type 
	# manipulation.
	#
	def move(self, after = None, before = None, under = None, allNodes = None):
		'''
		Pretty much does the obvious: properly removes self node
		from current location and places it elsewhere in the 
		linked node list.
		'''
		if allNodes == None:
			# Children only
			self._pluck()
			
		if after != None:
			self._insert(after=after)
		elif before != None:
			self._insert(before=before)
		elif under != None:
			self._insert(under=under)
	
	def flatten(self):
		'''
		Pre: 	A linked list of Node() objects with next and child ref's
		
		Post:	A normal Python list() object of the Nodes() after, under,
				and including the head Node() that this method was called
				from.
		
		Use:	Typically used on a Node().refs[Node.child]
		'''
#		floatNode = self
		flatList = []
		
		# Stack, first in - last out, break the loop on None, store only parents:
		nodeStack = [None]
		
		for nd in self.tree():
			node = nd[0]
			flatList.append(node)
		return flatList
				
		# Initiate the walking sequence:
#		flatList.append(floatNode)
		
		
		
		# Walk down the linked list: .child first, .after next, nodeStack.pop() last, break the loop on None:
#		while floatNode != None:
#			if floatNode.get(Node.child) != None:
#				# Append floatNode to nodeStack (to maintain a parentRef)
#				nodeStack.append(floatNode)
#				
#				# Move floatNode ref to child
#				floatNode = floatNode.get(Node.child)
#				
#				# Append floatNode to flatList
#				flatList.append(floatNode)
#				continue
#			
#			elif floatNode.get(Node.after) != None:
#				# Move floatNode ref to after
#				floatNode = floatNode.get(Node.after)
#				
#				# Append floatNode to flatList
#				flatList.append(floatNode)
#				continue
#			
#			else:
#				floatNode = nodeStack.pop()
#				# This second/nested while loop is needed to only check for .after nodes
#				# because floatNode is climbing back up the nodeStack list.
#				while floatNode != None:
#					if floatNode.get(Node.after) == None:
#						floatNode = nodeStack.pop()
#					else:
#						# Move floatNode ref to after
#						floatNode = floatNode.get(Node.after)
#						
#						# Append floatNode to flatList
#						flatList.append(floatNode)
#						break
#		
#		return flatList
	
	def tree(self):
		'''
		Pre: 	A linked list of Node() objects with next and child ref's
		
		Post:	A normal Python generator() object of the Nodes() after, under,
				and including the head Node() that this method was called from.
				
				This gen() yields a list: 
					[nodeOfInterest, referenceNode, relationToRefNode]
				
				Typical usage is...
					for nd in Node().tree():
						node = nd[0]
						ref = nd[1]
						pos = nd[2]
						...
		'''
		floatNode = self
		refNode = floatNode
		root = ''
		
		# Stack, first in - last out, break the loop on None, store only parents:
		nodeStack = [None]
				
		# Initiate the walking sequence:
		yield [floatNode, root, Node.after]
		
		# Walk down the linked list: .child first, .after next, nodeStack.pop() last, break the loop on None:
		while floatNode != None:
			if floatNode.get(Node.child) != None:
				# Append floatNode to nodeStack (to maintain a parentRef)
				nodeStack.append(floatNode)
				
				# Move floatNode ref to child and yield
				refNode = floatNode
				floatNode = floatNode.get(Node.child)
				yield [floatNode, refNode, Node.child]
				continue
			
			elif floatNode.get(Node.after) != None:
				# Move floatNode ref to after and yield
				refNode = floatNode
				floatNode = floatNode.get(Node.after)
				yield [floatNode, refNode, Node.after]
				continue
			
			else:
				floatNode = nodeStack.pop()
				# This second/nested while loop is needed to only check for .after nodes
				# because floatNode is climbing back up the nodeStack list.
				while floatNode != None:
					if floatNode.get(Node.after) == None:
						floatNode = nodeStack.pop()
					else:
						# Move floatNode ref to after and yield
						refNode = floatNode
						floatNode = floatNode.get(Node.after)
						yield [floatNode, refNode, Node.after]
						break

	
	def search(self, value, nodeRef, exact = None, caseInsensitive = None ):
		'''
		This method returns a list of matches to the search value in the nodeRef 
			-> Default search is case-insensitive, value anywhere in the string
		nodeRef is the iVar to look in for value
		Ex.
			matches = node.search('somePartOfLabelName', Node.label, caseInsensitive=True)
			for match in matches:
				print(match.label)
		'''
		ls = self.flatten()
		matches = []
		try:
			if exact:
				for item in ls:
					itemVal = item.get(nodeRef)
					if itemVal != None and value in itemVal:
						matches.append(item)
			elif caseInsensitive:
				for item in ls:
					itemVal = str(item.get(nodeRef)).lower()
					if itemVal != None and str(value).lower() in itemVal:
						matches.append(item)
			else:
				# Default search: case-insensitive, value anywhere in itemValue
				for item in ls:
					itemVal = str(item.get(nodeRef)).lower()
					if itemVal != None and str(value).lower() in itemVal:
						matches.append(item)
		except:
			return matches			
		return matches
	
	def _pluck(self):
		'''
		This method removes the parent node reference 
		and resets the before/after ref's to the nodes
		before and after this node to each other. Like
		taking off your hat (remove parent) and passing  
		the hands you're holding to each other (reassign  
		before/after) and removing yourself and your 
		backpack (child nodes).

		Update: 
			Need to verify that the ._pluck() works if 
			self is the 1st child of parent.
		Solved:
			That is implemented in the .remove() call
		
		Pre:
				  +--->	  +--->	  Parent
				  |		  |			^
				  V		  V			V
				Next <-> self <-> Prev
						  ^
						  V
				... <-> Child
		
		Post: 	
		
				  +--->	 Parent	
				  |		   ^			
				  V		   V			
				Next <-> Prev	 &&		 self
										  ^
										  V
								... <-> Child
		'''
		self.remove(Node.parent)
		nxt = self.get(Node.after)
		prv = self.get(Node.before)
		if nxt != None:
			nxt.reset(Node.before, prv)
		if prv != None:
			prv.reset(Node.after, nxt)
		
		self.remove(Node.before)
		self.remove(Node.after)
	
	def _insert(self, after = None, before = None, under = None):
		
		someNode = None
		
		# Small Talk Selectors
		if after != None:
			# -> insert self after someNode
			someNode = after
			
			# Connect Parent/Child
			self.set(Node.parent, someNode.get(Node.parent))
			
			# Connect Next/Prev
			nextNode = someNode.get(Node.after)
			if nextNode != None:
				oldNextNode = nextNode
				someNode.remove(Node.after)
				someNode.set(Node.after, self)
				self.set(Node.before, someNode)
			else:
				someNode.set(Node.after, self)
				self.set(Node.before, someNode)
					
			return True
			
		
		elif before != None:
			# -> insert self before someNode
			# 
			# 		This is/may be broken, before=headChild doesn't connect self.refs[Node.after] to headChild
			# 
			someNode = before
			
			
			# This should handle the case where the insert is replacing the head of 
			# a children list... I think it works actually
			
			# Set Parent.Child
			# if someNode is head
			parent = someNode.get(Node.parent)
			if parent.get(Node.child) == someNode:
				# set parent's new childNode
				parent.remove(Node.child)
				parent.set(Node.child, self)
			
			# Set Child.Parent
			self.set(Node.parent, someNode.get(Node.parent))
			
			# Connect Next/Prev
			#1. before head
			#		prevNode == None
			#		nextNode != None
			#2. before middle list node or tail
			#		prevNode != None
			#		nextNode != None or nextNode == None
			
			prevNode = someNode.get(Node.before)
			nextNode = someNode.get(Node.after)
			#1.
			if prevNode == None:
				someNode.set(Node.before, self)
				self.set(Node.after, someNode)
			
			#2.
			elif prevNode != None:
				#1. Remove old ref's
				someNode.remove(Node.before)
				prevNode.remove(Node.after)
				
				#2. Set before ref's
				someNode.set(Node.before, self)
				self.set(Node.before, prevNode)
				
				#3. Set after ref's
				prevNode.set(Node.after, self)
				self.set(Node.after, someNode)
			
			return True
		
		elif under != None:
			# -> insert self as child to someNode at the end of the list 
			someNode = under
			child = someNode.lastChild()
			if child == None:
				someNode.reset(Node.child, self)
			else:
				child.reset(Node.after, self)
			return True
		else:
			return False
		
	# ***** ************** ***** #
	#		Setter Methods		 #
	# ***** ************** ***** #
	# Set the node if self.Node == None; return True; else: return False
	# Pre:  self.Node == unknown
	#
	# Post:	self.Node == node 		-> True
	#		self.Node == unknown 	-> False	
	
	def get(self, toNode):
		return self.refs[toNode]
		
	def set(self, refTo=None, withNode=None):
		'''
		self.refsss is a mutable dict() to allow self.set() to 
		be a template function. It is used for all 4 node
		connections with all associated logic built in one 
		place.
		'''
		# Small Talk Selector Conversion
		toNode = refTo
#		fromNode = Node.refInv(toNode)
		node = withNode
		if self.refs[toNode] == None:
			self.refs[toNode] = node
			# If setting after/next or child, auto-set before/prev or parent on the new node
			if node != None and (toNode == Node.after or toNode == Node.child):
				node.set(Node.refInv(toNode), self)
			return True
		else:
			return False
	
	def reset(self, nodeRef, node = None):
		self.remove(nodeRef)
		self.set(nodeRef, node)
		
	def children(self):
		# Pre:  None
		# Post: Returns a list of childNode references, [] if no children
		ls = []
		if self.refs[Node.child] != None:
			node = self.refs[Node.child]
			while node != None:
				ls.append(node)
				node = node.refs[Node.after]
		return ls				
	
	def lastChild(self):
		chldn = self.children()
		if len(chldn) > 0:
			return chldn[-1]
		else:
			return None
	
	def isParent(self, node):
		try:
			chldn = self.refs[Node.child].flatten()
			return node in chldn
		except:
			return False
			
	def remove(self, refTo=None):
			'''
			Set self.refs[toNode] = None
			'''
			# Small Talk Selector Conversion
			toNode = refTo
			if toNode == Node.parent:
				parent = self.refs[toNode]
				if parent != None:
					child = parent.refs[Node.child]
					if child == self:
						parent.set(Node.child, self.get(Node.after))	
			self.refs[toNode] = None
	
	# ***** *************** ***** #
	#		Display Methods		  #
	# ***** *************** ***** #
	#
	# These methods should be the one's used for data type 
	# manipulation.
	#
	
	def connections(self):
		temp = ('self:\t' + str(self) +
		'\nparent:\t' + str(self.get(Node.parent)) +
		'\nchild:\t' + str(self.get(Node.child)) +
		'\nafter:\t' + str(self.get(Node.after)) + 
		'\nbefore:\t' + str(self.get(Node.before))
		)
		return temp
	
	def displayConnections(self):
		print(self.connections())			
	
	def destroy(self, head = False):
		# Remove all ref's to all other next/child nodes recursively
		nxt = self.get(Node.after)
		children = self.children()
		
		if head:
			child = self.get(Node.child)
			prev = self.get(Node.before)
			parent = self.get(Node.parent)
			if prev != None:
				prev.remove(Node.after)
			if parent != None:
				if parent.get(Node.child) == self:
					parent.remove(Node.child)
			if child != None:
				child.remove(Node.parent)
		
		self._removeAll()
		if len(children) > 0:
			for child in children:
				child.destroy()
		
		if nxt != None:
			nxt.destroy()	
	
	def _removeAll(self):
		# This will remove all ref's to other nodes in the list
		parent = self.get(Node.parent)
		if parent == None:
			pass
		elif parent.get(Node.child) == self: 
			nxt = self.get(Node.after)
			if nxt == None:
				parent.remove(Node.child)
			else:
				parent.set(Node.child, nxt)
		self.remove(Node.parent)
		self.remove(Node.after)
		self.remove(Node.before)
		self.remove(Node.child)
	
	def removeFromList(self):
		# Pre:  Next <-> self <-> Prev
		#				  ^
		#				  V
		#		... <-> Child
		#
		# Post: 	Next <-> Prev
		nxt = self.get(Node.after)
		prv = self.get(Node.before)
		if nxt != None and prv != None:
			child = self.get(Node.child)
			
			# Remove self from next/prev list
			self._removeAll()
			
			# Destroy all children
			child.destroy(head = True)
			
			# Reconnect the next/prev list
			nxt.remove(Node.before)
			prv.remove(Node.after)
			nxt._insert(after=prv)

	# Subclasses to impliment setters for:
	#	self.iid	
	

	# ***** ************************** ***** #
	#		Static Methods for Tkinter		 #
	# ***** ************************** ***** #
	
	def appendNode(node, withIid = None):
		# Use the given iid:
		if withIid != None:
			Node.iids[withKey] = node
			return True
		
		# Use the node's iid:
		elif node.refs[Node.iid] != None:
			Node.iids[node.refs[Node.iid]] = node
			return True
		
		# No iid given or found:
		return False

	def nodeForIid(iid):
		return Node.iids[iid]

	# ***** **************************** ***** #
	#		Instance Methods for Tkinter	   #
	# ***** **************************** ***** #
	
	
	def setIid(self, iid):
		Node.appendNode(self, withKey = iid)
		self.iid = iid
	
	def delete(self):
		del(Node.iids[self.iid])
		self.iid = None
		# {CMC} Code to reconnect the surrounding nodes
		self._pluck()

	
				
###############################
### ***** Unit - Tests **** ###
###############################


if __name__ == "__main__":
	from CDS import *
	from Columbus import *
	
	curdir = os.getcwd()
	#print(curdir)


#	filepaths = [os.path.join(curdir, 'Model2.py')]
#	filepaths.append(os.path.join(curdir, 'setup.py'))
#	filepaths.append(os.path.join(curdir, 'setup.py'))
#	filepaths.append(os.path.join(curdir, 'setup.py'))


	lines = CDS.readfiles(filepaths)
	cdslines = CDS.readfiles([os.path.join(curdir, 'Columbus Database Source', 'Current projects.cds')])
	
	#cdsPath = os.path.join(curdir, 'Columbus Database Source', 'Test.cds')
	cdsPath = os.path.join(curdir, 'Columbus Database Source', 'Current projects.cds')
	cdsPath2 = os.path.join(curdir, 'Columbus Database Source', 'Infrasource.cds')
	cdsPath3 = os.path.join(curdir, 'Columbus Database Source', 'ESM-Project Template.cds')
	'ESM-Project Template.cds'

	# something is FUBAR in the build() method, the node.flatten() output list is all screwed up
	# -> all better now =)
	node = CDS.build(cdsPath)
	node2 = CDS.build(cdsPath2)
	node3 = CDS.build(cdsPath3)
	


	# Find the node that the second CDS should be inserted under and do the nasty:
	match = node.search('infrasource.cds', Node.value)[0]
	node2.move(under=match, allNodes=True)

	
	#ls = node.flatten()
	#for ln in ls:
	#	print(ln)

	def search(text, node):
		matches = node.search(text, Node.label)
		for match in matches:
			print(match.get(Node.label))
		print()


	
	search('122', node)

	print(len(node.flatten()))
	
	
#	for nd in node3.flatten():
#		print(nd.refs[Node.label], '\n\t', nd.refs[Node.value])
	nd = node3
	while nd.refs[Node.after] != None:
		print(nd.refs[Node.label])
		if nd.refs[Node.child]:
			for child in nd.children():
				print('\t', child.refs[Node.label])
		nd = nd.refs[Node.after]
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
		
		
		


