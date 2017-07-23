import os, sys, pathlib
# This import sequence requires the other modules to be in the same /src directory
# if __name__ == '__main__':
# 	from tkBase import *
# 	from SearchBar import SearchBar
# else:
if 'src' in os.getcwd():
	from tkExt import *
	from SearchBar import SearchBar
else:
	from src.tkExt import *
	from src.SearchBar import SearchBar


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

		
		# Bind additional keys between widgets:
		self.setBindings()
	
	def hideSearchBar(self):
		self.searchbar.grid_remove()

	def showSearchBar(self):
		self.searchbar.grid()

	def setBindings(self):
		def handler(event):
			self.searchbar.cancelButton.invoke()
		self.treeview.bind(tkEvent.key.escape, handler)

		find = tkEvent.find
		self.searchbar.bind(tkEvent)