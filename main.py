import vpython as vp
import time
import environment
import creature
import random
import copy

env = environment.Enviroment(environment.envSizes)

class Chars:
    chars = {}
    def __init__(self, number=10):
        for i in range(number):
            pos = round(environment.envSizes[0]*0.85/number,2)*i-round(environment.envSizes[0]*0.85/2,2)
            char = creature.Creature(idnumber=i,pos=(pos,0,(environment.envSizes[2]*0.9)//2))
            self.chars[i]= char

    def setPos(self,foodlist):
        for char in self.chars.values():
            char.searchFood(foodlist.foods)
                
    def results(self):
        winners = []
        losers = []
        for char in self.chars.values():
            if char.hunger:
                winners.append(char.id)
                char.mutation()
            else:
                char.unVisible()
                losers.append(char.id)
        
        for charId in winners:
            while True:
                newId = random.randint(0,1000000)
                if not (newId in winners):
                    break
            print(f"{charId} duplicated {newId}")
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
            
            
        for loser in losers:
            del self.chars[loser].body
            del self.chars[loser].idText
            del self.chars[loser].angle
            self.chars.pop(loser)
            
        return winners, losers
        
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
            
            
            char.hunger =False
            i +=1
    
    def endofDay(self,Foods):
        print("End of The Day")
        winners, losers = self.results()
        print("Results:")
        print("Winners:", winners)
        print("Losers:", losers)
        time.sleep(2)
        Foods.restartFoods()
        self.resetPos()
        time.sleep(1)
        
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
        
dozenChar = Chars(10)
dozenFood = Foods(70)

env.dozenChar = dozenChar
env.menu.choices= env.updateMenu(dozenChar)

times = 0
day = 0
while True:
    if env.running:
        dozenChar.setPos(dozenFood)
        #environment.info(dozenChar.chars)
        
        if times >=30*20:
            dozenChar.endofDay(dozenFood)
            env.dozenChar = dozenChar
            env.menu.choices= env.updateMenu(dozenChar)
            times = 0
            day +=1
        if day >= 10:
            break
        
        times += 1
    vp.rate(40)

while True:
    pass