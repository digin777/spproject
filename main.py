import tkinter as tk
from tkinter import *
from tkinter import simpledialog
from table import *
from lib.spectrum import johnswapspectrum
from lib.generate import *
from tkinter.filedialog import asksaveasfile,askopenfile
from sdialogs import *
from RAOparser import *
import pandas as pd
from interpolaton import *
import matplotlib.pyplot as plt
class main_window(Frame):
	def __init__(self,master=None):
		super().__init__(master)
		self.master=master
		self.pack(fill="both",expand=True)
		self.add_widgets()
		self.spectrum=johnswapspectrum()
		
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
			plotEncounter=plotwindow(self.master,x=df["we"],y=df["swe"])
		else:
			messagebox.showerror("Error","Generate Encounter Spectra first")	
			
	def plot_Responsespectrum(self):
		df=self.table.data.copy()
		if "Sr(we)" in list(df.columns):
			dfx=df[pd.to_numeric(df["new we"],errors="coerce").notnull()]
			dfy=df[pd.to_numeric(df["Sr(we)"],errors="coerce").notnull()]
			plotResponse=plotwindow(self.master,x=dfx["new we"].dropna(),y=dfy["Sr(we)"].dropna())
		else:
			messagebox.showerror("Error","Response spectrum Not Generated")

	def Generate_responsespectrum(self):
		df=self.table.data.copy()
		dialog=resdialog(self.master)
		if dialog.resdict:
			self.PRAO=dialog.resdict['PRAO']
			self.Mtype=dialog.resdict['Mtype']
			self.Msubtype=dialog.resdict['Msubtype']
		else:
			messagebox.showinfo("Info","Operation Aborted")
			return
		self.raoresult,maxfreq,minfreq=RAOparse(self.PRAO)
		interx,intery=interpolation(df['we'],df['swe'],len(df['we'])-2)
		newx=[]
		newy=[]
		for x in interx:#filter out we from interpolated result to match with the Rao result
			if x>=minfreq and x<=maxfreq:
				newx.append(x)
				newy.append(intery[interx.index(x)])
		motype=self.Mtype+self.Msubtype
		data=self.RAO_Common_ForEach_Motion(motype,newx,newy)
		self.res_data=data
		h=data["new we"][1]-data["new we"][0]
		self.result={
		"M0":str(h/3*self.res_data["F(A)"].sum()),
		"M1":str((h**2/3)*self.res_data["F(M1)"].sum()),
		"M2":str((h**3/3)*self.res_data["F(M2)"].sum()),
		"M4":str((h**5/3)*self.res_data["F(M4)"].sum())
		}

		
	def RAO_Common_ForEach_Motion(self,motype,newx,newy):
		try:
			if self.angle==None:
				self.angle=0
		except AttributeError:
			self.angle=0
		df=pd.DataFrame()
		raoy=list(self.raoresult[(self.raoresult.heading==self.angle)][motype])
		raox =list(self.raoresult[(self.raoresult.heading==self.angle)]['frequency'])
		df["RAO"]=np.interp(newx,raox,raoy)
		df["new we"]=newx
		df["swe"]=newy
		df["Sr(we)"]=df['swe']*(df["RAO"]**2)
		#self.table.destroy()
		#self.table=table(self,df)
		df["SM"]=pd.Series(generate(df.shape[0])).values
		df["F(A)"]=df["Sr(we)"]*df["SM"]
		df["L"]=pd.Series(range(0,df.shape[0]))
		if df["new we"][0]!=0:
			df["F(M1)"]=df["F(A)"]*df["L"]
			df["F(M2)"]=df["F(A)"]*(df["L"]**2)
			df["F(M4)"]=df["F(A)"]*(df["L"]**4)
		for column in df.columns:
			self.table.update_column(df[column])
		#plt.plot(df["new we"],df["Sr(we)"])
		#plt.show()
		return df

		
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
			self.angle=angle
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
		filetypes =[('Coma separated values', '*.csv'),('All Files','*.*')]
		file_name=asksaveasfile(mode='w', defaultextension=".csv",filetypes=filetypes)
		if file_name is None: 
			return
		self.table.data.to_csv(file_name,index=False,sep=",",line_terminator='\n',encoding='utf-8')
		
	def Open(self):
		filetypes =[('Coma separated values', '*.csv')]
		file_name=askopenfile(mode='r', defaultextension=".csv",filetypes =filetypes)
		if file_name is None: 
			return
		self.table.destroy()
		self.table=table(self,pd.read_csv(file_name))
		
	def view_result(self):
		try:
			result_view =view_reult(self.master,data=self.result)
		except AttributeError:
			return messagebox.showinfo("info","plese perform generate response spectrun")
		
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
		self.plot.add_command(label="plot Response spectrum",command=self.plot_Responsespectrum)
		self.view=Menu(self.menubar,tearoff=0)
		self.view.add_command(label="View Result",command=self.view_result)
		self.help=Menu(self.menubar,tearoff=0)
		self.help.add_command(label="about",command=self.about)
		self.spectmenu.add_separator()
		self.menubar.add_cascade(label="File", menu=self.filemenu)
		self.menubar.add_cascade(label="Spectrum", menu=self.spectmenu)
		self.menubar.add_cascade(label="View", menu=self.view)
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