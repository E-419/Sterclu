import os

if 'src' in os.getcwd():
	from SearchView import SearchView
	from Node import Node
	from JBNode import JBNode
	from FBNode import FBNode
	from SearchViewController import SearchViewController

else:
	from src.Node import Node
	from src.JBNode import JBNode
	from src.FBNode import FBNode
	from src.SearchViewController import SearchViewController
	from src.SearchView import SearchView

class PVC(object):
	JB_model = 'JB_model'
	FB_model = 'FB_model'



class ProjectViewerController(object):
	def __init__(self, model_job_browser, view):
		self.refs = dict()


	def setModel_JB(self, model):
		self.refs[PVC.JB_model] = model

	def setModel_FB(self, model):
		self.refs[PVC.FB_model] = model

if __name__ == '__main__':
	from tkExt import *


	# Psuedo Job Browser Model:
	TVroot = ''
	
	# Head:
	jb1 = JBNode.init(parent=TVroot,			label = 'Bonaventure', 	value = '<INCLUDE \\\\esm8\\engr\\...\\1234\\001\\016\\Project.cds', cdsKey = 1)
	
	# Same parent as previous node:
	# jb2 = JBNode.initWithPrev(	label = 'Creviston', 	value = '<INCLUDE \\\\esm8\\engr\\...\\1235\\005\\007\\Project.cds', cdsKey = 5, prevNode = jb1)
	jb2 = JBNode.init(after=jb1, label = 'Creviston', 	value = '<INCLUDE \\\\esm8\\engr\\...\\1235\\005\\007\\Project.cds', cdsKey = 5,)

	# As a child of some other node (probably works with treeview.root too):
	# jb3 = JBNode.initWithParent(label = 'Test Child', 	value = '<INCLUDE \\\\esm8\\engr\\...\\1234\\002\\013\\Project.cds', cdsKey = 1, parentNode = jb1)
	jb3 = JBNode.init(parent=jb1, label = 'Test Child', 	value = '<INCLUDE \\\\esm8\\engr\\...\\1234\\002\\013\\Project.cds', cdsKey = 1)


	# Das GUI:
	root = tk.Tk()
	jobBrowser = SearchView(root)
	jobBrowser.grid(row=0,column=0, sticky=tkSticky.fill)



	# Root window defaults
	# -> To Do: make these values read from a file that saved from the last session
	root.grid_propagate(0)
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	root.configure(width=800, height=600)
	root.mainloop()


	# Psuedo File Browser Model:

	# mod = N
	# PVC = ProjectViewerController(mod, view)

