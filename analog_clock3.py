import sys, types, os
from time import localtime
from datetime import timedelta,datetime
from math import sin, cos, pi
from tkinter import * 





class mapper:
    ## Constructor.
    #world window rectangle.
    #viewport screen rectangle.

    def __init__(self, world, viewport):
        self.world = world 
        self.viewport = viewport
        x_min, y_min, x_max, y_max =world
        X_min, Y_min, X_max, Y_max =viewport
        f_x = float(X_max-X_min) / float(x_max-x_min) 
        f_y = float(Y_max-Y_min) / float(y_max-y_min) 
        self.f = min(f_x,f_y)
        x_c = 0.5 * (x_min + x_max)
        y_c = 0.5 * (y_min + y_max)
        X_c = 0.5 * (X_min + X_max)
        Y_c = 0.5 * (Y_min + Y_max)
        self.c_1 = X_c - self.f * x_c
        self.c_2 = Y_c - self.f * y_c

    ## Maps a single point from world coordinates to viewport (screen) coordinates.
    #
    #  x, y given point.
    #  return a new point in screen coordinates.
    #
    def __windowToViewport(self, x, y):
        X = self.f *  x + self.c_1
        Y = self.f * -y + self.c_2      # Y axis is upside down 
        return X , Y

    ## Maps two points from world coordinates to viewport (screen) coordinates.
    #
    #   x1, y1 first point.
    #  @param x2, y2 second point.
    #  @return two new points in screen coordinates.
    #
    def windowToViewport(self,x1,y1,x2,y2):
        return self.__windowToViewport(x1,y1),self.__windowToViewport(x2,y2)

## Class for drawing a simple analog clock.
#  The backgroung image may be changed by pressing key 'i'.
#  The image path is hardcoded. It should be available in directory 'images'.
#
class clock:

    def __init__(self,root,deltahours = 0,w = 500,h = 500):
        self.world       = [-1,-1,1,1] #left,top,right,down
        
        self.bgcolor     = '#000000' #background
        self.timecolor   = '#ffffff' #needlecolour
        self.circlecolor = '#808080' #colour of all the circles
        self.circlesize  = 0.05
        self._ALL        = 'handles'
        self.root        = root
        width, height    = w, h
        self.pad         = width/16

        self.delta = timedelta(hours = deltahours)
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad) #left,top,right,down
        self.T = mapper(self.world,viewport)  
        self.canvas = Canvas(root, width = width, height = height, background = self.bgcolor)#creates the background canvas
        self.canvas.pack(fill=BOTH, expand=True)
        #expand=bool - expand widget if parent size grows
        #fill=NONE or X or Y or BOTH - fill widget if widget grows
        self.canvas.bind("<Configure>",self.resize)


        
        self.poll()

    def resize(self,event):
        sc = self.canvas
        sc.delete(ALL)            # erase the whole canvas
        width  = sc.winfo_width()
        height = sc.winfo_height()

        imgSize = min(width, height)
        self.pad = imgSize/16
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad)
        self.T = mapper(self.world,viewport)


    ## Redraws the whole clock.
 
    def redraw(self):
        start = pi/2              # 12h is at pi/2
        step = pi/6		#Each hour
        for i in range(12):       # draw the minute ticks as circles
            angle =  start-i*step
            x, y = cos(angle),sin(angle)
            self.paintcircle(x,y)
        self.painthms()           # draw the handles
        self.paintcircle(0,0)  # draw a circle at the centre of the clock
   
        



    ## Draws the handles.
 
    def painthms(self):
        self.canvas.delete(self._ALL)  # delete the handles
        T = datetime.timetuple(datetime.utcnow()-self.delta)	#(year,month,mday,hour,min,sec,wday,ydaay,isdst)
        x,x,x,h,m,s,x,x,x = T
	
        self.root.title('%02i:%02i:%02i' %(h,m,s));'''
tkinter.Tk.title = wm_title(self, string=None)
    Set the title of this widget.'''

        angle = pi/2 - pi/6 * (h + m/60.0)
        x, y = cos(angle)*0.70,sin(angle)*0.70   
        scl = self.canvas.create_line
        # draw the hour handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = (self.pad-10)/3)
        angle = pi/2 - pi/30 * (m + s/60.0)
        x, y = cos(angle)*0.85,sin(angle)*0.85
        # draw the minute handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = (self.pad-10)/6)
        angle = pi/2 - pi/30 * s
        x, y = cos(angle)*0.95,sin(angle)*0.95   
        # draw the second handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, arrow = 'last')
        

       

    ## Draws a circle at a given point x,y given point.

    def paintcircle(self,x,y):
        rad = self.circlesize / 2.0
        draw_points = self.canvas.create_oval
	
        draw_points(self.T.windowToViewport(-rad+x,-rad+y,rad+x,rad+y), fill = self.circlecolor)
  

    def poll(self):
        self.redraw()
        self.root.after(1,self.poll);'''
tkinter.Tk.after = after(self, ms, func=None, *args)
    Call function once after given time.

    MS specifies the time in milliseconds. FUNC gives the
    function which shall be called. Additional parameters
    are given as parameters to the function call.  Return
    identifier to cancel scheduling with after_cancel.'''



#program:

deltahours = -5.5
w = h = 500
root = Tk()
clock(root,deltahours,w,h)
root.mainloop()
