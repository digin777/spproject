from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
	def validate(self):
		try:
			angle = float(self.e1.get())
			velocity = float(self.e2.get())
			self.enwavedict={"angle":angle,"velocity":velocity}
			return 1
		except:
			messagebox.showerror("Error", "Provide valid inputs")
			
	def apply(self):
		pass
				
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
	
	def validate(self):
		try:
			alpha = float(self.e1.get())
			hs = float(self.e2.get())
			tp=float(self.e3.get())
			gama=float(self.e4.get())
			sigma_a=float(self.e5.get())
			sigma_b=float(self.e6.get())
			self.wavedict={"alpha":alpha,"hs":hs,"tp":tp,"gama":gama,"sigma_a":sigma_a,"sigma_b":sigma_b}
			return 1
		except:
			messagebox.showerror("Error", "Provide valid inputs")
		
	def apply(self):
		pass
		
class plotwindow(Toplevel):
	def __init__(self, master, title = None,x=None,y=None):
		Toplevel.__init__(self, master)
		self.x=x
		self.y=y
		self.transient(master)
		self.parent = master
		self.title(title)
		body = Frame(self)
		self.initial_focus = self.body(body)
		body.pack(padx=5, pady=5,fill=BOTH,expand=True)
		if not self.initial_focus:
			self.initial_focus = self
		self.wait_window(self)
		
	def graph_selected(self,event):
		graphtype=self.comboselectgraphtype.get()
		if graphtype=="Line":
			self.ax.clear()
			self.ax.plot(self.x,self.y)
		elif graphtype=="Scatter":
			self.ax.clear()
			self.ax.scatter(self.x, self.y,marker="o",cmap = 'YlGnBu')
		elif graphtype=="Bar":	
			self.ax.clear()
			self.ax.bar(self.x, self.y)
			
		if self.x.name=="we":
			self.ax.set(title = "Encounter Spectrum",
			xlabel = "Encounter Frequency (We)\n (rad/sec)",
			ylabel = "S(we)")
			self.fig.canvas.draw()
		elif self.x.name=="w":
			self.ax.set(title = "Wave Spectrum",
			xlabel = "Frequency (W)\n (rad/sec)",
			ylabel = "S(w)")
			self.fig.canvas.draw()
			
	def body(self, master):
		plt.ion()
		self.fig=plt.Figure(figsize=(10,6),dpi=100)
		self.ax=self.fig.add_subplot(111)
		self.ax.plot(self.x,self.y)
		if self.x.name=="we":
			self.ax.set(title = "Encounter Spectrum",
			xlabel = "Encounter Frequency (We)\n (rad/sec)",
			ylabel = "S(we)")
		elif self.x.name=="W":
			self.ax.set(title = "Wave Spectrum",
			xlabel = "Frequency (W)\n (rad/sec)",
			ylabel = "S(w)")
		chart=FigureCanvasTkAgg(self.fig,master)
		self.comboselectgraphtype= ttk.Combobox(master, 
                            values=[
                                    "Line", 
                                    "Scatter",
                                    "Bar"])
		self.comboselectgraphtype.pack(side=LEFT,fill="x")
		chart.get_tk_widget().pack(side=TOP)
		self.comboselectgraphtype.current(0)
		self.comboselectgraphtype.bind("<<ComboboxSelected>>", self.graph_selected)

class about(simpledialog.Dialog):
	def body(self, master):
		Label(master, text="Spectral Analyzer",justify="center",font=("Times New Roman", 12, "bold")).pack()
		Label(master, text="version : 1.0",justify="center").pack()
		Label(master, text="Developer : DSP software foundation",justify="center").pack()
	
	def buttonbox(self):
		box = Frame(self)
		w = Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
		w.pack(side=LEFT, padx=5, pady=5)
		self.bind("<Return>", self.ok)
		box.pack()
		
	def ok(self):
		self.withdraw()
		self.parent.focus_set()
		self.destroy()