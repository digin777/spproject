import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from table import *
from lib.spectrum import johnswapspectrum
from sdialogs import *
import pandas as pd
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
			df["T"]=df.apply(lambda x:self.spectrum.c_T(x['W']),axis=1)
			df["sig"]=df.apply(lambda x:self.spectrum.c_sigma(x['W']),axis=1)
			df['sw']=df.apply(lambda x:self.spectrum.c_somega(x['W'],x["sig"]),axis=1)
			self.table.update_column(df["T"])
			self.table.update_column(df["sig"])
			self.table.update_column(df['sw'])
			#self.table.update_column(df['sw'])
			#self.table.update_column(self.table.data.apply(lambda x:self.spectrum.c_T(x['W']),axis=1))
		else:
			messagebox.showinfo("Info", "Unable to generate wave spectrum")
	def about(self)	:
		about_dialog=about(self.master)
	def plot_wavespectrum(self):
		df=self.table.data.copy()
		plotwave=plotwindow(self.master,x=df["W"],y=df["sw"])
	def plot_Encounterspectrum(self):
		df=self.table.data.copy()
		plotwave=plotwindow(self.master,x=df["we"],y=df["swe"])
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
			df['we']=df.apply(lambda x:self.spectrum.e_omega(x['W'],velocity,angle),axis=1)
			df['swe']=df.apply(lambda x:self.spectrum.c_somega_e(x['sw'],x['we'],velocity,angle),axis=1)
			self.table.update_column(df["we"])
			self.table.update_column(df["swe"])
		else:
			messagebox.showinfo("Info", "Unable to generate Encounter spectrum")
			
	def add_widgets(self):
		self.table=table(self,data=pd.DataFrame({'W':[""]}))
		self.menubar=Menu(self.master)
		self.filemenu = Menu(self.menubar, tearoff=0)
		self.filemenu.add_command(label="Generate wave spectrum",command=self.Generate_wavespectrum)
		self.filemenu.add_command(label="Generate Encounter spectrum",command=self.Generate_encounterspectrum)
		self.plot=Menu(self.menubar,tearoff=0)
		self.plot.add_command(label="plot Wave spectrum",command=self.plot_wavespectrum)
		self.plot.add_command(label="plot Encounter spectrum",command=self.plot_Encounterspectrum)
		self.help=Menu(self.menubar,tearoff=0)
		self.help.add_command(label="about",command=self.about)
		self.filemenu.add_separator()
		self.menubar.add_cascade(label="Spectrum", menu=self.filemenu)
		self.menubar.add_cascade(label="Plot", menu=self.plot)
		self.menubar.add_cascade(label="Help", menu=self.help)
		self.master.config(menu=self.menubar)
		

if __name__=='__main__':
	root=Tk()
	root.geometry("700x500")
	root.title("Spectral analyzer")
	app=main_window(master=root)
	app.mainloop() 