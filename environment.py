import vpython as vp
from time import *
#1800*900
envSizes = 70,1,70
scene = vp.canvas(title='Natural Selection Environment', width=1800, height=900, background= vp.vector(.95,.95,.95))
space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))