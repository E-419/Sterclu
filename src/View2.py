import os, sys, pathlib

## Standard tkinter import calls -> defaults to using themed Tkinter 
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from tkinter.ttk import *


import PIL 
	
##  ********** TKINTER EXTENTIONS ***********  ##           
#
# All modifications to these classes shall conform to the established Tkinter 
# style.
#
# Example:
#   class TkClass(TkClass):
#       def lower_case_methods_with_underscores(self):
#           pass
#
#
#
#
#

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  		  *********** Data Classes ***********  		   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Custom data storage classes:
class tkSticky():
	top         = 'n'
	left        = 'w'
	right       = 'e'
	bottom      = 's'
	vertical    = top + bottom
	horizontal  = left + right
	fill        = vertical + horizontal 

class tkEvent():
	'''
	Event Binding: Passing event to Parent (Python 2.7)
	http://stackoverflow.com/questions/32771369/how-to-pass-an-event-to-parent-widget/32771893#32771893
	
	This method calls for the use of Bind Tags (.bindtags(tuple(object.ref)))
	'''
	key_down   = '<KeyPress>'
	key_up     = '<KeyRelease>'
	key_escape = '<KeyPress-Escape>'
	key_delete = '<KeyPress-Delete>'





class Icon():
	'''
	All files that are to be used as icons in this app should be ref'd from this class
	and follow the naming convention 'icon_lowercaseiconname.gif'
	
	That will allow for all the files to stay in the root folder and be moderately organizable
	via this application's file filtering capabilities.
	
	This class depends on the Pillow module:
		https://pypi.python.org/pypi/Pillow/2.2.1
	
	import pip
	pip.main(['install','Pillow'])

	
	
	'''
#	BITMAP = """
#	#define im_width 32
#	#define im_height 32
#	static char im_bits[] = {
#	0xaf,0x6d,0xeb,0xd6,0x55,0xdb,0xb6,0x2f,
#	0xaf,0xaa,0x6a,0x6d,0x55,0x7b,0xd7,0x1b,
#	0xad,0xd6,0xb5,0xae,0xad,0x55,0x6f,0x05,
#	0xad,0xba,0xab,0xd6,0xaa,0xd5,0x5f,0x93,
#	0xad,0x76,0x7d,0x67,0x5a,0xd5,0xd7,0xa3,
#	0xad,0xbd,0xfe,0xea,0x5a,0xab,0x69,0xb3,
#	0xad,0x55,0xde,0xd8,0x2e,0x2b,0xb5,0x6a,
#	0x69,0x4b,0x3f,0xb4,0x9e,0x92,0xb5,0xed,
#	0xd5,0xca,0x9c,0xb4,0x5a,0xa1,0x2a,0x6d,
#	0xad,0x6c,0x5f,0xda,0x2c,0x91,0xbb,0xf6,
#	0xad,0xaa,0x96,0xaa,0x5a,0xca,0x9d,0xfe,
#	0x2c,0xa5,0x2a,0xd3,0x9a,0x8a,0x4f,0xfd,
#	0x2c,0x25,0x4a,0x6b,0x4d,0x45,0x9f,0xba,
#	0x1a,0xaa,0x7a,0xb5,0xaa,0x44,0x6b,0x5b,
#	0x1a,0x55,0xfd,0x5e,0x4e,0xa2,0x6b,0x59,
#	0x9a,0xa4,0xde,0x4a,0x4a,0xd2,0xf5,0xaa
#	};
#	"""
#	
#	def __init__(self):
#		self.bitmap = tk.BitmapImage(
#			data=IconImage.BITMAP,
#			foreground="white", background="black"
#			)
	
	def resource(fileName=None, fullpath = None):
		if fileName:
			imageName = 'icon_' + fileName + '.gif'
			if fullpath:
				fileName = os.path.join(fullpath, 'res', imageName)
			else:
				fileName = os.path.join('.', 'res', imageName)			
			return tk.PhotoImage(file=fileName)
	
	def cancel():
		return Icon.resource('cancel')

	def add():
		return Icon.resource('add')
	
	def appIcon(fullpath = None):
		return Icon.resource('appicon', fullpath = fullpath)





# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  		*********** Widgets Extensions *********** 		   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Tkinter Extensions:
#   All GUI classes have been extented into a more general framework.
#	This embodies the 'batteries included' mentality much better this
#	way.
#
# Usage:
#   Instantiate the Frame() and Treeview() object as normal, however
#	they have been potentially restricted to the .grid() method only.
#	I don't know enough about .pack() or .place() to check otherwise.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# tkinter extensions:
#
class AutoScrollbar(Scrollbar):
	#
	#	http://effbot.org/zone/tkinter-autoscrollbar.htm
	#
	'''
	A scrollbar that hides itself if it's not needed.
	Only works if you use the grid geometry manager!
	Usage:
		sb = AutoScrollbar(master, orient=tk.HORZONTAL/VERTICAL)
		sb.grid(row=..., column=..., sticky=Stick.horizontal/vertical
		scrolledWidget = Widget(master, x/yscrollcommand = sb.set)
	
	Update:
		Changed to add a callback() when the scrollbar is displayed,
		that way a grip can be gridded when both bars are shown (if
		desired).
		
		Don't use this directly, just use the ScrollView() instead.
	
	'''
	def __init__(self, master, *args, **kwargs):
		Scrollbar.__init__(self, master, *args, **kwargs)
		self.callback = None
		
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			self.grid_remove()
			if self.callback != None:
				self.callback(False)
		else:
			self.grid()
			if self.callback != None:
				self.callback(True)
		Scrollbar.set(self, lo, hi)
	
	def setCallback(self, callback):
		self.callback = callback
	
	# Reject all non-grid() geometry managers:
	def pack(self, **kw):
		raise TclError("cannot use pack with this widget")
	def place(self, **kw):
		raise TclError("cannot use place with this widget")

class ScrollView():
	'''
	A flaw in this design is that the scrollbars actually cover some of the content
	rather than resize the view, so there is no way to scroll to the left and lower
	edges of the view at this time.
	
	Example Usage (direct):
		root = tk.Tk()
		tv = ttk.Treeview(root)
		Scrollview(tv)
		
		# Configure the widget for display:
		tv.grid(sticky='NSEW')   
		tv.grid_propagate(0)
		tv.column('#0', stretch=0)
		tv.column(0, stretch=0)
		# ...
		#tv.column(n, stretch=0)
		
		root.mainloop()
	
	Or (tk.class extension):
		class Treeview(Treeview):
			def __init__(self, master, **kw):
				super().__init__(master, **kw)
				
				# Make this widget a scrolled view:
				self.sv = ScrollView(self)
				
				# Configure the widget for display:
				self.grid(sticky='NSEW')   
				self.grid_propagate(0)
				
				# Set columns to not stretch, otherwise they don't play nicely with ScrollView()
				self.column('#0', stretch=0)
				if 'columns' in kw.keys():
					print('columns in keys')
					for column in kw['columns']:
						self.column(column, stretch=0)
				self.rowconfigure(		0, weight = 1)
				self.columnconfigure(	0, weight = 1)	

	'''
	def __init__(self, master): # master is any view widget that implements _scrollcommand
		# Setup horizontal scroll bar
		self.xScroll = AutoScrollbar(master, orient=tk.HORIZONTAL)
		master.configure(xscrollcommand=self.xScroll.set)
		self.xScroll.grid(row=1, column=0, sticky=tkSticky.horizontal + tkSticky.bottom)
		self.xScroll.config(command=master.xview)
		self.xScroll.setCallback(self.xScrollViewChanged)
		
		# Setup vertical scroll bar
		self.yScroll = AutoScrollbar(master, orient=tk.VERTICAL)
		master.configure(yscrollcommand=self.yScroll.set)
		self.yScroll.grid(row=0, column=1, sticky=tkSticky.vertical + tkSticky.right)
		self.yScroll.config(command=master.yview)
		self.yScroll.setCallback(self.yScrollViewChanged)
		
		# Setup the little patch thingy that shows in the lower right corner when both scrollbars appear
		self.grip = Sizegrip(master)
		self.grip.grid(row=1,column=1)
		self.yIsShown = True
		self.xIsShown = True
		'''
		To be finished...
		'''
	def updateGripView(self):
		if self.yIsShown and self.xIsShown:
			self.grip.grid()
		else:
			self.grip.grid_remove()
	
	def yScrollViewChanged(self, isShown):
		self.yIsShown = isShown
		self.updateGripView()
	
	def xScrollViewChanged(self, isShown):
			self.xIsShown = isShown
			self.updateGripView()

		
class Treeview(Treeview):
	'''
	The columns are set to not stretch by default. It is advisable to only
	allow the right-most column to be allowed to stretch (if any) because 
	of the negative interactions with the ScrollView(). 
	
	There is a bug where the AutoScrollbar() won't re-grid if a column is set
	to stretch=1.
	
	Example Usage:
		root=tk.Tk()
		tv = Treeview(root)
		# tv.insert(bunch-o-items)
		root.mainloop()
	'''
	event_select = '<<TreeviewSelect>>'
	event_open   = '<<TreeviewOpen>>'
	event_close  = '<<TreeviewClose>>'
	root         = ''	
		
	def __init__(self, master, **kw):		
		super().__init__(master, **kw)
		
		# Make this widget a scrolled view:
		self.sv = ScrollView(self)
		
		# Configure the widget for display:
		self.grid(sticky=tkSticky.fill)   
		self.grid_propagate(0)
		
		# Set columns to not stretch, otherwise they don't play nicely with ScrollView()
		self.column('#0', stretch=0)
		self._setColumnStretchToZero(**kw)

		self.rowconfigure(		0, weight = 1)
		self.columnconfigure(	0, weight = 1)	
	
	def configure(self, *args, **kw):
		super().configure( **kw)
#		self._setColumnStretchToZero(**kw)
	
	def _setColumnStretchToZero(self, **kw):
		# Update the stretch kw if columns were added:
		if 'columns' in kw.keys():
			if type(kw['columns']) != str and len(kw['columns']) > 1:
				for column in kw['columns']:
					self.column(column, stretch=0)
			else:
				self.column(kw['columns'], stretch=0)
		
	def column(self, cid, **kw):
		super().column(cid, **kw)
			
	def ext_test(self):
		print('''I'm awesome''')

	def detach_all(self):
		items = self.get_children()
		for item in items:
			self.detach(item)
	
	def delete_all(self):
		items = self.get_children()
		for item in items:
			self.delete(item)

class Frame(Frame):
	def ext_test(self):
		print('this is bawm')


class Notebook(Notebook):
	current = 'current'
	event_tab_changed = '<<NotebookTabChanged>>'
	
	def ext_test(self):
		print('this is bawm')












# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  	  *********** Context Menu Widgets ***********  	   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 




'''
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  	    *********** Binding to Parent ***********          ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
#	Via:
#	http://stackoverflow.com/questions/32771369/how-to-pass-an-event-to-parent-widget/32771893#32771893
#	...
#	Tkinter does not pass events to parent widgets. However, you can simulate the 
#	effect through the use of bind tags (or "bindtags").
#
#	The shortest explanation I can give is this: when you add bindings to a widget, 
#	you aren't adding a binding to a widget, you are binding to a "bind tag". This 
#	tag has the same name as the widget, but it's not actually the widget.
#
#	Widgets have a list of bind tags, so when an event happens on a widget, the 
#	bindings for each tag are processed in order. Normally the order is:
#
#		1. bindings on the actual widget
#		2. bindings on the widget class
#		3. bindings on the toplevel widget that contains the widget
#		4. bindings on "all"
#	
#	Notice that nowhere in that list is "bindings on the parent widget".
#
#	You can insert your own bindtags into that order. So, for example, you can add 
#	the main canvas to the bind tags of each sub-canvas. When you bind to either, 
#	the function will get called. Thus, it will appear that the event is passed to 
#	the parent.
#
#	Here's some example code written in python 2.7. If you click on a gray square 
#	you'll see two things printed out, showing that both the binding on the 
#	sub-canvas and the binding on the main canvas fire. If you click on a pink 
#	square you'll see that the sub-canvas binding fires, but it prevents the parent 
#	binding from firing.
#
#	With that, all button clicks are in effect "passed" to the parent. The 
#	sub-canvas can control whether the parent should handle the event or not, by 
#	returning "break" if it wants to "break the chain" of event processing.


## Python 2.7 ##
import Tkinter as tk

class Example(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent)
		
		self.main = tk.Canvas(self, width=400, height=400, 
								borderwidth=0, highlightthickness=0,
								background="bisque")
		self.main.pack(side="top", fill="both", expand=True)

		# add a callback for button events on the main canvas
		self.main.bind("<1>", self.on_main_click)

		for x in range(10):
			for y in range(10):
				canvas = tk.Canvas(self.main, width=48, height=48, 
									 borderwidth=1, highlightthickness=0,
									 relief="raised")
				if ((x+y)%2 == 0):
					canvas.configure(bg="pink")

				self.main.create_window(x*50, y*50, anchor="nw", window=canvas)

				# adjust the bindtags of the sub-canvas to include
				# the parent canvas
				bindtags = list(canvas.bindtags())
				bindtags.insert(1, self.main)
				canvas.bindtags(tuple(bindtags))

				# add a callback for button events on the inner canvas
				canvas.bind("<1>", self.on_sub_click)


	def on_sub_click(self, event):
		print "sub-canvas binding"
		if event.widget.cget("background") == "pink":
			return "break"

	def on_main_click(self, event):
		print "main widget binding"

if __name__ == "__main__":
	root = tk.Tk()
	Example(root).pack (fill="both", expand=True)
	root.mainloop()
'''






'''
# Code example for a ContextMenu()
# Taken from:
#	http://effbot.org/zone/tkinter-popup-menu.htm
# Written for Python 1, maybe 2

from Tkinter import *

root = Tk()

w = Label(root, text="Right-click to display menu", width=40, height=20)
w.pack()

# create a menu
popup = Menu(root, tearoff=0)
popup.add_command(label="Next") # , command=next) etc...
popup.add_command(label="Previous")
popup.add_separator()
popup.add_command(label="Home")

def do_popup(event):
	# display the popup menu
	try:
		popup.tk_popup(event.x_root, event.y_root, 0)
	finally:
		# make sure to release the grab (Tk 8.0a1 only)
		popup.grab_release()

w.bind("<Button-3>", do_popup)

b = Button(root, text="Quit", command=root.destroy)
b.pack()

mainloop()
'''



class MenuItem():
	'''
	This is purely a data container for ContextMenu construction
	
	Typical Usage:
	ls = list()
	ls.append(MenuItem(label='Hi Inner'))
	ls.append(MenuItem(separator=True)
	ls.append(MenuItem(label='Low Inner')
	mnu1 = ContextMenu(ls)
	
	ls.clear()
	ls.append(MenuItem(label='Hi Outer'))
	ls.append(MenuItem(separator=True)
	ls.append(MenuItem(label='Low Outer')
	ls.append(MenuItem(menuRef=mnu1)
	mnu2 = ContextMenu(ls)
	'''
	def __init__(self, label=None, command=None, accelerator=None, menuRef=None, separator=None):
		self.label=label
		self.command=command
		self.accelerator=accelerator
		self.menuRef=menuRef
		self.separator=separator

class ContextMenu(tk.Menu):
	'''
	This should be a flat menu, fly-outs are annoying usually.
	
	This is the base class that will be locally subclassed and 
	extended within other view classes. That will keep all the 
	options for each view's context menu within its own class 
	definition.
	
	
	Typical usage: (binds 'Right-Click' events on whatever the 'master' is on init)
	
	class SomeView(Frame):
		def __init__(self, master, *args, **kw):
			super().__init__(master, *args, **kw)
			self.subView = Treeview()
			...
			
			# Build the context menu:
			self.subView.CMenu = ContextMenu(self.subView) # <-- Right-Clicks bound to this passed object ref
			menuList = [	MenuItem(label='High', command=self.printHigh),
							MenuItem(label='Low', command=self.printLow)]
			self.subView.CMenu.loadMenuItems(menuList)
			
			...
	
	'''
	def __init__(self, master, *args, **kw):
		super().__init__(master)
		self.configure(tearoff=0)
		self.x = None
		self.y = None
		
		##{CMC_BINDINGS}
		# Bind the 'Right-Click' event for Windows and macOS:
		butevt = None
		if os.name == 'nt':
			butevt = '<Button-3>'
		else:
			butevt = '<Button-2>'
		master.bind('<Alt-Button-1>', self.popup)
		master.bind(butevt, self.popup)
	
	def setBindings(self, master):
		pass
	
	def popup(self, event):
		# This is the location that the context menu shows up at
		try:	
			self.post(event.x_root, event.y_root)
			self.x = event.x
			self.y = event.y
		finally:
			self.grab_release()
	
	def loadMenuItems(self, listOfMenuItems = None):
		if listOfMenuItems:
			for itm in listOfMenuItems:
				if itm.separator:
					self.add_separator()
				elif itm.menuRef:
					self.add_cascade(label=itm.label, menu=itm.menuRef)
				else:
					if itm.accelerator == None:
						itm.accelerator = ''
					self.add_command(	label=itm.label, 
										command=itm.command, 
										accelerator=itm.accelerator)

					















# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  		*********** Compound Widgets *********** 		   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
'''
This segment of code needs to be broken down into compound widgets 
that can be assembled into windows and such.

Each widget should be responsible for doing a specific task:
	JobBrowser
	FileBrowser
	
'''


class StatusBar(Frame):
	def __init__(self, master, *args, **kw):
		super().__init__(master, *args, **kw)
		
		self._configureWidget()
		self._createWidgets()
		
	def _configureWidget(self):
		self.grid(sticky=tkSticky.fill)
		
		# Set the stretchy part to be the width only:
		self.rowconfigure(	 0, weight = 0)
		self.columnconfigure(0, weight = 1)
		
	def _createWidgets(self):	
		self.text = tk.StringVar()
		self.text.set('This is the Status Message')
		self.grip = Sizegrip(self)
		self.label = Label(self, textvariable=self.text)
		self.label.grid(row=0, 
						column=0, 
						sticky=tkSticky.fill)
		self.grip.grid(	row=0, 
						column=1, 
						sticky=tkSticky.right + tkSticky.vertical)



class SearchBar(Frame):
	'''
	
	* * * * * * * * * * * *
	* * * General Use * * *
	* * * * * * * * * * * *
	
	This class is just the search bar and button with all associated
	bindings and calls built in. All that is required upon instantiation
	is the parent and callback functions be provided.
		
	Example usage:
		root = Tk()
		...
		t = SearchBar(root)
		t.setCallback(root.someCallbackfunction)
		...
		root.mainloop()
	Or:
		root = Tk()
		...
		t = SearchBar(root, callback=root.someCallbackfunction)
		...
		root.mainloop()
	Where:
		class root():
			...
			def someCallbackfunction(self, widget):
				SearchBarStringVar = widget.text
				SearchBarString = widget.text.get()
				# do stuff...
				...
				return
		
	self.callback() is called every time the user releases a key 
	or presses the delete/escape keys AND when the button is pressed.
	
	.callback() is passed a reference to self, as close to an event
	as I could devise without major weirdness happening.
	
	'''
	def __init__(self, master=None, debug = None, callback = None):
		Frame.__init__(self, master, class_='SearchBar')
		
		# Event Callback function:
		self.callback = callback
		
		# Public iVars:
		self.text = tk.StringVar()
		
		if debug:
			# This creates a small widget window:
			self._configureForDebug()
		else:
			# This is the default behavior
			self._configureWidget()
		self._createSearchBar()
		self._createCancelButton()
		
	def _configureWidget(self):
		# Apply to widget to parent:
		self.grid(sticky=tkSticky.fill)   
		
		# Set the stretchy part to be the Entry only:
		self.rowconfigure(	 0, weight = 1)
		self.columnconfigure(0, weight = 1)

	def _createSearchBar(self):
		# Text Entry:	
		self.searchBar = Entry(self, textvariable=self.text)
		
		##{CMC_BINDINGS}
		# Event callbacks and binding:
		self.searchBar.bind('<KeyRelease>', 	 self._callback)		
		self.searchBar.bind('<KeyPress-Escape>', self._callbackClearAll)
		self.searchBar.bind('<KeyPress-Delete>', self._callbackClearAll)
		
		# Apply to widget to parent:
		self.searchBar.grid(row		= 0,
							column	= 0,
							sticky	= tkSticky.fill)
	
	def _createCancelButton(self):
		# Main action when the cancel button is pressed:
		def handler(): 
			self.text.set('')
			self.callback(self)
#			self.searchBar.focus_set()
		
		# Cancel Button, not in focus routing:
		
		# Save a reference to the image on the button:
		self.cancelImage = Icon.cancel()
#		self.cancelButton = Button(self, image=self.cancelImage, command=handler, width=2)
		self.cancelButton = Button(self, image=self.cancelImage, command=handler)
		
				
		# Apply to widget to parent:
		self.cancelButton.grid(row	  = 0,
							   column = 1,
							   stick  = tkSticky.fill)
	
	def _callbackClearAll(self, event):
		self.cancelButton.invoke()
		
	def _callback(self, event):
		self.callback(self)
			
	def setCallback(self, callbackFunc):
		self.callback = callbackFunc
	
	def _configureForDebug(self):
		# Add a panel grip thingy here
		self.grid(sticky=tkSticky.fill)   
		self.config(height=50, width=300)
		self.grid_propagate(0)
		
		top = self.winfo_toplevel()
		top.title('SearchBar')
		
		self.sizeGrip = Sizegrip(self)
		self.sizeGrip.grid()
		
		top.rowconfigure(		0, weight = 1)
		top.columnconfigure(	0, weight = 1)
		
		self.rowconfigure(		0, weight = 1)
		self.columnconfigure(	0, weight = 1)
		self.rowconfigure(		1, weight = 1)
		self.columnconfigure(	1, weight = 1)
	
				



class SearchView(Frame):
	def __init__(self, master, *args, **kw):
		super().__init__(master, *args, **kw)
		# Configure Widget:
		self.grid_propagate(0)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)
		self.grid(sticky=tkSticky.fill)
		
		# Create Subwidgets:
		self.treeview = Treeview(self)
		self.searchbar = SearchBar(self)
		self.treeview.grid(row=1, sticky=tkSticky.fill)
		self.searchbar.grid(row=0, sticky=tkSticky.fill)





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
		self.bind(Notebook.event_tab_changed, self.tabChanged)
		
		
		
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



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  			  *********** VIEW ***********			       ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# MainApplication Class:
#   Main GUI class for the Columbus replacement (name = TBD)
#
# Usage:
#   One instance will 
#
# Things I've learned...
# 	The various parts of the GUI window need to be made into 
#	widgets so that they may be tested indepentantly of each other.
#
# 	Those widgets can then be assembled into a larger component
#	more easily and portably.
#
#	Data types fed to the UI widgets must be kept very generic,
#	otherwise interfacing gets awkward really quick outside of the
#	original scope.
#
# Widgets to make:
#	JobBrowser(TreeView) -> linked list data source
#	FileBrowser(TreeView) -> linked list data source
#	FileBrowser(filedialog)
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# this is a one-shot does all class which needs to be broken into pieces


# Application class template:
class MainApplication(Frame):   
	not_assigned = 'not assigned' # This should be = None

	# Column Layout:
	JobBrowserColumn = 0
	ResizeBarColumn = JobBrowserColumn + 1  
	FileBrowserColumn = ResizeBarColumn + 1 
	DataDisplayColumn = FileBrowserColumn
	SizeGripColumn = JobBrowserColumn
	StatusBarColumn = JobBrowserColumn
	JobBrowserSearchBarColumn = JobBrowserColumn
	
	# Row Layout:
	JobBrowserRow = 1
	JobBrowserSearchBarRow = JobBrowserRow - 1
	FileBrowserRow = JobBrowserRow
	ResizeBarRow = JobBrowserRow + 1
	DataDisplayRow = ResizeBarRow + 1
	SizeGripRow = JobBrowserRow + 3
	StatusBarRow = SizeGripRow
	
	# Span Layout
	JobBrowserRowSpan = 2
	StatusBarColumnSpan = 2
	

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.JobBrowserDelegate = None
		self.FileBrowserDelegate = None
	
		self._configureWindow()
		self._createWidgets()						   
	
	def setDelegate(self, JobBrowser = not_assigned, FileBrowser = not_assigned):
		'''
		if self.JobBrowserDelegate == MainApplication.not_assigned:
			pass
		else:
			self.JobBrowserDelegate = JobBrowser#Delegate()
		
		if not(self.FileBrowserDelegate == MainApplication.not_assigned):
			self.FileBrowserDelegate = FileBrowser#Delegate()
		'''
		self.JobBrowserDelegate = JobBrowser#Delegate()
		self.JobBrowserSearchBar.config(textvariable=self.JobBrowserDelegate.SearchBarText)
		
		self.FileBrowserDelegate = FileBrowser#Delegate()
		
		self.JobBrowserDelegate.setFileBrowserDelegate(self.FileBrowserDelegate)
		self.JobBrowserDelegate.finish__init__()
		self.FileBrowserDelegate.finish__init__()
	
	def doThis(self):
		print('Impliment this Event')
	
	def _configureWindow(self):
		# self.someCallToRetrieveLastSessionWindowSizeAndLocation()
		# Add a panel grip thingy here
		self.grid(sticky=tkSticky.fill)   
		self.config(height=900, width=1200)
		self.grid_propagate(0)
		top = self.winfo_toplevel()
		top.title('CMColumbus' + ' ' + os.getcwd())
		#self.sizeGrip = Sizegrip(self)
		#self.sizeGrip.grid()
		'''
		This is probably where I should use a for-loop to set the default
		behavior to stretchy and then adjust as-needed:
		'''
		top.rowconfigure(		0, weight = 1)
		top.columnconfigure(	0, weight = 1)
		top.columnconfigure(	1, weight = 0)
		self.rowconfigure(		0, weight = 1)
		self.columnconfigure(	0, weight = 1)
		self.columnconfigure(	1, weight = 0)
		
	
	def _createWidgets(self):
		self._createMainMenu()
		self._createIconMenu()
		self._createJobTabs()
		
		self._createMainPane()
		self._createSubPane()
		#self._createPanedWindow()
		self._createJobBrowser()
		self._createFileBrowser()
		self._createFileDataDisplay()
		self._createJobBrowserSearchBar()
		
		self._createSizeGrip()
	
	def _createMainPane(self):
		self.MainPane = PanedWindow(self, orient=tk.HORIZONTAL)
		#self.MainPane.add(Button(self, text='Pane 1'), weight=1)
		#self.MainPane.add(Button(self, text='Pane 2'), weight=3)
		#self.MainPane.pane(0)['weight'] = 3000
		#print(self.MainPane.pane(0))
		self.MainPane.grid(row=1, column=0, sticky=tkSticky.fill)
	
	def _createSubPane(self):
		self.SubPane = PanedWindow(self.MainPane, orient=tk.VERTICAL)
		self.MainPane.add(self.SubPane)
	
	def _createPanedWindow(self):
		self.PanedWindow = Panedwindow(self, orient = tk.HORIZONTAL)
		self.PanedWindow.grid(row = 1, column = 0, stick=tkSticky.fill)
			
	
	
		
	def _createSizeGrip(self):
		self.SizeGrip = Sizegrip(self)
		self.SizeGrip.grid(row=MainApplication.SizeGripRow, 
							column=MainApplication.SizeGripColumn,
							sticky=tkSticky.right)	
	
	def _createMainMenu(self):
		# Create the usual windows menus here
		pass
		
	def _createIconMenu(self):
		self.rowconfigure(0, minsize=25, weight=0)
		self.rowconfigure(1, weight=1)
		# This is where the 'Open in Explorer' icon thingy goes
		self.iconMenuFrame = Frame(self)
		self.iconMenuFrame.grid_propagate(0)
		#self.iconMenuFrame.config(height=30)
		
		self.iconMenuFrame.grid(row=0, column=0, columnspan=2, 
								sticky=tkSticky.fill, 
								ipadx=5, ipady=5)
		Button(self.iconMenuFrame, text='hi' ).grid(row=0, column=0) #''',command=self.ext_test'''
		Button(self.iconMenuFrame, text='lo').grid(row=0, column=2)
		
	
	def _createJobTabs(self):
		# This is where a Notebook is created and instances of the 
		# MainBrowser are added... or just one is re-shown with 
		# diffent data.
		pass
		
	def _createSeparator(self):
		self.VertResizeBar = Separator(self, orient = tk.VERTICAL)
		self.VertResizeBar.grid(
			row	 	= MainApplication.JobBrowserRow,
			rowspan	= MainApplication.JobBrowserRowSpan,
			column	= MainApplication.ResizeBarColumn,
			sticky	= tkSticky.vertical)

	def JobBrowserSearchBarHandler(self, event):
			self.JobBrowserDelegate.searchBarFilter(event)
	
	def _createJobBrowserSearchBar(self):
		
		self.JobBrowserSearchBar = Entry(self.JobBrowserFrame)
		self.JobBrowserSearchBar.bind(tkEvent.key_up, self.JobBrowserSearchBarHandler)

		self.JobBrowserSearchBar.grid(row=MainApplication.JobBrowserSearchBarRow,
									  column=MainApplication.JobBrowserSearchBarColumn,
									  sticky=tkSticky.fill)
		self._createJobBrowserSearchBarCancelButton()
	
	def _createJobBrowserSearchBarCancelButton(self):
		def handler():
			self.JobBrowserDelegate.searchBarButtonClicked()
		self.JobBrowserSearchBarCancelButton = Button(self.JobBrowserFrame,
													  text='X',
													  command=handler,
													  width=2)
		self.JobBrowserSearchBarCancelButton.grid(
				row=MainApplication.JobBrowserSearchBarRow,
				column=MainApplication.JobBrowserSearchBarColumn + 1,
				stick=tkSticky.fill)
																 
	
	def _createJobBrowser(self):
		# This is a TreeView that is populated by the 'Current Projects.cds'
		# -> Expands to show the Psuedo Directories and actual Directories via All Files:
		'''
		self.JobBrowserFrame = Frame(self)
		self.JobBrowserFrame.grid(
				row	 = MainApplication.JobBrowserRow,
				column  = MainApplication.JobBrowserColumn,
				rowspan = MainApplication.JobBrowserRowSpan, 
				sticky  = tkSticky.fill)
		'''
		self.JobBrowserFrame = Frame(self.MainPane, )
		self.MainPane.insert(0, self.JobBrowserFrame, weight = 0)
		self.JobBrowserFrame.grid_propagate(0)
		self.JobBrowserFrame.config(width = 250)
		
		self.JobBrowserFrame.rowconfigure( MainApplication.JobBrowserRow, 
				weight = 1)
		self.JobBrowserFrame.columnconfigure( MainApplication.JobBrowserColumn, 
				weight = 1)
		
		self.JobBrowser = Treeview(self.JobBrowserFrame, 
								   selectmode='browse', 
								   columns=('JobName'), )
		#self.MainPane.insert(0, self.JobBrowser, weight = 0)
		#self.JobBrowser.grid(row=0, column=0, sticky=tkSticky.fill)
		self.JobBrowser.grid(row=MainApplication.JobBrowserRow,
							 column=MainApplication.JobBrowserColumn,
							 sticky=tkSticky.fill, 
							 columnspan=2)
		self.columnconfigure(0, minsize=80)
		self.JobBrowser.column('#0', width=2000, stretch=False)
		
		
		# Event Handler and Bindings:
		def handler(event):
			self.JobBrowserDelegate.onSelection(event)
			
		self.JobBrowser.bind(Treeview.event_select, handler)
		
		
		
	def _createFileBrowser(self):
		# This is a custom entry window or something that is populated by the 
		# associated folder(s) and file type(s) from the JobBrowser and 'Project.cds'
		# -> This will be a TreeView that doesn't expand, it just has multiple columns
		#
		#   self.callToReadLastSession'sSettingsForColumnSizing
		#   if [lastLine] = None:
		#	   useDefaultValues
		#   else:
		#	   useLastSession'sValues
		#
		'''
		self.FileBrowserFrame = Frame(self)
		self.FileBrowserFrame.grid(
				row	 = MainApplication.FileBrowserRow, 
				column  = MainApplication.FileBrowserColumn, 
				sticky  = tkSticky.fill)
		'''
		self.FileBrowserFrame = Frame(self.SubPane)
		self.SubPane.add(self.FileBrowserFrame, weight = 1)
		self.FileBrowserFrame.rowconfigure(0, weight = 1)
		self.FileBrowserFrame.columnconfigure(0, weight = 1)
				
		self.FileBrowser = Treeview(self.FileBrowserFrame, selectmode='extended')
		self.FileBrowser.grid(row=0,
							  column=0,
							  sticky=tkSticky.fill)
##		self.FileBrowser.grid(row=MainApplication.FileBrowserRow,
##							  column=MainApplication.FileBrowserRow,
##							  sticky=tkSticky.fill)
		
		self.FileBrowser.config(columns=('FileName', 'Status', 'Description'))
		self.FileBrowser.column('#0', width=20, stretch=False)
		self.FileBrowser.column('FileName', stretch=False, minwidth=50)
		self.FileBrowser.heading('FileName', text='File Name', command=self.doThis)
		
		
		# To be used in a for-loop: 
		#for i in range(0, 100):
		#   self.FileBrowser.insert('', 0, values=(('Rprt-%d.docx' % i), '2016-10-26', 'Test Document Properties'))
	
	def _createFileDataDisplay(self):
		# This is the thing that shows the 'Date Last Saved:' (etc) info
		self.DataDisplay = Button(self.SubPane, text='DataDisplay')
		self.SubPane.add(self.DataDisplay)
		#self.DataDisplay.grid(row=2, column=2, sticky=tkSticky.fill)
	



#p = MainApplication()
#p.mainloop()

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
	img = tk.Image("photo", file="icon_appicon.gif")
	root.tk.call('wm','iconphoto',root._w,img)



	root.iconify()
	root.update()
	root.deiconify()
	root.mainloop()





