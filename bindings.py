'''self.bind("<Double-Button-1>",self.handle_double_click) 
        self.bind("<Control-Button-1>", self.handle_left_ctrl_click) 
        self.bind("<Shift-Button-1>", self.handle_left_shift_click) 
        self.bind("<ButtonRelease-1>", self.handle_left_release) 
        if self.ostyp=='mac': 
            #For mac we bind Shift, left-click to right click 
            self.bind("<Button-2>", self.handle_right_click) 
            self.bind('<Shift-Button-1>',self.handle_right_click) 
        else: 
            self.bind("<Button-3>", self.handle_right_click) 
        self.bind('<B1-Motion>', self.handle_mouse_drag) 
        self.bind('<Motion>', self.handle_motion) 
        self.bind_all("<Control-x>", self.deleteRow) 
        self.bind_all("<Control-n>", self.addRow) 
        self.bind_all("<Delete>", self.clearData) 
        self.bind_all("<Control-v>", self.paste) 
          #if not hasattr(self,'parentapp'): 
          #    self.parentapp = self.parentframe 
        self.parentframe.master.bind_all("<Right>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<Left>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<Up>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<Down>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<KP_8>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<Return>", self.handle_arrow_keys) 
        self.parentframe.master.bind_all("<Tab>", self.handle_arrow_keys) 
          #if 'windows' in self.platform: 
        self.bind("<MouseWheel>", self.mouse_wheel) 
        self.bind('<Button-4>', self.mouse_wheel) 
        self.bind('<Button-5>', self.mouse_wheel) 
        self.focus_set() '''