import vpython as vp
import time
import environment
import creature
import random
class Chars:
    chars = {}
    def __init__(self, number=10):

        for i in range(number):
            colors = (random.randint(0,100)/100, random.randint(0,100)/100, random.randint(0,100)/100)
            speed = random.randint(0,200)/100-1
            axiss = (random.randint(0,200)/100-1,0,random.randint(0,200)/100-1)
            pos = round(environment.envSizes[0]*0.85/number,2)*i-round(environment.envSizes[0]*0.85/2,2)
            char = creature.Creature(color=colors,speed=speed,axis=axiss, idnumber=i,pos=(pos,0,(environment.envSizes[2]*0.9)//2))
            self.chars[i]= char

    def setPos(self,foodlist):
        for char in self.chars.values():
            char.searchFood(foodlist.foods)
                
    def results(self):
        winners = []
        losers = []
        for char in self.chars.values():
            winners.append(char.id) if char.hunger else losers.append(char.id)
        return winners, losers
            
class Foods:
    foods = {}
    def __init__(self,number):
        for i in range(number):
            x = int(environment.envSizes[0]*0.75)
            z = int(environment.envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos, id=i)
            self.foods[i] = food
        
dozenChar = Chars(25)
dozenFood = Foods(10)



time = 0
while True:
    dozenChar.setPos(dozenFood)
    vp.rate(30)

    time += 1
    if time >=15*30:
        print("End of The Day")
        break

winners, losers = dozenChar.results()
print("Results:")
print("Winners:", winners)
print("Losers:", losers)

while True:
    pass
