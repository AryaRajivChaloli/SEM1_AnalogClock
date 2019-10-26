
#importing the files:

from datetime import timedelta,datetime
from math import sin, cos, pi
from tkinter import *

#defining the classes:

class find_coords:
	def __init__(self,world,viewport):
		x_min,y_min,x_max,y_max	= world
		X_min,Y_min,X_max,Y_max	= viewport
		self.delta		= min((X_max-X_min)/(x_max-x_min),(Y_max-Y_min)/(y_max-y_min))
		x_c,y_c			= 0.5*(x_min+x_max),0.5*(y_min+y_max)
		X_c,Y_c			= 0.5*(X_min+X_max),0.5*(Y_min+Y_max)
		self.c_1		= X_c-self.delta*x_c
		self.c_2		= Y_c-self.delta*y_c
	def change(self,x,y):
		X_new,Y_new		= (self.delta*x+self.c_1),(self.delta*(-y)+self.c_2)
		return X_new,Y_new
	def coords(self,x1,y1,x2,y2):
		return self.change(x1,y1),self.change(x2,y2)

class make_clock:
	def __init__(self,root,time_gap=0,w=500,h=650):
		self.def_world		= [-1,-1,1,1.5]
		self.bg_color_analog	= 'black'
		self.bg_color_digital	= 'grey'
		self.font_digital	= 'Harrington 20'
		self.align_digital	= 'center'
		self.needle_color	= 'light blue'
		self.month_color	= 'red'
		self.circle_color	= 'blue'
		self.circle_size	= 0.05
		self.len_hrs		= 0.50
		self.len_min		= 0.80
		self.len_sec		= 0.90
		self.root		= root
		width,height		= w,h
		self.gap		= min(width,height)/16
		self.width_hrs		= (self.gap-10)/3
		self.width_min		= (self.gap-10)/6
		self.time_gap		= timedelta(hours = time_gap)
		viewport		= (self.gap,self.gap,width-self.gap,height-25)
		self.convert		= find_coords(self.def_world,viewport)
		self.frame		= Frame(root,background=self.bg_color_analog)
		self.canvas		= Canvas(self.frame,width=width,height=height,background=self.bg_color_analog)
		self.frame.pack(fill=BOTH,expand=True)
		self.canvas.pack(fill=BOTH,expand=True)
		self.canvas.bind("<Configure>",self.resize)
		self.action()
	def resize(self,event):
		self.canvas.delete(ALL)
		width,height		= self.canvas.winfo_width(),self.canvas.winfo_height()
		self.gap		= min(width,height)/16
		viewport		= (self.gap,self.gap,width-self.gap,height-self.gap)
		self.convert		= find_coords(self.def_world,viewport)
	def action(self):
		self.create()
		self.root.after(500,self.action)
	def create(self):
		self.canvas.delete(ALL)
		year,month,date,*extra = datetime.timetuple(datetime.utcnow()-self.time_gap)
		month_list		= ['Jan','Febr','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
		month_name		= month_list[month-1]
		start,step		= pi/2,pi/6
		for i in range(12):
			angle		= start-(i*step)
			x_coord,y_coord	= cos(angle),sin(angle)
			if i==month or (i+12)==month:
				self.create_circle(x_coord,y_coord,True)
				self.canvas.create_text(self.convert.change(x_coord,y_coord-2*self.circle_size),fill="white",text=' '.join([str(date),month_name,str(year)]),font='Calibri 11')
			else:
				self.create_circle(x_coord,y_coord)
		self.create_needles()
		self.create_circle(0,0)
	def create_circle(self,x,y,ismonth=False):
		radius			= self.circle_size/2.0
		draw_point		= self.canvas.create_oval
		if ismonth:
			draw_point(self.convert.coords(x-radius,y-radius,x+radius,y+radius),fill=self.month_color)
			
		else:
			draw_point(self.convert.coords(x-radius,y-radius,x+radius,y+radius),fill=self.circle_color)
	def create_needles(self):
		year,month,date,hrs,min,sec,*extra = datetime.timetuple(datetime.utcnow()-self.time_gap)
		angle			= (pi/2)-(pi/6)*(hrs+(min/60.0))
		x_hrs,y_hrs		= cos(angle)*self.len_hrs,sin(angle)*self.len_hrs
		angle			= (pi/2)-(pi/30)*(min+(sec/60.0))
		x_min,y_min		= cos(angle)*self.len_min,sin(angle)*self.len_min
		angle			= (pi/2)-(pi/30)*sec
		x_sec,y_sec		= cos(angle)*self.len_sec,sin(angle)*self.len_sec
		month_list		= ['January','February','March','April','May','June','July','August','September','October','November','December']
		month_name		= month_list[month-1]
		time_display		= '%02i : %02i : %02i'%(hrs,min,sec)
		date_display		= ' '.join([str(date),month_name,str(year)])
		digital_time		= time_display+"\n"+date_display
		draw_line		= self.canvas.create_line
		self.root.title(time_display)
		draw_line(self.convert.coords(0,0,x_hrs,y_hrs),fill=self.needle_color,width=self.width_hrs)
		draw_line(self.convert.coords(0,0,x_min,y_min),fill=self.needle_color,width=self.width_min)
		draw_line(self.convert.coords(0,0,x_sec,y_sec),fill=self.needle_color,arrow='last')
		self.canvas.create_text(self.convert.change(0,-1.4),fill="white",text="     "+digital_time,font=self.font_digital)
		


#program:

time_gap = -5.5
w = h = 500
root = Tk()
make_clock(root,time_gap)
root.mainloop()