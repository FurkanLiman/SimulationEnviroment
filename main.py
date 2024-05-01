import vpython as vp
import time
import environment
import creature
import random
import copy
from ete3 import Tree, TreeStyle, NodeStyle, TextFace
from PIL import Image
import radarChart

env = environment.Enviroment(environment.envSizes)

PhyloTree = Tree()
root = PhyloTree.get_tree_root()
genePool = {}

class Chars:
    chars = {}
    EoDStats = {}
    def __init__(self, number=10):
        for i in range(number):
            pos = round(environment.envSizes[0]*0.85/number,2)*i-round(environment.envSizes[0]*0.85/2,2)
            char = creature.Creature(idnumber=i,pos=(pos,0,(environment.envSizes[2]*0.9)//2))

            self.chars[i]= char
            if self.chars[i].gene not in genePool:
                nstyle = NodeStyle()
                nstyle["fgcolor"] = ("#{:02x}{:02x}{:02x}".format(int(char.body.color.x*255), int(char.body.color.y*255), int(char.body.color.z*255)))
                nstyle["size"] = 10
                genePool[self.chars[i].gene] = root.add_child(name= self.chars[i].gene)
                genePool[self.chars[i].gene].set_style(nstyle)

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
                if mutationState:
                    nstyle = NodeStyle()
                    nstyle["size"] = 10
                    nstyle["fgcolor"] = ("#{:02x}{:02x}{:02x}".format(int(char.body.color.x*255), int(char.body.color.y*255), int(char.body.color.z*255)))
                    genePool[char.gene] = genePool[oldGene].add_child(name=char.gene)
                    genePool[char.gene].set_style(nstyle)
            else:
                char.unVisible()
                losers.append(char.id)
        
        self.dailyStats(winners)
        
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
        
    def dailyStats(self, winners):
        speedSum, visionSum,visionRadiusSum = 0,0,0
        for charId in winners:
            speedSum += self.chars[charId].genomes["speed"]
            visionSum += self.chars[charId].genomes["vision"]
            visionRadiusSum += self.chars[charId].genomes["visionRadius"]
        avarageSpeed = speedSum / len(winners)
        avarageVision = visionSum / len(winners)
        avarageVisionRadius = visionRadiusSum / len(winners)
        self.EoDStats[day] = [avarageSpeed,avarageVision,avarageVisionRadius]
            
            
        
    def resetPos(self):
        i = 0
        for char in self.chars.values():
            pos = round(environment.envSizes[0]*0.85/len(self.chars)*i,2)-round(environment.envSizes[0]*0.85/2,2)
            axis = vp.vector(1,0,0)
            char.body.axis = axis
            char.body.pos=vp.vector(pos,0,(environment.envSizes[2]*0.9)//2)            
            char.idText.pos = char.body.pos
            char.angle.pos.x = (char.genomes["visionRadius"]/2)*axis.x + char.body.pos.x
            char.angle.pos.z = (char.genomes["visionRadius"]/2)*axis.z + char.body.pos.z
            char.angle.axis = char.body.axis
            char.angle.visible = False
            
            
            char.hunger =False
            i +=1
    
    def endofDay(self,Foods):
        print("End of The Day", day)
        winners, losers = self.results()
        print("Results:")
        print("Winners:", winners)
        print("Losers:", losers)
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

            
            
class Foods:
    foods = {}
    def __init__(self,number):
        self.number = number
        for i in range(number):
            x = int(environment.envSizes[0]*0.75)
            z = int(environment.envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
    
    def restartFoods(self):
        for food in self.foods.values():
            food.body.visible = False
            #food.idText = False
        self.foods.clear()
        
        for i in range(self.number):
            x = int(environment.envSizes[0]*0.75)
            z = int(environment.envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
        
dozenChar = Chars(2)
dozenFood = Foods(20)

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

while True:
    if env.running:
        dozenChar.setPos(dozenFood)
        
        if times >=24*60:
            dozenChar.endofDay(dozenFood)
            env.dozenChar = dozenChar
            env.menu.choices= env.updateMenu(dozenChar)
            
            PhyloTree.render(f"results/Tree_day{day}.png", tree_style=ts)
            filenames.append(f"results/Tree_day{day}.png")
            
            times = 0
            day +=1
        if day >= 15:
            break
        times += 1
        env.dayInfo.text = f"    |     Time= {(times//60):02d}:{(times%60):02d}    Day= {day}"
        vp.rate(env.speed.value)

    else:
        vp.rate(30)    


dozenChar.countGene()
#matplot grafiğini hem pylotreeyi aynı anda bastır.
radarChart.resultChart(dozenChar.EoDStats)
images = [ ]
if len(filenames)!=0:
    for filename in filenames:
        images.append(Image.open(filename))
    width, height = images[0].size
    images[0].save("results/result.gif", save_all=True, append_images=images[1:], duration=500, loop=0)

PhyloTree.show(tree_style=ts)

while True:
    pass