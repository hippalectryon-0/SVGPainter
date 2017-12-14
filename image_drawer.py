from time import sleep # pause the program
import win32api, win32con # simulate mouse presses and listen to mouse events
from numpy import linspace,array,cos,sin,pi,arcsin,arccos,arctan,array_equal,sqrt # maths
import svgpathtools # convert SVG to paths

## Mouse handling
def m_move(x,y): # mouse mouse at pos (x,y) in pixels from top left corner
    win32api.SetCursorPos((x,y))

def m_up(): # sets LMB up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

def m_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)

def click(x,y):
    m_move(x,y)
    m_down()
    m_up()
    
## Maths

def Heaveside(x): # Heaveside that's 1/2 for x=0
    if x==0: return .5
    return 0 if x<0 else 1

def sgn(x): # sign of x, 0 for x=0
    if x==0: return 0
    return 1 if x>0 else -1

def sgnp(x): # sign of x, 1 for x=0
    return 1 if x>=0 else -1

## Drawer
class CurveDrawer():
    def __init__(self):
        """
        sX,sY: size (pixels) of the windows in which to draw
        xmin,ymin: top left corner of the window to draw in
        """
        # init vars
        self.prev_curs_pos=array([])
    
    def initFrame(self,sX,sY,xmin,ymin):
        # propagate vars
        self.sX=sX
        self.sY=sY
        self.xmin=xmin
        self.ymin=ymin
    
    def draw(self,curve,tmin,tmax,steps=2,wait_time=1/60.):
        """
        draws the curve given by moving the mouse down at each curve(t) for tmin<=t<=tmax with `steps` steps. The pause between each step is `wait_time`
        the mouse state is NOT restored up in the end
        Pauses before starting if MB3 is pressed, resumes when MB3 (usually mouse wheel click) is pressed again
        """
        if win32api.GetKeyState(0x04)<0: # mb3 down, usually mouse wheel click
            m_up()
            while win32api.GetKeyState(0x04)<0: # mb3 down, usually mouse wheel click
                sleep(wait_time)
            while win32api.GetKeyState(0x04)>=0: # mb3 up, usually mouse wheel click
                sleep(wait_time)
            while win32api.GetKeyState(0x04)<0: # mb3 down, usually mouse wheel click
                sleep(wait_time)
            if self.prev_curs_pos.shape[0]!=0: # if there's a prev position
                m_move(self.prev_curs_pos[0],self.prev_curs_pos[1])
            m_down()
        
        stay_on=False # don't get the mouse up if there no change of position between two curves
        x,y=curve(tmin)
        x,y=int(self.xmin+max(0,min(x,self.sX))),int(self.ymin+max(0,min(y,self.sY)))
        if self.prev_curs_pos.shape[0]!=0: # if there's a prev position
            stay_on=array_equal(array([x,y]),self.prev_curs_pos)
        
        m_up()
        sleep(wait_time)
        m_move(x,y)
        m_down()
        for t in linspace(tmin,tmax,steps):
            sleep(wait_time)
            pos=curve(t);x,y=pos[0],pos[1]
            x,y=int(self.xmin+max(0,min(x,self.sX))),int(self.ymin+max(0,min(y,self.sY)))
            m_move(x,y)
            m_down()
        self.prev_curs_pos=array([x,y])
        
## Geometric shapes
class RegPol():
    def __init__(self,center,radius,n_sides=3,rot=0):
        self.center=array(center) # center [x,y]
        self.radius=radius
        self.n_sides=n_sides
        self.rot=rot # rotation 1=2pi
    
    def curve(self,t):
        return self.center+self.radius*array([cos((t+self.rot)*2*pi),sin((t+self.rot)*2*pi)])
    
    def draw(self,drawer):
        drawer.draw(self.curve,0,1,self.n_sides+1)

class Line():
    def __init__(self,start,end,nP=2):
        self.start=array(start)
        self.end=array(end)
        self.nP=nP
    
    def curve(self,t):
        return self.start*t+self.end*(1-t)
    
    def draw(self,drawer):
        drawer.draw(self.curve,0,1,self.nP)

class Rectangle():
    def __init__(self,start,end):
        self.start=array(start)
        self.end=array(end)
    
    def draw(self,drawer):
        Line(self.start,[self.start[0],self.end[1]]).draw(drawer)
        Line([self.start[0],self.end[1]],self.end).draw(drawer)
        Line(self.end,[self.end[0],self.start[1]]).draw(drawer)
        Line([self.end[0],self.start[1]],self.start).draw(drawer)

class Bezier(): # Quad Bezier
    def __init__(self,P0,P1,P2,nP):
        self.P0=array(P0) # start
        self.P1=array(P1) # mid
        self.P2=array(P2) # end
        self.nP=nP # points
    
    def curve(self,t):
        return (1-t)*((1-t)*self.P0+t*self.P1)+t*((1-t)*self.P1+t*self.P2)
    
    def draw(self,drawer):
        drawer.draw(self.curve,0,1,self.nP)

class CubicBezier():
    def __init__(self,P0,P1,C0,C1,nP):
        self.P0=array(P0) # start
        self.P1=array(P1) # end
        self.C0=array(C0) # control
        self.C1=array(C1)
        self.nP=nP # points
    
    def curve(self,t):
        B1=Bezier(self.P0,self.C0,self.C1,self.nP)
        B2=Bezier(self.C0,self.C1,self.P1,self.nP)
        return (1-t)*B1.curve(t)+t*B2.curve(t)
    
    def draw(self,drawer):
        drawer.draw(self.curve,0,1,self.nP)

## Scene to draw
class Scene():
    def __init__(self,elts=[]):
        self.elts=elts
        self.drawer=CurveDrawer()
    
    def add(self,elt):
        self.elts.append(elt)
        
    def remove(self,elt):
        self.elts.remove(elt)
        
    def draw(self,sX,sY,xmin,ymin):
        """
        sX,sY: size (pixels) of the windows in which to draw
        xmin,ymin: top left corner of the window to draw in
        """
        self.drawer.initFrame(sX,sY,xmin,ymin)
        for elt in self.elts:
            elt.draw(self.drawer)
        m_up()

def draw_svg(sX,sY,xmin,ymin,name='C://Users//Hippa//Documents//Python stuff//TOL Image drawer//test.svg',bbox=True,flip_svg=False):
    """
    Draws the svg `name`, with a bounding box if `bbox`, flipped if `flip_svg`
    sX,sY: size (pixels) of the windows in which to draw
    xmin,ymin: top left corner of the window to draw in
    """
    paths, attributes, svg_attributes = svgpathtools.svg2paths2(name)
    svg_w,svg_h=int(float(svg_attributes['width'].replace('px','').replace('pt',''))),int(float(svg_attributes['height'].replace('px','').replace('pt','')))
    svg_w,svg_h=8000,7500 # may have to tweak those manually
    factX,factY=sX/svg_w,sY/svg_h
    
    scene=Scene()
    if bbox:
        scene.add(Rectangle([0,0],[sX,sY])) # Bounding box
    
    def flip(elt): # flip an image vertically, sometimes needed
        if type(elt) is svgpathtools.Line or type(elt) is svgpathtools.CubicBezier:
            elt.start=elt.start.real+1j*(svg_h-elt.start.imag)
            elt.end=elt.end.real+1j*(svg_h-elt.end.imag)
        if type(elt) is svgpathtools.CubicBezier:
            elt.control1=elt.control1.real+1j*(svg_h-elt.control1.imag)
            elt.control2=elt.control2.real+1j*(svg_h-elt.control2.imag)
        return elt
    for i in range(len(paths)):
        path,attrib=paths[i],attributes[i]
        for elt in path:
            if flip_svg:
                elt=flip(elt)
            if type(elt) is svgpathtools.Line:
                scene.add(Line([elt.start.real*factX,elt.start.imag*factY],[elt.end.real*factX,elt.end.imag*factY],4))
            elif type(elt) is svgpathtools.CubicBezier:
                scene.add(CubicBezier([elt.start.real*factX,elt.start.imag*factY],[elt.end.real*factX,elt.end.imag*factY],[elt.control1.real*factX,elt.control1.imag*factY],[elt.control2.real*factX,elt.control2.imag*factY],3))
            elif type(elt) is svgpathtools.Arc:
                continue # Not implemented yet
            else:
                print(elt)
    
    scene.draw(sX,sY,xmin,ymin)

sleep(1)
draw_svg(650, 800, 613+10, 83+20+100*1,flip_svg=True)






















