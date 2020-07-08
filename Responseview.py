from table import *
import tkinter as tk
from tkinter import *
import pandas as pd
class resview(table):
	def __init__(self,master=None,data=None):
		super().__init__(master=master,data=data)
		self.master=master
if __name__=='__main__':
	x="D:\\S6 MCA\\Main_project_siva_and_prasanth\\data\\fg.csv"
	#x="C:\\Users\\user\\Downloads\\hepatitis.csv"
	s=pd.read_csv(x)
	root=Tk()
	a=resview(root,s)
	a.mainloop()