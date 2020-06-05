import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from table import *
from lib.spectrum import johnswapspectrum
from tkinter.filedialog import asksaveasfile,askopenfile
from sdialogs import *
import pandas as pd
from Interpolation import *
class main_window(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master=master
		self.pack(fill="both",expand=True)
		self.add_widgets()
		
	def Generate_wavespectrum(self):
		dialog=wavedialog(self.master)
		if dialog.wavedict:
			self.spectrum=johnswapspectrum(dialog.wavedict["alpha"],dialog.wavedict["hs"],dialog.wavedict["tp"],dialog.wavedict["gama"],dialog.wavedict["sigma_a"],dialog.wavedict["sigma_b"])
			self.spectrum.set_omega_z()
			df=self.table.data.copy()
			df["T"]=df.apply(lambda x:self.spectrum.c_T(x['w']),axis=1)
			df["sig"]=df.apply(lambda x:self.spectrum.c_sigma(x['w']),axis=1)
			df['sw']=df.apply(lambda x:self.spectrum.c_somega(x['w'],x["sig"]),axis=1)
			self.table.update_column(df["T"])
			self.table.update_column(df["sig"])
			self.table.update_column(df['sw'])
		else:
			messagebox.showinfo("Info", "Unable to generate wave spectrum")
			
	def about(self)	:
		about_dialog=about(self.master)
		
	def plot_wavespectrum(self):
		df=self.table.data.copy()
		if "sw" in list(df.columns):
			plotwave=plotwindow(self.master,x=df["w"],y=df["sw"])
		else:
			messagebox.showerror("Error","Generate wave Spectra first")
		
	def plot_Encounterspectrum(self):
		df=self.table.data.copy()
		if "swe" in list(df.columns):
			plotwave=plotwindow(self.master,x=df["we"],y=df["swe"])
		else:
			messagebox.showerror("Error","Generate Encounter Spectra first")	
	def Generate_responsespectrum(self):
		df=self.table.data.copy()
		x,y=interpolation(df['we'],df['swe'],len(df['we'])-2)
		df['inter we']=pd.Series(x)
		df['inter swe']=pd.Series(y)
		self.table.update_column(df['inter we'])
		self.table.update_column(df['inter swe'])
	
	def Generate_encounterspectrum(self):
		df=self.table.data.copy()
		try:
			df["sw"]
		except:
			messagebox.showinfo("Info", "Compute Wave Spectrum before doing Encounter Spectrum")
			return
		dialog=enwavedialog(self.master)
		if dialog.enwavedict:
			angle=dialog.enwavedict["angle"]
			if angle>360:
				messagebox.showerror("Error","angle of encounter canot be garter than 360")
				return
			velocity=dialog.enwavedict["velocity"]
			df['we']=df.apply(lambda x:self.spectrum.e_omega(x['w'],velocity,angle),axis=1)
			df['swe']=df.apply(lambda x:self.spectrum.c_somega_e(x['sw'],x['we'],velocity,angle),axis=1)
			self.table.update_column(df["we"])
			self.table.update_column(df["swe"])
		else:
			messagebox.showinfo("Info", "Unable to generate Encounter spectrum")
	
	def Exit(self):
		import sys
		sys.exit()
		
	def Exports_csv(self):
		filetypes =[('Coma separated values', 'csv')]
		file_name=asksaveasfile(mode='w', defaultextension=".csv")
		if file_name is None: 
			return
		self.table.data.to_csv(file_name,index=False,sep=",",line_terminator='\n',encoding='utf-8')
		
	def Open(self):
		filetypes =[('Coma separated values', 'csv')]
		file_name=askopenfile(mode='r', defaultextension=".csv")
		if file_name is None: 
			return
		self.table.destroy()
		self.table=table(self,pd.read_csv(file_name))
		
	def add_widgets(self):
		self.table=table(self,data=pd.DataFrame({'w':[""]}))
		self.menubar=Menu(self.master)
		self.filemenu=Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Open",command=self.Open)
		self.filemenu.add_command(label="Exports as csv",command=self.Exports_csv)
		self.filemenu.add_command(label="Exit",command=self.Exit)
		self.spectmenu = Menu(self.menubar, tearoff=0)
		self.spectmenu.add_command(label="Generate wave spectrum",command=self.Generate_wavespectrum)
		self.spectmenu.add_command(label="Generate Encounter spectrum",command=self.Generate_encounterspectrum)
		self.spectmenu.add_command(label="Generate Response spectrum",command=self.Generate_responsespectrum)
		self.plot=Menu(self.menubar,tearoff=0)
		self.plot.add_command(label="plot Wave spectrum",command=self.plot_wavespectrum)
		self.plot.add_command(label="plot Encounter spectrum",command=self.plot_Encounterspectrum)
		self.help=Menu(self.menubar,tearoff=0)
		self.help.add_command(label="about",command=self.about)
		self.spectmenu.add_separator()
		self.menubar.add_cascade(label="File", menu=self.filemenu)
		self.menubar.add_cascade(label="Spectrum", menu=self.spectmenu)
		self.menubar.add_cascade(label="Plot", menu=self.plot)
		self.menubar.add_cascade(label="Help", menu=self.help)
		self.master.config(menu=self.menubar)
		
if __name__=='__main__':
	root=Tk()
	root.geometry("700x500")
	root.title("Spectral analyzer")
	photo = PhotoImage(file = "D:\\S6 MCA\\Main_project_siva_and_prasanth\\resorces\\icons\\ship_x.png")
	root.iconphoto(True, photo)
	app=main_window(master=root)
	app.mainloop() 