import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from table import *
from lib.spectrum import johnswapspectrum
import pandas as pd

class wavedialog(simpledialog.Dialog):
	def body(self, master):
		Label(master, text="Alpha:").grid(row=0)
		Label(master, text="Wave Height:").grid(row=1)
		Label(master, text="spectral peak period:").grid(row=2)
		Label(master, text="Wave Height:").grid(row=3)
		Label(master, text="peakness parameter:").grid(row=4)
		Label(master, text="sigma a:").grid(row=5)
		Label(master, text="sigma b:").grid(row=6)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e6 = Entry(master)
		self.e7 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		self.e6.grid(row=5, column=1)
		self.e7.grid(row=6, column=1)
		return self.e1 # initial focus
	
	def validate(self):
		try:
			 float(self.e1.get())
			 float(self.e2.get())
			 float(self.e3.get())
			 float(self.e4.get())
			 float(self.e5.get())
			 float(self.e6.get())
		except:
			messagebox.showerror("Error", "Provide valid inputs")
		else:
			return
	def apply(self):
		first = self.e1.get()
		second = self.e2.get()
		print (first, second )

class main_window(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master=master
		self.pack(fill="both",expand=True)
		self.add_widgets()
	def Generate_wavespectrum(self):
		self.spectrum=johnswapspectrum()
		dialog=wavedialog(self.master)
	def add_widgets(self):
		self.table=table(self,data=pd.DataFrame({'W':[""]}))
		#self.table.add_empty_column("we")
		#self.table.add_column(pd.Series([10,20],name="ab") )
		self.menubar=Menu(self.master)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Generate wave spectrum",command=self.Generate_wavespectrum)
		self.filemenu.add_command(label="Generate Encounter spectrum")
		self.plot=Menu(self.menubar,tearoff=0)
		self.plot.add_command(label="plot Wave spectrum")
		self.plot.add_command(label="plot Encounter spectrum")
		self.filemenu.add_separator()
		self.menubar.add_cascade(label="Spectrum", menu=self.filemenu)
		self.menubar.add_cascade(label="Plot", menu=self.plot)
		self.master.config(menu=self.menubar)
		

if __name__=='__main__':
	root=Tk()
	a=main_window(master=root)
	a.mainloop() 