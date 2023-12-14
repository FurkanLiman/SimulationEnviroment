import vpython as vp
import time
import environment
import creature
import random

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
                char.body.visible = False
                char.idText.visible = False
                losers.append(char.id)
        
        for loser in losers:
            del self.chars[loser].body
            self.chars.pop(loser)
        return winners, losers
        
    def resetPos(self):
        i = 0
        for char in self.chars.values():
            pos = round(environment.envSizes[0]*0.85/len(self.chars)*i,2)-round(environment.envSizes[0]*0.85/2,2)
            char.body.pos=vp.vector(pos,0,(environment.envSizes[2]*0.9)//2)
            char.idText.pos = char.body.pos
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
        self.foods.clear()
        
        for i in range(self.number):
            x = int(environment.envSizes[0]*0.75)
            z = int(environment.envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
        
dozenChar = Chars(25)
dozenFood = Foods(50)



times = 0
day = 0
while True:
    if environment.running:
        
        dozenChar.setPos(dozenFood)
        environment.info(dozenChar.chars)
        
        if times >=30*20:
            dozenChar.endofDay(dozenFood)
            times = 0
            day +=1
        if day >= 5:
            break
        
        times += 1
    vp.rate(30)

while True:
    pass