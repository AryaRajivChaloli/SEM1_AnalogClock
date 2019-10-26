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

    def __init__(self,root,deltahours = 0,w = 400,h = 400):
        self.world       = [-1,-1,1,1] #left,top,right,down
        
        self.setColors()
        self.circlesize  = 0.09
        self._ALL        = 'handles'
        self.root        = root
        width, height    = w, h
        self.pad         = width/16

        
        self.delta = timedelta(hours = deltahours)
        viewport = (self.pad,self.pad,width-self.pad,height-self.pad)
        self.T = mapper(self.world,viewport)  
        self.canvas = Canvas(root, width = width, height = height, background = self.bgcolor)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.poll()

    def setColors(self):
           self.bgcolor     = '#000000' #background
           self.timecolor   = '#ffffff' #needlecolour
           self.circlecolor = '#808080' #colour of all the circles



    ## Redraws the whole clock.
    # 
    def redraw(self):
        start = pi/2              # 12h is at pi/2
        step = pi/6
        for i in range(12):       # draw the minute ticks as circles
            angle =  start-i*step
            x, y = cos(angle),sin(angle)
            self.paintcircle(x,y)
        self.painthms()           # draw the handles
        self.paintcircle(0,0)  # draw a circle at the centre of the clock
   
    ## Draws the handles.
    # 
    def painthms(self):
        self.canvas.delete(self._ALL)  # delete the handles
        T = datetime.timetuple(datetime.utcnow()-self.delta)
        x,x,x,h,m,s,x,x,x = T
	
        self.root.title('%02i:%02i:%02i' %(h,m,s))
        angle = pi/2 - pi/6 * (h + m/60.0)
        x, y = cos(angle)*0.70,sin(angle)*0.70   
        scl = self.canvas.create_line
        # draw the hour handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = self.pad/3)
        angle = pi/2 - pi/30 * (m + s/60.0)
        x, y = cos(angle)*0.90,sin(angle)*0.90
        # draw the minute handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, width = self.pad/5)
        angle = pi/2 - pi/30 * s
        x, y = cos(angle)*0.95,sin(angle)*0.95   
        # draw the second handle
        scl(self.T.windowToViewport(0,0,x,y), fill = self.timecolor, tag=self._ALL, arrow = 'last')
   
    ## Draws a circle at a given point x,y given point.

    def paintcircle(self,x,y):
        ss = self.circlesize / 2.0
        sco = self.canvas.create_oval
	
        sco(self.T.windowToViewport(-ss+x,-ss+y,ss+x,ss+y), fill = self.circlecolor)
  

    def poll(self):
        self.redraw()
        self.root.after(200,self.poll)



#program:

deltahours = -5.5
w = h = 400
root = Tk()
clock(root,deltahours,w,h)
root.mainloop()
