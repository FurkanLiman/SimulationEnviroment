import vpython as vp
from time import *
#1800*900
envSizes = 70,1,70
"""scene = vp.canvas(title='Natural Selection Environment      ', width=1800, height=900, background= vp.vector(.95,.95,.95))
space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))"""

"""vp.arrow(pos=vp.vector(0,2,0), axis=vp.vector(2,0,0), color= vp.color.red)
vp.label(text="x",color=vp.color.red, pos=vp.vector(1,2,0),line=True)
vp.arrow(pos=vp.vector(0,2,0), axis= vp.vector(0,0,2), color = vp.color.blue)
vp.label(text="z",color=vp.color.blue, pos=vp.vector(0,2,1),line=True)"""



class Enviroment:
    def __init__(self,envSizes):
        self.scene = vp.canvas(title='Natural Selection Environment      ', width=1800, height=900, background= vp.vector(.95,.95,.95))
        self.space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))
        self.running = True
        vp.button(text="Pause", pos=self.scene.title_anchor, bind=self.Run)
        self.menulist = ["default"]
        self.dozenChar = None
        self.menu = vp.menu(choices=self.menulist, index=0, bind=self.M)
        self.infos = vp.wtext(text="select id to see information")

    def Run(self,b):
        self.running
        self.running = not self.running
        if self.running: b.text = "Pause"
        else: b.text = "Run"

    def M(self,m):
        val = m.selected
        if val == "default":
            self.infos.text = "select id to see information"
            self.scene.camera.follow(self.space)
        else:
            self.info(self.dozenChar.chars[int(val)])
            self.scene.camera.follow(self.dozenChar.chars[int(val)].body)
    
    def updateMenu(self,dozenChar):
        self.menulist = ["default"]
        for i in dozenChar.chars.keys():
            self.menulist.append(str(i))
        return self.menulist 

    def info(self, char):
        self.infos.text = ""
        texts = ""
        gens = ""
        for name,gen in char.genomes.items():
            gens += f"  {name}  {gen},"
        texts =  f"id: {char.id}" + gens + " hunger:" + str(not char.hunger)  + "\n"
        
        self.infos.text = texts
