import startUpWindow
import vpython as vp
import time
import environment
import creature
import random
import copy
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
from PIL import Image
import radarChart
import lineChart
import os
import naturalDisasters
import math

startUpWindow.StartUp()
startUpConfigurations= startUpWindow.startUpConfigurations
envSizes = startUpConfigurations["envSizes"]
env = environment.Enviroment(envSizes)

PhyloTree = Tree()
root = PhyloTree.get_tree_root()
genePool = {}

class Chars:
    chars = {}
    EoDStats = {}
    population = {}
    def __init__(self, number=10):
        positions = [
            (envSizes[0], 0, (envSizes[2] * 0.9) // 2),
            (envSizes[2], 0, (envSizes[0] * 0.9) // 2),
            (envSizes[0], 0, (-envSizes[2] * 0.9) // 2),
            (envSizes[2], 0, (-envSizes[0] * 0.9) // 2),
        ]
        say = number
        idm = 0
        for j in range(4):
            if say%4 != 0:
                don = say//4 + 1
                say -=1
            else:
                don = number//4
            for i in range(don):
                pos = round(positions[j][0] * 0.85 / (number / 4), 2) * i - round(positions[j][0] * 0.85 / 2, 2)
                actual_pos = (pos, 0, positions[j][2]) if j % 2 == 0 else (positions[j][2], 0, pos)
                char = creature.Creature(idnumber=idm, pos=actual_pos)
                self.chars[idm] = char
                if self.chars[idm].gene not in genePool:
                    nstyle = NodeStyle()
                    nstyle["fgcolor"] = ("#{:02x}{:02x}{:02x}".format(int(char.body.color.x*255), int(char.body.color.y*255), int(char.body.color.z*255)))
                    nstyle["size"] = 10
                    genePool[self.chars[idm].gene] = root.add_child(name= self.chars[idm].gene)
                    genePool[self.chars[idm].gene].set_style(nstyle)
                idm +=1
                
       

    def setPos(self,foodlist):
        for char in self.chars.values():
            char.searchFood(foodlist.foods)
                
    def results(self):
        winners = []
        losers = []
        for char in self.chars.values():
            if char.hunger:
                winners.append(char.id)
                oldGene= char.gene
                mutationState = char.mutation()
                if mutationState and (char.gene not in genePool):
                    nstyle = NodeStyle()
                    nstyle["size"] = 10
                    nstyle["fgcolor"] = ("#{:02x}{:02x}{:02x}".format(int(char.body.color.x*255), int(char.body.color.y*255), int(char.body.color.z*255)))
                    genePool[char.gene] = genePool[oldGene].add_child(name=char.gene)
                    genePool[char.gene].set_style(nstyle)
            else:
                char.unVisible()
                losers.append(char.id)
        
        self.dailyStats(winners,len(losers))
        
        for charId in winners:
            while True:#burayı değiştir bence belki buga girmesini burası sağlıyordur
                newId = random.randint(0,1000000)
                if not (newId in winners):
                    break
            #print(f"{charId} duplicated {newId}")
            color = copy.deepcopy(self.chars[charId].body.color)
            speed = copy.deepcopy(self.chars[charId].genomes["speed"])
            vision = copy.deepcopy(self.chars[charId].genomes["vision"])
            visionRadius = copy.deepcopy(self.chars[charId].genomes["visionRadius"])
            axis =copy.deepcopy(self.chars[charId].body.axis)
            pos = copy.deepcopy(self.chars[charId].body.pos)
            self.chars[newId] = creature.Creature(idnumber=newId,color=(color.x,color.y,color.z),speed=speed, vision=vision, visionRadius=visionRadius,axis=(axis.x,axis.y,axis.z), pos=(pos.x,pos.y,pos.z))
            self.chars[newId].angle.pos.x = (visionRadius/2)*axis.x + self.chars[newId].body.pos.x
            self.chars[newId].angle.pos.z = (visionRadius/2)*axis.z + self.chars[newId].body.pos.z
            self.chars[newId].angle.axis = self.chars[newId].body.axis
            self.chars[newId].angle.visible = False
            
            
        for loser in losers:
            del self.chars[loser].body
            del self.chars[loser].idText
            del self.chars[loser].angle
            self.chars.pop(loser)
            
        return winners, losers
        
    def dailyStats(self, winners,lenLosers):
        
        if len(winners):
            sumS = {name: 0 for name in list(self.chars[winners[0]].genomes.keys())}
            for charId in winners:
                for isim in list(sumS.keys()):
                    if isim == "immunity":
                        sumS[isim] +=len(self.chars[charId].genomes[isim])
                    else:
                        sumS[isim] +=self.chars[charId].genomes[isim] 
                    
            
            self.EoDStats[day] = [values/len(winners) for values in list(sumS.values())]
            self.population[day] = [(len(winners)+lenLosers),len(winners),lenLosers,isDisasterInDay]
 
    def resetPos(self):
        i = 0
        for char in self.chars.values():
            pos = round(envSizes[0]*0.85/len(self.chars)*i,2)-round(envSizes[0]*0.85/2,2)
            axis = vp.vector(1,0,0)
            char.body.axis = axis
            char.body.pos=vp.vector(pos,0,(envSizes[2]*0.9)//2)            
            char.idText.pos = char.body.pos
            char.angle.pos.x = (char.genomes["visionRadius"]/2)*axis.x + char.body.pos.x
            char.angle.pos.z = (char.genomes["visionRadius"]/2)*axis.z + char.body.pos.z
            char.angle.axis = char.body.axis
            char.angle.visible = False
            
            
            char.hunger =False
            i +=1
    
    def endofDay(self,Foods):
        #print("End of The Day", day)
        winners, losers = self.results()
        #print("Results:")
        #print("Winners:", winners)
        #print("Losers:", losers)
        #time.sleep(2)
        Foods.restartFoods()
        self.resetPos()
        #time.sleep(1)
        
    def countGene(self):
        ts = TreeStyle()
        ts.show_leaf_name = True
        for i in genePool.keys():
            genes = []
            for j in self.chars.values():
                genes.append(j.gene)
            total = genes.count(i)
            totalText = TextFace(str(total))
            totalText.fgcolor="red"
            genePool[i].add_face(totalText, column=1, position = "branch-bottom")

    def lookSickness(self):
        for id in self.chars.keys():
            self.chars[id].sickness()
            
    def lookHeal(self):
        for id in self.chars.keys():
            if self.chars[id].diseased != {}:
                oldGene= self.chars[id].gene
                changeState = self.chars[id].heal()

                if changeState and (self.chars[id].gene not in genePool):
                    nstyle = NodeStyle()
                    nstyle["size"] = 10
                    nstyle["fgcolor"] = ("#{:02x}{:02x}{:02x}".format(int(self.chars[id].body.color.x*255), int(self.chars[id].body.color.y*255), int(self.chars[id].body.color.z*255)))
                    genePool.update({self.chars[id].gene: genePool[oldGene].add_child(name=self.chars[id].gene)})
                    genePool[self.chars[id].gene].set_style(nstyle)
                    
                
class Foods:
    foods = {}
    def __init__(self,number):
        self.number = number
        for i in range(number):
            x = int(envSizes[0]*0.75)
            z = int(envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
    
    def restartFoods(self):
        for food in self.foods.values():
            food.body.visible = False
            #food.idText = False
        self.foods.clear()
        
        for i in range(self.number):
            x = int(envSizes[0]*0.75)
            z = int(envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
        
dozenChar = Chars(startUpConfigurations["startPopulation"])
dozenFood = Foods(startUpConfigurations["startFood"])

env.dozenChar = dozenChar
env.menu.choices= env.updateMenu(dozenChar)
times = 0
day = 1

ts = TreeStyle()
ts.show_leaf_name = True
ts.mode = "c"
ts.arc_start = -180
ts.arc_span = 180

filenames = []

folderPath = "results/dailyPhyloTree/"
fileList = os.listdir(folderPath)
for file_name in fileList:
    if file_name.endswith(".png"):
        file_path = os.path.join(folderPath, file_name)
        os.remove(file_path)

# Giriş sayfası ayarları




#disasters = naturalDisasters.Disasters()
dayLength = 24*60
isDisaster = False
isDisasterInDay = 0
#Daily loop
while True:
    if env.running:
        dozenChar.setPos(dozenFood)
        if isDisaster:
            dozenChar.chars,isDisaster = disasters.collideCheck(dozenChar.chars)
            dozenChar.lookSickness()
        
        if times >= dayLength:
            
            dozenChar.lookHeal()
            dozenChar.endofDay(dozenFood)
            env.dozenChar = dozenChar
            env.menu.choices= env.updateMenu(dozenChar)
            
            disasterHarsness = env.disasterHarsness
            disasterRandom = random.random()
            isDisaster = False
            isDisasterInDay = 0
            if disasterRandom<env.disasterPossibility:
                isDisaster = True
                disasterTime = random.randint(int(dayLength*0.45),int(dayLength*0.90))
                disasters = naturalDisasters.Disasters(disasterHarsness,disasterTime)
                isDisasterInDay = disasters.state +1
            
            PhyloTree.render(f"results/dailyPhyloTree/Tree_day{day}.png", tree_style=ts)
            filenames.append(f"results/dailyPhyloTree/Tree_day{day}.png")
            
            times = 0
            day +=1
            if day >= 11 or len(dozenChar.chars.keys()) == 0:
                break
        times += 1
        env.dayInfo.text = f"    |     Time= {(times//60):02d}:{(times%60):02d}    Day= {day}"
        vp.rate(env.speed.value)

    else:
        vp.rate(30)    

#result .Gif
images = [ ]
if len(filenames)!=0:
    for filename in filenames:
        images.append(Image.open(filename))
    width, height = images[0].size
    images[0].save("results/dailyPhyloTree/result.gif", save_all=True, append_images=images[1:], duration=500, loop=0)

dozenChar.countGene()
#Graphs
radarChart.resultChart(dozenChar.EoDStats)
lineChart.lineResult(dozenChar.EoDStats,dozenChar.population)
lineChart.populationDistribution(dozenChar.chars)
PhyloTree.show(tree_style=ts)

while True:
    pass