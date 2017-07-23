import os
if 'src' in os.getcwd():
	from tkExt import *
	from StatusBar import *
	from SearchView import *
	from ContextMenu import *
	from Icon import *
else:
	from src.tkExt import *
	from src.StatusBar import *
	from src.SearchView import *
	from src.ContextMenu import *
	from src.Icon import *


class _ProjectView(Frame):
	'''
	* * * * * * * * * * * * * * *
	* * * Columbus Specific * * *
	* * * * * * * * * * * * * * *
	
	This class will use composition to house the dual paned-window view 
	that shows the folder and file structure of the Columbus data model.
	
	This class should be instantiated for each new notebook tab.
	
	All options here should be hardcoded to start, as much as I don't 
	like it. The reason is that this view won't change much... ever. A
	new or different view will be made for this app if a UI overhaul is 
	needed.
	'''
	class _PanedWindow(Frame):
		def __init__(self, master, *args, **kw):
			super().__init__(master, *args, **kw)
			# Configure Widget:
			self.grid_propagate(0)
			self.rowconfigure(0, weight=1)
			self.columnconfigure(0, weight=1)
			self.grid(sticky=tkSticky.fill)
			
			# Create Subwidgets:
			self.horizontal = Panedwindow(self, orient=tk.HORIZONTAL)
			self.vertical	= PanedWindow(self, orient=tk.VERTICAL)	
			self.horizontal.grid(sticky=tkSticky.fill)
			self.vertical.grid(sticky=tkSticky.fill)
			
	
#	class _SearchView(Frame):
#		def __init__(self, master, *args, **kw):
#			super().__init__(master, *args, **kw)
#			# Configure Widget:
#			self.grid_propagate(0)
#			self.rowconfigure(1, weight=1)
#			self.columnconfigure(0, weight=1)
#			self.grid(sticky=tkSticky.fill)
#			
#			# Create Subwidgets:
#			self.treeview = Treeview(self)
#			self.searchbar = SearchBar(self)
#			self.treeview.grid(row=1, sticky=tkSticky.fill)
#			self.searchbar.grid(row=0, sticky=tkSticky.fill)
			
	
	def __init__(self, master, *args, **kw):
		super().__init__(master, *args, **kw)
		self.JobBrowserDelegate = None
		self.FileBrowserDelegate = None
		
		# Event Callback function:
		self.callback = None
		self._configureWidget()
		self._createWidgets()
			
	def _configureWidget(self):
		# Apply to widget to parent:
		self.grid(sticky=tkSticky.fill)   
		self.rowconfigure(	 0, weight = 1)
		self.columnconfigure(0, weight = 1, minsize=200)

	def _createWidgets(self):		
		# PanedWindow (PW)
		self.PW = _ProjectView._PanedWindow(self)
		
		# Job Browser (JB)
		self.JB = SearchView(self.PW.horizontal)
		self.JB.configure(width=250)
		#self.JB.searchbar.setCallback(self.JBController.searchCallback)
		
		# File Browser (FB)
		self.FB = SearchView(self.PW.vertical)
		self.FB.grid_propagate(1)
		#self.FB.searchbar.setCallback(self.FBController.searchCallback)
		
		# Grid everything:
		self.PW.horizontal.add(self.JB)
		self.PW.horizontal.insert(self.JB, self.PW.vertical, weight = 0)
		self.PW.vertical.add(self.FB)
		







class ProjectViewer(Notebook):
	'''
	* * * * * * * * * * * * * * *
	* * * Columbus Specific * * *
	* * * * * * * * * * * * * * *
	
	This is a Notebook() wrapper for the _ProjectView() class above.
	'''
	def __init__(self, master, *args, **kw):
		super().__init__(master, *args, **kw)
		self.PV = dict()
		self.tabId = 0
		self._configureWidget()
		self._createWidgets()
		##{CMC_BINDINGS}
		self.bind_all('<Control-KeyPress-t>', self.addTabEvent)
		self.bind_all('<Control-KeyPress-w>', self.deleteTabEvent)
		self.bind('<Shift-Button-1>', self.deleteTabEvent)
#		self.bind(Notebook.event_tab_changed, lambda x: print('tab changed'))
		# print(Notebook.event_tab_changed)
		self.bind('<<NotebookTabChanged>>',self.tabChanged)
		
		# self.bind(Notebook.event_tab_changed, self.tabChanged)
		
		
		
		# Build the context menu:
		self.CMenu = ContextMenu(self)
		
		menuList = 	[	
						MenuItem(label='Close Tab', command=self.deleteTab),
#						MenuItem(label='New Tab', command=self.addTab),
						MenuItem(label='High', command=self.printHigh),
						MenuItem(label='Low', command=self.printLow)
					]
		
		self.CMenu.loadMenuItems(menuList)
	
	def _configureWidget(self):
		# Apply to widget to parent:
		self.grid(sticky=tkSticky.fill)   
		self.rowconfigure(	 0, weight = 1)
		self.columnconfigure(0, weight = 1)
		self.enable_traversal()
	
	def _createWidgets(self):
		# Insert the '+' tab first, then a blank:
		self.addIcon = Icon.add()
		self.addTab(image=self.addIcon)
		self.addId = self.select()
		self.addTab()
	
	def printHigh(self):
		print('high')
		
	def printLow(self):
		self.bell()
		print('Low')
		
	def addTabEvent(self, event):
		print('add tab event called')
		self.addTab()
		
	def deleteTabEvent(self, event):
		self.deleteTab(event=event)
	
	def deleteTab(self, tab=None, event=None):
		# Forget the tab that's currently selected 
		# and select the tab to the left
		#
		# 'tab' is a numeric index of the selected tab, counting from 0
		# self.index('end') returns the number of tabs, counting from 1
		
		# Local vars:
		t = None
		x = y = 0
		
		# Figure out where the user clicked:
		if event:
			# From the '<Shift-Button-1>' event
			x = event.x
			y = event.y
		else:
			# From the '<Button-2>' event
			x = self.CMenu.x
			y = self.CMenu.y
			
		# Identify the tab that was clicked:
		if x and y:
			t = self.index('@'+str(x)+','+str(y))
			tab = t
			# Exclude the addTab, OBOB was here:
			if tab == self.index('end') - 1:
				return
		
		# Do the nasty:
		tab = self.selectTab(tab)
		self.selectPrevTab(tab)
		self.forget(tab)
	
	def selectTab(self, tab=None):
		# Selects the tab with index == 'tab', else it selects the current tab 
		# and returns a reference/index... I think... 
		tab = tab
		if tab == None:
			tab = self.select()
		return tab
	
	def selectPrevTab(self, tab=None):
		# From the currently selected tab, this method selects
		# the tab to the left and returns its index if it's not 
		# the '+' tab. Returns None otherwise.
		tab = tab
		if tab == None:
			tab = self.select()
		prevTab = self.index(tab) - 1
		if prevTab < 0:
			prevTab = 0
		self.select(prevTab)
		if tab == self.addId:
			return None
		return prevTab
	
	def addTab(self, tabName=None, image=None):
		
		if tabName == None:
			tabName = 'New Tab' + ' ' + str(self.tabId)
		self.PV[self.tabId] = _ProjectView(self)
		
		idx = self.index('end')
		if idx == 0:
			# This is the '+' icon tab: no text, icon only and run once at startup
			self.add(self.PV[self.tabId])
			self.tab(0, image=self.addIcon)
			self.tabId += 1
			return
			
		self.insert(idx-1, self.PV[self.tabId])
		self.tab(idx-1, text=tabName)
		
		idx = self.index('end')
		self.select(idx-1)
		self.tabId += 1
		

	def tabChanged(self, event):
		'''
		The idea here is that *** if *** the '+' tab is clicked to add a new tab
		Then a new tab is created and the new tab is selected.
		
		Otherwise display the tab selected.
		'''
		# Add a new tab if the '+' tab is selected
		if self.select() == self.addId:
			self.addTab()
			self.selectPrevTab()
		print(self.select())
		print(event.widget)
	
	# Current Tab accessor methods:
	def _projectView(self):
		return self.nametowidget(self.select())
		
	def JB(self):
		return self._projectView().JB
	
	def FV(self):
		return self._projectView().FV







if __name__ == '__main__':
	root = tk.Tk()



	root.grid_propagate(0)
	root.rowconfigure(0, weight=1)
	root.columnconfigure(0, weight=1)
	root.configure(width=800, height=600)

	
	pv = ProjectViewer(root)
	sb = StatusBar(root)
	pv.grid(sticky=tkSticky.fill)
	sb.grid(sticky=tkSticky.horizontal + tkSticky.bottom)


	'''
	Add an app icon
	Taken from:
	http://stackoverflow.com/questions/16081201/setting-application-icon-in-my-python-tk-base-application-on-ubuntu

	This works on Windows and Ubuntu only
	'''
	# img = tk.Image("photo", file="icon_appicon.gif")
	img = Icon.appIcon()
	root.tk.call('wm','iconphoto',root._w,img)



	root.iconify()
	root.update()
	root.deiconify()
	root.mainloop()





