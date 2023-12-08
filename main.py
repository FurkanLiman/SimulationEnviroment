import vpython as vp
from time import *
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
            char = creature.Creature(color=colors,speed=speed,axis=axiss, idnumber=i)
            self.chars[i]= char

    def setPos(self):
        for char in self.chars.values():
            char.pos()
        
    def checkCollide(self,foods):
        for char in self.chars.values():
            char.collide(foods.foods)    
        
class Foods:
    foods = {}
    def __init__(self,number):
        for i in range(number):
            x = int(environment.envSizes[0]*0.75)
            z = int(environment.envSizes[2]*0.75)
            pos = (random.randint(0,x)-x//2,0,random.randint(0,z)-z//2)
            food = creature.Food(pos=pos)
            self.foods[i] = food
        
dozenChar = Chars(20)
dozenFood = Foods(12)
while True:
    dozenChar.setPos()
    dozenChar.checkCollide(dozenFood)
    vp.rate(30)