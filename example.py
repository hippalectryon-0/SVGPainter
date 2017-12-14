## Paint an SVG
from SVGPainter import drawSvg
drawSvg(650, 800, 613+10, 83+20+100*1,'C://Users//Hippa//Documents//GitHub//SVGPainter//test.svg',flip_svg=False)

## Create a custom Scene and draw items
from SVGPainter import Scene, Line, RegPol, Rectangle
scene=Scene()
scene.add(RegPol([50,60],30,8))
scene.add(RegPol([350,350],100,5))
scene.add(RegPol([600,350],40,3))
scene.add(Rectangle([100,450],(200,650)))
scene.draw(650,800,620,200)

## Create custom shapes
from SVGPainter import Scene, CurveDrawer
from numpy import array,pi,cos,sin
class MyShape(): # Epicycloid
	def __init__(self,center,a,b,nP,scale=1):
		self.center=array(center)
		self.a=a
		self.b=b
		self.nP=nP
		self.scale=scale
		
	def curve(self,t):
		t=t*2*pi
		return self.center+self.scale*array([(self.a+self.b)*cos(t)-self.b*cos((self.a/self.b+1)*t),(self.a+self.b)*sin(t)-self.b*sin((self.a/self.b+1)*t)])
	
	def draw(self,drawer):
		drawer.draw(self.curve,0,1,self.nP)
Scene([MyShape([300,300],3,1,50,20),MyShape([300,300],12,1,500,20)]).draw(650,800,620,200)