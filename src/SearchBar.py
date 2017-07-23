import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
# if __name__ == '__main__':
# 	from tkBase import *
# 	from AutoScrollBar import AutoScrollbar
# 	from Icon import Icon
# else:
if 'src' in os.getcwd():
	from tkBase import *
	from AutoScrollBar import AutoScrollbar
	from Icon import Icon
else:
	from src.tkBase import *
	from src.AutoScrollBar import AutoScrollbar
	from src.Icon import Icon



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
		# self.searchBar.bind('<KeyRelease>', 	 self._callback)		
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
			# self.callback(self)
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
			
	def setCallback(self, callbackFunc = None):
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
	
