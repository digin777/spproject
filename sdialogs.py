from tkinter import *
from tkinter import simpledialog

class enwavedialog(simpledialog.Dialog):
	def body(self, master):
		self.enwavedict=None
		Label(master, text="angle of Encounter (degree) :").grid(row=0)
		Label(master, text="Velocity (m/s):").grid(row=1)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		return self.e1
		
	def apply(self):
			try:
				angle = float(self.e1.get())
				velocity = float(self.e2.get())
				self.enwavedict={"angle":angle,"velocity":velocity}
			except:
				messagebox.showerror("Error", "Provide valid inputs")
				
class wavedialog(simpledialog.Dialog):
	def body(self, master):
		self.wavedict=None
		Label(master, text="Alpha:").grid(row=0)
		Label(master, text="Wave Height:").grid(row=1)
		Label(master, text="spectral peak period:").grid(row=2)
		Label(master, text="peakiness parameter:").grid(row=3)
		Label(master, text="sigma a:").grid(row=4)
		Label(master, text="sigma b:").grid(row=5)
		self.e1 = Entry(master)
		self.e2 = Entry(master)
		self.e3 = Entry(master)
		self.e4 = Entry(master)
		self.e5 = Entry(master)
		self.e6 = Entry(master)
		self.e1.grid(row=0, column=1)
		self.e2.grid(row=1, column=1)
		self.e3.grid(row=2, column=1)
		self.e4.grid(row=3, column=1)
		self.e5.grid(row=4, column=1)
		self.e6.grid(row=5, column=1)
		return self.e1 # initial focus
	
	'''def validate(self):
		try:
			 float(self.e1.get())
			 float(self.e2.get())
			 float(self.e3.get())
			 float(self.e4.get())
			 float(self.e5.get())
			 float(self.e6.get())
		except:
			messagebox.showerror("Error", "Provide valid inputs")
		'''	
	def apply(self):
		try:
			alpha = float(self.e1.get())
			hs = float(self.e2.get())
			tp=float(self.e3.get())
			gama=float(self.e4.get())
			sigma_a=float(self.e5.get())
			sigma_b=float(self.e6.get())
			self.wavedict={"alpha":alpha,"hs":hs,"tp":tp,"gama":gama,"sigma_a":sigma_a,"sigma_b":sigma_b}
		except:
			messagebox.showerror("Error", "Provide valid inputs")
class about(simpledialog.Dialog):
	def body(self, master):
		Label(master, text="Spectral Analyzer").grid(row=0)
		Label(master, text="version : 1.0").grid(row=1)
		Label(master, text="Developer : DSP software foundation").grid(row=2)