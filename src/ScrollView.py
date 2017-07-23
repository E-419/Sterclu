import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
if __name__ == '__main__':
	from tkBase import *
	from AutoScrollBar import AutoScrollbar
else:
	if 'src' in os.getcwd():
		from tkBase import *
		from AutoScrollBar import AutoScrollbar
	else:
		from src.tkBase import *
		from src.AutoScrollBar import AutoScrollbar



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

