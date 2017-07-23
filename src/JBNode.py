import os, sys, pathlib
# if __name__ == '__main__':
# 	from Node import *
# else:
if 'src' in os.getcwd():
	from Node import *
else:
	from src.Node import *

root = ''

class JBNode(Node):
	count = 0
	# iids = dict() # empty dictionary
	# set: JBNode.iids[someKey] = someValue
	# get: JBNode.iids[someKey]
	yearID = 'yearID'
	clientID = 'clientID'
	
	
	# Designated init:
	def __init__(self, label, value = None, cdsKey = None):
		Node.__init__(self, label, value)
		self.cdsKey = cdsKey
		self.refs[JBNode.yearID] = None
		self.refs[JBNode.clientID] = None
		
	
	# ***** ***************** ***** #
	#       Convenience inits       #
	# ***** ***************** ***** #
	
	def init(	label = '', 
				value = None, 
				cdsKey = None, 
				parent = None, 
				after = None, 
				before = None,
				asChildOf = None): # Depricated
		
		node = JBNode(label, value, cdsKey = cdsKey)
		
		if parent:
			node.move(under=parent)
		
		elif after:
			node.move(after=after)
		
		elif before:
			node.move(before=before)

		elif asChildOf:
			parent = asChildOf
			child = parent.get(Node.child)
			if child != None:
				node.move(under=parent)
			else:
				node.move(before=child)
		
		return node
		

	# ****** Depricated ******
	def initWithParent(label = '', value = None, cdsKey = None, parentNode = None):
		node = JBNode(label, value, cdsKey = cdsKey)
		node.move(under=parentNode)
		return node
	
	def initWithPrev(label = '', value = None, cdsKey = None, prevNode = None):
		node = JBNode(label, value, cdsKey = cdsKey)
		node.move(after=prevNode)
		return node
			

	# # ***** ************** ***** #
	# #		Static Methods		 #
	# # ***** ************** ***** #
	
	# def appendNode(node, withKey = None):
	# 	# Do checks for unique key values, ensure withKey != None
	# 	JBNode.iids[withKey] = node
	
	# def nodeForIid(iid):
	# 	return JBNode.iids[iid]


	# # ***** **************** ***** #
	# #		Instance Methods	   #
	# # ***** **************** ***** #
	
	# def setIid(self, iid):
	# 	JBNode.appendNode(self, withKey = iid)
	# 	self.iid = iid
	
	# def delete(self):
	# 	del(JBNode.iids[self.iid])
	# 	self.iid = None
	# 	# {CMC} Code to reconnect the surrounding nodes
	# 	self._pluck()
		
	
	def __str__(self):
		return ('Label: ' + str(self.label) + ', Value: ' + str(self.value) + ', IID: ' + str(self.iid) + '')




