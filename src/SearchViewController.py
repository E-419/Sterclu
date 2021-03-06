import os, sys, pathlib
if 'src' in os.getcwd():
	from tkExt import *
	from Node import Node
else:
	from src.tkExt import *
	from src.Node import Node


class SearchViewController():
	'''
	This class is built specifically for the ProjectView
	'''
	
	def __init__(self, model=None, view=None):
		self.model = model  			# This is a Node() of some sort
		self.view = view				# This is a SearchView()
		self.searchItemFocus = list()	# A place to store the current iid of the item(s) with focus
		
		self.setCallbacks()
		
		self.loadview()
	
	def setCallbacks(self):
		def callback(*args):
			self.searchBarUpdated()

		# {CMC revision to use the tk.StringVar for searchbar.text updates}
		# self.view.searchbar.setCallback(self.searchBarUpdated) 
		self.view.searchbar.text.trace('w', callback)
	
	
	def setSelectMode(self, mode):
		if mode == Treeview.selectmode_single:
			self.selectmode = Treeview.selectmode_single
		elif mode == Treeview.selectmode_multi:
			self.selectmode = Treeview.selectmode_multi
		else:
			self.selectmode = Treeview.selectmode_none
		self.view.treeview.configure(selectmode = self.selectmode)
	
			
	def searchBarUpdated(self, searchbar = None):
		tv = self.view.treeview
		self.reset_treeview()
		txt = self.view.searchbar.text.get()
		matches = None
		matchlist = None

		# Search is over, reset the view with the newly selected items (if any)
		if txt == '': 
			itemsToShow = None
			if len(self.searchItemFocus) != 0:
				if self.selectmode == Treeview.selectmode_multi:
					itemsToShow = self.searchItemFocus # List of iids
				elif self.selectmode == Treeview.selectmode_single:
					itemsToShow = tv.focus() # Single iid
				
				self.loadview()
				tv.selection_set(itemsToShow)
			
				# Reset the search item list
				self.searchItemFocus = list()
				
				# Set the treeview to show the last item selected:
				if type(itemsToShow) == str:
					tv.see(itemsToShow)
				else:
					tv.see(itemsToShow[-1])
			return
		
		# Search is going, create a list of the items to show:
		else:
			
			self.searchItemFocus.append(tv.focus())
			tv.selection_set('')
			
			# Split the search text into a list of stripped strings:
			txtList = txt.strip().split(' ')

			# Create a list of matches for each _txt in txtList:
			matches = list()
			for _txt in txtList:
				matches.append(self.search(_txt))

			# Keep only the matches that occur in all lists of txtList:
			matchlist = set(matches[0])
			for _matchList in matches:
				matchlist &= set(_matchList)

			# Cast the set() to a list()
			matchlist = list(matchlist)
		
		# Do the nasty:
		self.loadview(withList = matchlist)
	
	def reset_treeview(self):
		self.view.treeview.detach_all()
		self.loadview()

	def search(self, text):
		# In: 		Search text (str)
		# Process:	Loop through model and compare values with search text
		# Out:		Return a list of unique matches

		results = list()
		keylist = list(self.model.refs.keys())

		# Reorder keys to give search precedence to the node.label and node.value first
		# 
		# ... I'm not convinced that this actually does anything...
		keylist.remove(Node.label)
		keylist.remove(Node.value)
		keylist.insert(0, Node.value)
		keylist.insert(0, Node.label)
		
		for key in keylist:
			
			# Skip the internal node references 
			if key in [Node.before, Node.after, Node.parent, Node.child, Node.iid]:
				continue
			
			# Search for this text in the model and add stuff to the results list:
			for match in self.model.search(text, key):
				if match not in results:
					results.append(match)

		# Return the list of unique matches:
		return results
		
		
	def filter(fileList, filterString):
		ls = list()
		for itm in fileList:
			if filterString.lower() in itm.lower():
				ls.append(itm)
		return ls	

	
	def loadview(self, tempModel = None, withList = None):
		
		# Shorthand var names
		tv = self.view.treeview
		mod = self.model
#		tv.detach_all()
		
		# Use the passed model
		if tempModel != None:
			mod = tempModel
		
		elif withList != None:
			# withList is a list of Node()
			# __lt__ is defined in Node.py for this function and compares Node().refs[Node.iid]
			mod = sorted(withList)
			
		# Setup
		root = ''
		parentiid = root
		curNode = mod
		
		########################
		# Search item loading:
		#	Create a list of items at the root of the Treeview 
		#	where the children are retained by a parent that fits
		#	the search criteria.	
		
		ls = list()
		if type(mod) == list:
			
			def addIid(lst, node):
				# Only add iid if it's been loaded into self.view.treeview
				if Node.iid in node.refs.keys():
					lst.append(node.refs[Node.iid])
			
			prev = None		
			for x in mod:
				# Add the first item to the tv.root:
				if prev == None:
					addIid(ls, x)
					prev = x
					continue
				

				breakToggle = False
				for _iid in tv.get_children():
					if breakToggle:
						breakToggle = False
						break
					rootNode = Node.nodeForIid(_iid)
					if rootNode.isParent(x):
						breakToggle = True
						continue

					addIid(ls, x)

			tv.set_children(root, *ls)
			return
			
		#
		########################

		
#		if type(mod) == list:
#			
#			'''
#			1. Create a linked Node() list from the list of Nodes
#				-> To be done here because the input is given to be a list of Node()s
#			2. The original Node() iid is the value of the temp_list
#			3. Upon selection, the original Node() is used to populate the other GUI components
#			'''

		
		# Do the loading
		if mod != None:		
			for ls in mod.tree():
				x = ls[0]
				ref = ls[1]
				pos = ls[2]
				print(x, ref, pos)
				
				# Check for items with iid's already and use tv.move() to place them (.move() handles relative connections between nodes)
				if Node.iid in x.refs.keys():
					if ref == root:
						tv.move(x.refs[Node.iid], root, 0)
					elif pos == Node.child:
						tv.move(x.refs[Node.iid], ref.refs[Node.iid], 'end')
					elif pos == Node.after:
						if ref.refs[Node.parent] == None:
							tv.move(x.refs[Node.iid], root, 'end')
						else:
							tv.move(x.refs[Node.iid], ref.refs[Node.parent].refs[Node.iid], 'end')
					continue
				else:
					# These items get inserted because they have no iid's
					if ref == root:
						x.refs[Node.iid] = tv.insert(root, 'end', text=x.refs[Node.label])
					elif pos == Node.child:
						x.refs[Node.iid] = tv.insert(ref.refs[Node.iid], 'end', text=x.refs[Node.label])
					elif pos == Node.after:
						if ref.refs[Node.parent] == None:
							x.refs[Node.iid] = tv.insert(root, 'end', text=x.refs[Node.label])
						else:
							x.refs[Node.iid] = tv.insert(ref.refs[Node.parent].refs[Node.iid], 'end', text=x.refs[Node.label])
					
					Node.appendNode(x) 
		
				


if __name__ == '__main__':
	from JBNode import JBNode as Node
#	from CustomView import *
	from AutoScrollBar import AutoScrollbar
	from SearchView import SearchView
	
	
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
	
#	print(n3.isParent(n1))
	
	
#	print(str(Node.refInv('test')))
	
	root = tk.Tk()
	sv = SearchView(root)
	
	
	# Model needs to be a JBNode to behave correctly, although Nodes will work.
	svc = SearchViewController(model=n1, view=sv)
	svc.setSelectMode(Treeview.selectmode_single)

	svc.view.treeview.detach_all()
	svc.loadview(tempModel=n1)
	
#	svc.configure(selectmode=Treeview.selectmode_single)
	
#	n1.refs[Node.iid] = sv.treeview.insert(''			  ,     0, text=n1.refs[Node.label])
#	n2.refs[Node.iid] = sv.treeview.insert(n1.refs[Node.iid], 'end', text=n2.refs[Node.label])

	
#	print(n1.refs[Node.iid], n2.refs[Node.iid])
		
	
	root.grid_propagate(0)
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	root.configure(width=200, height=600)
	
	root.mainloop()

