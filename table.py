from tkinter import *
import pandas as pd
import numpy as np
class TbEntry(Entry):
	def __init__(self,master=None,id=None):
		super().__init__(master)
		self.id=id
		self.master=master
		self.master.selected_items=[]
		self.dobindings()
		self.flag=1
		
	def dobindings(self): 
		self.bind("<Button-1>",self.handle_left_click) 
		self.bind("<Double-Button-1>",self.handle_double_click) 
		self.bind("<Key-Return>",self.handle_Enter)
		self.bind("<Key>",self.handle_enykey)
		self.bind("<FocusOut>",self.handle_focusout)
		self.bind('<B1-Motion>', self.handle_leftdrag)
		self.bind('<Motion>', self.handle_motion)
		self.bind('<Control-Button-1>',self.handle_multiselection) 
		
	def handle_double_click(self,event):
		self['state']=NORMAL
		print(self.id)
	def handle_left_click(self,event):
		if self.flag:
			self.old_value=self.get()
			self.flag=None
			
	def handle_Enter(self,event):
		self.flag=1
		if self.old_value!=self.get():
			self.old_value=self.get()
			try:
				float(self.get())
			except:
				messagebox.showerror("Error", "Provide valid inputs")
				return
			try:
				self.master.master.master.tb_dict[str(int(self.id.split(",")[0])+1)+","+str(0)]
			except:
				if self.master.master.master.no_rows!=1:
					self.master.master.master.data=self.master.master.master.data.append(pd.Series(),ignore_index=True)
				self.master.master.master.add_row({k:"" for k in self.master.master.master.data.columns})
			self.master.master.master.data[self.master.master.master.data.columns[int(self.id.split(",")[1])]][int(self.id.split(",")[0])]=float(self.old_value)
	def handle_enykey(self,event):
		pass
		
	def handle_leftdrag(self,event):
		pass
		
	def handle_motion(self,event):
		pass
		
	def handle_focusout(self,event):
		self.flag=1
		if self.old_value!=self.get():
			self.delete(0,END)
			self.insert(0,self.old_value)
			
	def handle_multiselection(self,event):
		if self.id not in self.master.selected_items:
			self.master.selected_items.append(self.id)
			self['bg']="yellow"
			#self['fg']='white'
			
class table(Frame):
	def __init__(self,master=None,data=None):
		super().__init__(master)
		#self.master.title("Table")
		if data is not None and isinstance(data,pd.DataFrame):
			self.data=data
		else: 
			self.data=pd.DataFrame()
		canvas = Canvas(self)
		scrollbary = Scrollbar(self, orient="vertical", command=canvas.yview)
		scrollbarx = Scrollbar(self, orient="horizontal", command=canvas.xview)
		self.scrollable_frame=Frame(canvas)
		self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            ))
		canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
		canvas.configure(yscrollcommand=scrollbary.set)
		canvas.configure(xscrollcommand=scrollbarx.set)
		scrollbarx.pack(side="bottom", fill="x")
		scrollbary.pack(side="right", fill="y")
		canvas.pack(side="left", fill="both",expand=True)
		self.tb_dict={}
		self.draw_table(self.data)
		self.pack(fill="both",expand=True)
		
	def draw_table(self,data):
		assert isinstance(data,pd.DataFrame), "it shoulbe a dataframe"
		self.no_rows,self.no_cols=data.shape
		for c in range(len(data.columns)):
			var=StringVar()
			x=Entry(self.scrollable_frame,fg="green",bg="black",cursor="arrow",justify="center",highlightcolor="green",font=('Arial',8,'bold'),state="readonly",textvariable=var)
			var.set(data.columns[c])
			x.grid(row=0,column=c)
		for r in range(self.no_rows):
			for c in range(self.no_cols):
				self.tb_dict[str(r)+","+str(c)]=(TbEntry(self.scrollable_frame,id=str(r)+","+str(c)),StringVar())
				self.tb_dict[str(r)+","+str(c)][0].textvariable=self.tb_dict[str(r)+","+str(c)][1]
				self.tb_dict[str(r)+","+str(c)][1].set(str(data.iloc[r][data.columns[c]]))
				self.tb_dict[str(r)+","+str(c)][0].insert(0,str(data.iloc[r][data.columns[c]]))
				self.tb_dict[str(r)+","+str(c)][0].grid(row=(r+1),column=c)
		if self.no_rows==0:
			self.add_row(data)
				
	def add_row(self,data):
		if type(data)==dict:
			data=pd.DataFrame({k: [v] for k, v in data.items()})
		if(self.no_rows==0):
			for c in range(len(data.columns)):
				var=StringVar()
				x=Entry(self.scrollable_frame,fg="green",bg="black",cursor="arrow",justify="center",highlightcolor="green",font=('Arial',8,'bold'),state="readonly",textvariable=var)
				var.set(data.columns[c])
				x.grid(row=0,column=c)
		r=self.no_rows
		for c in range(len(data.columns)):
			self.tb_dict[str(r)+","+str(c)]=(TbEntry(self.scrollable_frame,id=str(r)+","+str(c)),StringVar())
			self.tb_dict[str(r)+","+str(c)][0].textvariable=self.tb_dict[str(r)+","+str(c)][1]
			self.tb_dict[str(r)+","+str(c)][1].set(str(data.iloc[0][data.columns[c]]))
			self.tb_dict[str(r)+","+str(c)][0].insert(0,str(data.iloc[0][data.columns[c]]))
			self.tb_dict[str(r)+","+str(c)][0].grid(row=(r+1),column=c)
		self.no_rows+=1
		
	def add_column(self,data):
		assert isinstance(data,pd.core.series.Series),"It must be pandas Series"
		self.add_empty_column(data.name)
		c=self.no_cols-1
		ds=[i for i in data]
		for r in range(len(ds)):
			self.tb_dict[str(r)+","+str(c)][1].set(str(ds[r]))
			self.tb_dict[str(r)+","+str(c)][0].insert(0,ds[r])
			self.data[data.name][r]=ds[r]
			
	def update_column(self,data):
		assert isinstance(data,pd.core.series.Series),"It must be pandas Series"
		c=self.no_cols
		if data.name in self.data.columns:
			c_no=list(self.data.columns).index(data.name)
			#c_no+=1
			try:
				if type(self.tb_dict[str(0)+","+str(c_no)]) ==tuple:
					ds=[i for i in data]
					for r in range(len(ds)):
						self.tb_dict[str(r)+","+str(c_no)][1].set(str(ds[r]))
						self.tb_dict[str(r)+","+str(c_no)][0].delete(0,END)
						self.tb_dict[str(r)+","+str(c_no)][0].insert(0,ds[r])
						self.data[data.name][r]=ds[r]
			except Exception as e:
				pass
		else:
			self.add_column(data)
					
	def add_empty_column(self,column_name):
		c=self.no_cols
		self.no_cols+=1
		#c=self.no_cols
		var=StringVar()
		x=Entry(self.scrollable_frame,fg="green",bg="black",cursor="arrow",justify="center",highlightcolor="green",font=('Arial',8,'bold'),state="readonly",textvariable=var)
		var.set(column_name)
		x.grid(row=0,column=c)
		for r in range(self.no_rows):
			self.tb_dict[str(r)+","+str(c)]=(TbEntry(self.scrollable_frame,id=str(r)+","+str(c)),StringVar())
			self.tb_dict[str(r)+","+str(c)][0].textvariable=self.tb_dict[str(r)+","+str(c)][1]
			self.tb_dict[str(r)+","+str(c)][1].set(str(""))
			self.tb_dict[str(r)+","+str(c)][0].insert(0,"")
			self.tb_dict[str(r)+","+str(c)][0].grid(row=r+1,column=c)
		self.data[column_name] = self.data.apply(lambda _: '', axis=1)
	
	def get_tbdata(self):
		return self.data
		
	def set_tbdata(self,data):
		self.data=data
		
if __name__=='__main__':
	#s=pd.read_csv("D:\\S6 MCA\\Main_project_siva_and_prasanth\\data\\pddataf.csv")
	x="D:\\S6 MCA\\Main_project_siva_and_prasanth\\data\\fg.csv"
	#x="C:\\Users\\user\\Downloads\\hepatitis.csv"
	s=pd.read_csv(x)
	root=Tk()
	photo = PhotoImage(file = "D:\\S6 MCA\\Main_project_siva_and_prasanth\\resorces\\trend.png")
	root.iconphoto(False, photo)
	#root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='D:\S6 MCA\Main_project_siva_and_prasanth\resorces\trend.png'))
	a=table(master=root,data=s)
	a.add_row({'T':10,'w':11,'s':15,'a.g2.w-5':12,'-(w-w0)2':13,'2.s2w02':20,'f(g)':55,'f(w/w0)':36,'Sz(w)':45,'SM':23,'f[Sz(w)]':71})
	a.mainloop()