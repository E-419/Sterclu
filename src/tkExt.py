import os, sys, pathlib

# if __name__ == '__main__':
# 	from tkBase import *
# 	from ScrollView import ScrollView
# else:
if 'src' in os.getcwd():
	from tkBase import *
	from ScrollView import ScrollView
else:
	from src.tkBase import *
	from src.ScrollView import ScrollView

		

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
	
	selectmode_single = 'browse'
	selectmode_multi  = 'extended'
	selectmode_none   = 'none'
	
	id_region_none      = 'nothing'   # Point not in (functional part of) widget
	id_region_heading   = 'heading'   # Point in heading row
	id_region_separator = 'separator' # Point on separator, use with .identify_column() for the column to the left
	id_region_icon      = 'tree'      # Point is in the icon column of a row
	id_region_cell      = 'cell'      # Point is in a row, not in the icon column
	
	
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




