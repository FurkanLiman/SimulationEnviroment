import vpython as vp
from time import *
import mutationFactors

#1800*900
envSizes = 70,1,70




class Enviroment:
    def __init__(self,envSizes):
        self.scene = vp.canvas(title='Natural Selection Environment ', width=1800, height=900, background= vp.vector(.95,.95,.95))
        self.space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))
        vp.button(text="Pause", pos=self.scene.title_anchor, bind=self.Run)
        vp.wtext(text= "    |   ", pos = self.scene.title_anchor)
        vp.checkbox(text="Show View Angles    ", pos = self.scene.title_anchor, bind=self.showAngles)
        vp.wtext(text='|    Vary the speedrate', pos= self.scene.title_anchor, color = vp.color.red)
        self.speed = vp.slider(min=5, max=200, value=30, length=220,pos=self.scene.title_anchor, bind=self.setSpeed, right=15)
        self.speedText = vp.wtext(text='{:1.2f}'.format(self.speed.value), pos= self.scene.title_anchor)
        self.dayInfo = vp.wtext(text= "    |    Time= 00:00    Day= 0", pos = self.scene.title_anchor)
        vp.wtext(text= "    |    MutationRate:", pos = self.scene.title_anchor)
        self.mutationRate = vp.slider(min=0, max=1000, value=5, length=220,pos=self.scene.title_anchor, bind=self.setMutationRate, right=15, text= "sea")
        self.mutationRateText = vp.wtext(text='{:1.2f}'.format(self.mutationRate.value/1000), pos= self.scene.title_anchor)
        mutationFactors.mutationProbability = self.mutationRate.value/1000
        
        self.running = True
        self.menulist = ["default"]
        self.dozenChar = None
        self.menu = vp.menu(choices=self.menulist, index=0, bind=self.selectCreature)
        self.infos = vp.wtext(text="  Select id to see information")

    def Run(self,b):
        self.running
        self.running = not self.running
        if self.running: b.text = "Pause"
        else: b.text = "Run"

    def setMutationRate(self, d):
        mutationFactors.mutationProbability = d.value /1000
        self.mutationRateText.text = '{:1.3f}'.format(d.value/1000)

    def selectCreature(self,m):
        val = m.selected
        if val == "default":
            self.infos.text = "  Select id to see information"
            self.scene.camera.follow(self.space)
        else:
            self.info(self.dozenChar.chars[int(val)])
            self.scene.camera.follow(self.dozenChar.chars[int(val)].body)
    
    def showAngles(self,r):
        if r.checked:
            for i in self.dozenChar.chars.values():
                i.angle.visible= True
        else:
            for i in self.dozenChar.chars.values():
                i.angle.visible= False

    def setSpeed(self, s):
        self.speedText.text = '{:1.2f}'.format(s.value)
    
            
    def updateMenu(self,dozenChar):
        self.menulist = ["default"]
        for i in sorted(list(dozenChar.chars.keys())):
            self.menulist.append(str(i))
        return self.menulist 

    def info(self, char):
        self.infos.text = ""
        texts = ""
        gens = ""
        for name,gen in char.genomes.items():
            gens += f"  {name}  {gen},"
        texts =  f"  id: {char.id}" + gens + " hunger:" + str(not char.hunger)  + "\n"
        
        self.infos.text = texts
        
    
