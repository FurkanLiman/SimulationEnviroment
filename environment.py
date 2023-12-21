import vpython as vp
from time import *
#1800*900
envSizes = 70,1,70
scene = vp.canvas(title='Natural Selection Environment      ', width=1800, height=900, background= vp.vector(.95,.95,.95))
space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))

"""vp.arrow(pos=vp.vector(0,2,0), axis=vp.vector(2,0,0), color= vp.color.red)
vp.label(text="x",color=vp.color.red, pos=vp.vector(1,2,0),line=True)
vp.arrow(pos=vp.vector(0,2,0), axis= vp.vector(0,0,2), color = vp.color.blue)
vp.label(text="z",color=vp.color.blue, pos=vp.vector(0,2,1),line=True)"""

running = True

def Run(b):
    global running
    running = not running
    if running: b.text = "Pause"
    else: b.text = "Run"


vp.button(text="Pause", pos=scene.title_anchor, bind=Run)


infos = vp.wtext(text="")
def info(chars):
    infos.text = ""
    texts = ""
    for char in chars.values():
        gens = ""
        
        for name,gen in char.genomes.items():
            gens += f"  {name}  {gen},"
        texts +=  f"id: {char.id}" + gens + "\n"
    infos.text = texts