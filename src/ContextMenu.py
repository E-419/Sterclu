import os
if 'src' in os.getcwd():
	from tkExt import *

else:
	from src.tkExt import *

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

					






