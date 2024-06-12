import vpython as vp
from time import *
import creature.mutationFactors as mutationFactors

#1800*900
envSizes = 150,1,150




class Enviroment:
    def __init__(self,envSizes):
        self.scene = vp.canvas(title='Natural Selection Environment ', width=1800, height=900, background= vp.vector(.95,.95,.95))
        self.space = vp.box(pos=vp.vector(0,-4,0),size=vp.vector(envSizes[0],envSizes[1],envSizes[2]))
        vp.button(text="Pause", pos=self.scene.title_anchor, bind=self.Run)
        vp.wtext(text= "    |   ", pos = self.scene.title_anchor)
        vp.checkbox(text="Show View Angles    ", pos = self.scene.title_anchor, bind=self.showAngles)
        vp.wtext(text='|    Vary Speedrate', pos= self.scene.title_anchor, color = vp.color.red)
        self.speed = vp.slider(min=5, max=200, value=30, length=220,pos=self.scene.title_anchor, bind=self.setSpeed, right=15)
        self.speedText = vp.wtext(text='{:1.2f}'.format(self.speed.value), pos= self.scene.title_anchor)
        self.dayInfo = vp.wtext(text= "    |    Time= 00:00    Day= 0", pos = self.scene.title_anchor)
        vp.wtext(text= "\nMutation Settings :   MutationPossibility:      ", pos = self.scene.title_anchor)
        self.mutationRate = vp.slider(min=0, max=1000, value=5, length=220,pos=self.scene.title_anchor, bind=self.setMutationRate, right=15, text= "sea")
        self.mutationRateText = vp.wtext(text='{:1.2f}'.format(self.mutationRate.value/1000), pos= self.scene.title_anchor)
        mutationFactors.mutationProbability = self.mutationRate.value/1000
        
        vp.wtext(text= "\nDisease  Settings :   DailyDisasterPossibility:", pos = self.scene.title_anchor)
        self.disasterPossibilityS = vp.slider(min=0, max=1000, value=250, length=220,pos=self.scene.title_anchor, bind=self.setDisasterPossibility, right=15, text= "sea")
        self.disasterPossibilityText = vp.wtext(text='{:1.2f}'.format(self.disasterPossibilityS.value/1000), pos= self.scene.title_anchor)
        self.disasterPossibility = self.disasterPossibilityS.value/1000
        
        vp.wtext(text= "    |    DiseaseHarsness:", pos = self.scene.title_anchor)
        self.disasterHarsnessS = vp.slider(min=1000, max=3000, value=1000, length=220,pos=self.scene.title_anchor, bind=self.setDisasterHarsness, right=15, text= "sea")
        self.disasterHarsnessText = vp.wtext(text='{:1.2f}'.format(self.disasterHarsnessS.value/1000), pos= self.scene.title_anchor)
        self.disasterHarsness = self.disasterHarsnessS.value/1000
        vp.wtext(text= "  ->   1 : Random    |    (1-2) : Temporary Physical Events    |    [2-2.8) : Permanent Immune Diseases    |    [2.8-3] : Lethal Diseases", pos = self.scene.title_anchor)
        
        
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

    def setDisasterHarsness(self, d):
        self.disasterHarsness = d.value /1000
        self.disasterHarsnessText.text = '{:1.3f}'.format(d.value/1000)

    def setDisasterPossibility(self, d):
        self.disasterPossibility = d.value /1000
        self.disasterPossibilityText.text = '{:1.3f}'.format(d.value/1000)

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
        
    
