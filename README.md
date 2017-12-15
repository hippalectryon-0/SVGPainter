SVGPainter
===================
SVGPainter allows you to draw SVG or custom shapes on programs such as Paint.
Only tested on Windows10.

How to use
-------------
All the required functions are in `SVGPainter.py`. Examples are given in `example.py`.
## Painting an SVG
Painting an SVG is done via the `drawSVG` function:

    from SVGPainter import drawSvg
    drawSvg(sX,sY,xmin,ymin,filepath,bbox=True,flip_svg=True)
## Painting custom shapes
Painting custom shapes is done by creating a `Scene` , adding elements to that Scene, then drawing it:

    from SVGPainter import Scene, Rectangle
    scene=Scene()
    scene.add(Rectangle([100,450],(200,650)))
    scene.draw(650,800,620,200)

Several shapes are builtin and can be imported: `Rectangle,Line,RegPol,Bezier,CubicBezier`

Documentation
-------------
## drawSVG(sX,sY,xmin,ymin,name,bbox=True,flip_svg=False,auto_resize=True)
Draws the SVG file located at `name` in a box of size `sX,sY` located at `xmin,ymin` from the top left corner.
*bbox* ("bounding box"): if True, draws a rectangle indicating the scene's box
*flip_svg*: if True, flip the SVG vertically (SVGs are sometime encoded flipped)
*auto_resize*: instead of using the width and height provided by the SVG file, which can be misleading, automatically finds the best width and height (+5%) including all the shapes in the image

## Scene(elts=[])
A `Scene` is a container for the shapes to draw.
*elts* ("elements"): the scene can be initialized with a list of shapes.

Once a scene is created, shapes can be added via the `add` function:

    scene=Scene()
    scene.add(shape)
  
Finally, the scene can be drawn on a given box of size `sX,sY` located at `xmin,ymin` from the top left corner using the `draw` function:
 `scene.draw(sX,sY,xmin,ymin)`
 All the coordinates of the shapes are relative to the drawing box.

## Shapes
A scene contains geometric shapes. There are several builtin shapes:
### RegPol(center,radius,n_sides=3,rot=0)
A regular polygon located on the circle of radius `radius` and center `center` with `n_sides` sides, rotated by `rot`*2π radians. If `n_sides` is high enough, draws a near-circle.
### Line(start,end,nP=2)
A line from `start` to `end` as coordinates `[x,y]`, with `nP` points.
### Rectangle(start,end)
A rectangle from `start` to `end` as coordinates `[x,y]`.
### Bezier(P0,P1,P2,nP)
Quadratic Bezier curve given three points `P0,P1,P2` as coordinates `[x,y]` with `nP` points.
### CubicBezier(P0,P1,C0,C1,nP)
Cubic Bezier curve given a starting point `P0`, an end point `P1`, and their two control points `C0,C1` as coordinates `[x,y]` with `nP` points.

### Creating custom shapes
You can create your own shapes. A shape is a class that contains two functions, `curve` and `draw`:

    class MyShape():
    	def curve(self,t):
    		return foo(t)
    	def draw(self,drawer):
    		drawer.draw(self.curve,tmin,tmax,steps)
 The shape is determined by its parametric curve `MyShape().curve(t)`. 
 The `draw` function uses a `CurveDrawer` instance passed as an argument `drawer` by the `scene` to draw itself between `tmin` and `tmax` with `steps` steps.

## CurveDrawer()
This is the class that handles the drawings and the mouse movements. **By default, you won't have to manipulate this class directly, all the work is done via the `Scene` object.**

It needs to be initialized through `CurveDrawer().init(sX,sY,xmin,ymin)` defining the box in which it can draw, of size `sX,sY` located at `xmin,ymin` from the top left corner.

For each shape class, it can then be called through `CurveDrawer().draw(self,curve,tmin,tmax,steps=2,wait_time=1/60.)` which draws the parametric curve `curve` from `tmin` to `tmax` with `steps` steps, waiting `wait_time` between each step.