import tkinter as tk
from tkinter import *
from table import *
import pandas as pd
class main_window(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.pack(fill="both",expand=True)
		self.add_widgets()
	def add_widgets(self):
		self.table=table(self,data=pd.DataFrame({'W':[""],'T':[""],'sig':[""],'sw':[""]}))
		#self.table.add_row({'W':"",'T':"",'sig':"",'sw':""})
if __name__=='__main__':
	root=Tk()
	a=main_window(master=root)
	a.mainloop()