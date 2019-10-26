
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
	def __init__(self,root,time_gap=0,w=1000,h=650):
		self.def_world		= [-1,-1,1,1.5]
		self.bg_color_analog	= 'black'
		
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
		self.refresh_time	= 500
		self.text_color		= 'white'
		self.font_analog	= 'Calibri 11'
		self.gap		= min(width,height)/16
		self.width_hrs		= (self.gap-10)/3
		self.width_min		= (self.gap-10)/6
		self.time_gap		= timedelta(hours = time_gap)
		viewport		= (self.gap,self.gap,width-self.gap,height-25)
		self.convert		= find_coords(self.def_world,viewport)
		self.canvas		= Canvas(root,width=width,height=height,background=self.bg_color_analog)
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
		
		self.root.after(self.refresh_time,self.action)









	def create(self):
		self.canvas.delete(ALL)
		year,month,date,*extra 	= datetime.timetuple(datetime.utcnow()-self.time_gap)
		month_list		= ['Jan','Febr','Mar','Apr','May','Jun','Jul','Aug','Sept','Oct','Nov','Dec']
		month_name		= month_list[month-1]
		start,step		= pi/2,pi/6
		self.create1()
		self.create2()
		self.create3()
		for i in range(12):
			angle		= start-(i*step)
			x_coord,y_coord	= cos(angle),sin(angle)
			if i==month or (i+12)==month:
				self.canvas.create_text(self.convert.change(x_coord,y_coord),fill='red',text=' '.join([str(date),month_name,str(year)]),font='Harrington 17')
			elif i==0:
				self.canvas.create_text(self.convert.change(x_coord,y_coord),fill='white',text=str(12),font=self.font_digital)				
			else:
				self.canvas.create_text(self.convert.change(x_coord,y_coord),fill='white',text=str(i),font=self.font_digital)
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
		self.canvas.create_text(self.convert.change(0,-1.4),fill=self.text_color,text="      "+digital_time,font=self.font_digital)





	def create1(self):
		year,month,date,*extra = datetime.timetuple(datetime.utcnow()-self.time_gap)
		start,step		= pi/2,pi/6
		for i in range(12):
			angle		= start-(i*step)
			x_coord,y_coord	= 0.2*cos(angle),0.2*sin(angle)
			self.canvas.create_text(self.convert.change(x_coord,y_coord+0.4),fill='blue',text=str(i+1),font='calibri 9')
		angle		= start-((month-1)*step)
		x_month,y_month	= 0.15*cos(angle),0.15*sin(angle)
		self.canvas.create_line(self.convert.coords(0,0.4,x_month,y_month+0.4),fill="red",arrow='last')
		self.canvas.create_text(self.convert.change(0,0.45),fill='white',text='Month',font='Papyrus 10')

	


	def create2(self):
		year,month,date,*extra = datetime.timetuple(datetime.utcnow()-self.time_gap)
		start,step		= pi/2,pi*2/31
		for i in range(31):
			angle		= start-(i*step)
			x_coord,y_coord	= 0.35*cos(angle),0.35*sin(angle)
			self.canvas.create_text(self.convert.change(x_coord,y_coord-0.5),fill='blue',text=str(i+1),font='calibri 7 bold')
		angle		= start-((date-1)*step)
		x_date,y_date	= 0.3*cos(angle),0.3*sin(angle)
		self.canvas.create_line(self.convert.coords(0,-0.5,x_date,y_date-0.5),fill="red",arrow='last')
		self.canvas.create_text(self.convert.change(0,-0.45),fill='white',text='Date',font='Papyrus 10')




	def create3(self):
		year,month,date,h,m,s,day,yday,*extra = datetime.timetuple(datetime.utcnow()-self.time_gap)
		day=day+1#######
		start,step		= pi/2,pi*2/7
		for i in range(7):
			angle		= start-(i*step)
			x_coord,y_coord	= 0.2*cos(angle),0.2*sin(angle)
			self.canvas.create_text(self.convert.change(x_coord-0.5,y_coord),fill='blue',text=str(i+1),font='calibri 9')
		angle		= start-((day-1)*step)
		x_day,y_day	= 0.15*cos(angle),0.15*sin(angle)
		day_list=['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']
		day_name=day_list[day-1]
		self.canvas.create_text(self.convert.change(0.5,0),fill='white',text=day_name,font='Papyrus 10')
		self.canvas.create_line(self.convert.coords(-0.5,0,x_day-0.5,y_day),fill="red",arrow='last')
		self.canvas.create_text(self.convert.change(-0.5,0.05),fill='white',text='Day',font='Papyrus 10')
	



		


#program:

time_gap	= -5.5
w,h		= 500,650
root		= Tk()
make_clock(root,time_gap,w,h)
root.mainloop()