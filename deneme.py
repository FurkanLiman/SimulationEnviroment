import vpython as vp
import time

#body = vp.ellipsoid(size = vp.vector(2,7,2), axis = vp.vector(1,0,0), color=vp.color.blue, pos=vp.vector(0,0,0))
#idText = vp.label(text="sa",color=vp.color.cyan, pos=body.pos,line=True)
scene = vp.canvas()

acider = 60
acirad = acider*vp.pi/180

aci = vp.shapes.circle(radius=2, angle1=-acirad/2,angle2=acirad/2)


sa = vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,0,-0.1)],
          shape= aci)





r = vp.pi/12
a = 0
while True:
    a += r
    time.sleep(1)
    sa.rotate(angle=r, axis=vp.vector(0,0,1), origin=vp.vector(0,0,0))
    vp.rate(60)
