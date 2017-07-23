import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
if __name__ == '__main__':
	from tkBase import *
else:
	if 'src' in os.getcwd():
		from tkBase import *
	else:
		from src.tkBase import *
		

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

