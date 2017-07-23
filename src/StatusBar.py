import os
if 'src' in os.getcwd():
	from tkExt import *

else:
	from src.tkExt import *

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

