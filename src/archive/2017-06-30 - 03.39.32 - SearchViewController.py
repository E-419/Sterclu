import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
#if __name__ == '__main__':
#	from tkBase import *
#	from Node import *
#else:
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
		# if __name__ == '__main__':
		# 	try:
		# 		print(searchbar.text.get())
		# 	except:
		# 		pass
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
				# for _match in self.search(_txt):
				# 	matches.append(_match)


			# Keep only the matches that occur in all lists of txtList:
			matchlist = set(matches[0])
			for _matchList in matches:
				matchlist &= set(_matchList)

			# Cast the set() to a list()
			matchlist = list(matchlist)


			# searchTxtList = txt.split(' ')
			
			# matchesLists = list()
			# matchesSets = list()
			# matches = set()

			# for txt in searchTxtList:
			# 	for itm in self.search(txt):
			# 		matches.add(itm)
			# 	# matchesLists.append( self.search(itm) )
			# 	# matchesSets.append( set(matchesLists[-1]))

			# matches = matchesSets[0]
			# for matchset in matchesSets:
			# 	# Keep only the nodes that appear in all lists:
			# 	matches &= matchset
			# matchlist = list(matches)
			# # # This should be removed:
			# # for nodeSet in matchesLists:
			# # 	for itm in nodeSet:
			# # 		for _set in matchesLists:
			# # 			if itm not in _set:
			# # 				nodeSet.remove(itm)
			# # 	matchlist = nodeSet


			# matchlist = self.search(txt)
		
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
		for key in self.model.refs.keys():
			
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
#		
#		# {CMC} this needs to change to loop through the Node.refs.keys()
#		matches = [Node(label='***** Label Matches *****')]
#		
#			
#		# Search Node Labels:
##		matches.append(self.model.search(text, Node.label))
#		for itm in self.model.search(text, Node.label):
#			matches.append(itm)
#		
#		# Search JBNode Client Numbers:
#		matches.append(Node(label='***** Client Number Matches *****'))
#		for itm in self.model.search(text, 'clientID'):
#			matches.append(itm)
#		
#		# Search JBNode Year Codes:
#		matches.append(Node(label='***** Year Code Matches *****'))
#		for itm in self.model.search(text, 'yearID'):
#			matches.append(itm)
		
#		for match in matches:
#			print(match.get(Node.label))
#		print()
#		return matches
		
		# Update the view 
#		self.loadView(tempModel = matches)
	
	def loadview(self, tempModel = None, withList = None):
		
		# Shorthand var names
		tv = self.view.treeview
		mod = self.model
#		tv.detach_all()
		
		# Use the passed model
		if tempModel != None:
			mod = tempModel
		elif withList != None:
			mod = withList
		
		
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
					# if Node.iid in x.refs.keys():
					# 	ls.append(x.refs[Node.iid])
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



				# if prev.isParent(x):
				# 	pass
				# else:
				# 	addIid(ls, x)
				# prev = x
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
#			
#			
#			# 1.
#			head = Node.copy(mod[0])
##			head.set[Node.value, mod[0].refs[Node.iid]]
#			node = None
#			prevNode = head
#			
#			for x in mod[1:]:
#				node = Node.copy(x)
#				if Node.iid in x.refs.keys():
#					node.set(Node.value, x.refs[Node.iid])
#				prevNode.set(Node.after, node)
#				prevNode = node
#			
#			mod = head
		
		# Do the loading
		if mod != None:
			
#			# {CMC} this is a bug, it assumes the tree is always empty at the start.
#			emptyTree = True
			
			for ls in mod.tree():
				x = ls[0]
				ref = ls[1]
				pos = ls[2]
				print(x, ref, pos)
				
				# Check for items with iid's already and use tv.move() to place them
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
					# 
					Node.appendNode(x) 
		
				
			
#			for x in mod:
#				print(x.refs[Node.label])
#				if Node.iid in x.refs.keys():
#					if Node.iid in tv.get_children():
#						continue
#					tv.move(x.refs[Node.iid], root, 'end')
#					
#				else:
#					tv.insert(root, 'end', text=x.refs[Node.label])
#				
				

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
	n6 = Node('test label 6', 'esm8\\engr\\esm-jobs\\1234\\004\\014\\Project.cds')
	n7 = Node('test label 7', 'esm8\\engr\\esm-jobs\\1234\\005\\016\\Project.cds')
	
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
	n5.set(Node.clientID, '1234')
	
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

