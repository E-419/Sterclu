import os, sys, pathlib

## Standard tkinter import calls -> defaults to using themed Tkinter 
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser
from tkinter.ttk import *



import PIL 		

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  		  *********** Data Classes ***********  		   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Custom data storage classes:
class tkSticky(object):
	top         = 'n'
	left        = 'w'
	right       = 'e'
	bottom      = 's'
	vertical    = top + bottom
	horizontal  = left + right
	fill        = vertical + horizontal 


class tkKey(object):
	'''
	This class is a data container for all the .keysym's used in the Tkinter 
	framework.
	'''
	key_down   = 'KeyPress'
	key_up     = 'KeyRelease'

	control 		= 'Control'
	control_right 	= 'Control_R'
	control_left 	= 'Control_L'
	
	escape 		= 'Escape'
	delete 		= 'Delete'
	tab			= 'Tab'
	
	shift_right	= 'Shift_R'
	shift_left 	= 'Shift_L'
	
	alt			= 'Alt'
	alt_right	= 'Alt_R'
	alt_left	= 'Alt_L'


class _tkEvent(object):
	'''
	Event Binding: Passing event to Parent (Python 2.7)
	http://stackoverflow.com/questions/32771369/how-to-pass-an-event-to-parent-widget/32771893#32771893
	
	This method calls for the use of Bind Tags (.bindtags(tuple(object.ref)))
	'''

	def __add__(self, other):
		return str(self) + '-' + str(other)

	def __iadd__(self, other):
		return tkEvent.__add__(self, other)

	def __str__(self):
		return self.value

	def __init__(self, *args):
		self.value = args[0]
		for itm in args[1:]:
			self.value = self + itm
			
	def keysym(self):
		sym_L = '<'
		sym_R = '>'
		return sym_L + str(self) + sym_R
	
	def control(*args):
		return _tkEvent(tkKey.control, tkKey.key_down, *args)

	def control_shift(*args):
		pass




class tkEvent(_tkEvent):
	class key(object):
		escape 		= _tkEvent(tkKey.escape).keysym()
		delete 		= _tkEvent(tkKey.delete).keysym()

	# Common Event Sequences:
	key_down   	= _tkEvent(tkKey.key_down).keysym()
	key_up     	= _tkEvent(tkKey.key_up).keysym()
	

	# Compound Event Sequences:
	# copy		= _tkEvent(tkKey.control, tkKey.key_down, 'c').keysym()
	copy		= _tkEvent.control('c').keysym()
	cut 		= _tkEvent.control('v').keysym()
	cut 		= _tkEvent(tkKey.control, tkKey.key_down, 'x').keysym()
	paste 		= _tkEvent(tkKey.control, tkKey.key_down, 'v').keysym()
	find		= _tkEvent(tkKey.control, tkKey.key_down, 'f').keysym()
	
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
##  	   *********** Tkinter Extensions ***********  		   ##
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == '__main__':
# 	from tkExt import *
# else:
	if 'src' in os.getcwd():
		from tkExt import *
	else:
		from src.tkExt import *

	t = tkEvent(tkKey.key_down, 'C')

	copy = tkEvent(tkKey.control , t)
	t += 'beta'
	print('',
		t,'\n', 
		copy.keysym(),'\n', 
		tkEvent.paste,'\n',
		tkEvent.copy)






























