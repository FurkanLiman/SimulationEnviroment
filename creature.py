import vpython as vp
from time import *
import random
from environment import envSizes
import mutationFactors
import math
import fovCalculation

class Creature:
    time = 0
    def __init__(self, idnumber, color=(0,0,1), speed=0.4, vision=45, allergyProtein=0, axis=(1,0,0), pos = (0,1,-35)):
        self.genomes = {
        "speed" : speed,
        "vision" : vision,
        # enviromental harshness
        # durability 
        }
        x,y,z = axis
        r,g,b= color
        posX,posY,posZ = pos
        self.hunger = False
        self.id = idnumber
        self.body = vp.ellipsoid(size = vp.vector(2,7,2), axis = vp.vector(x,y,z), color=vp.vector(r,g,b),pos=vp.vector(posX,posY,posZ))
        self.idText = vp.label(text=f"{idnumber}",color=vp.vector(r,g,b),pos=self.body.pos,line=True)
        sizeX,sizeY,sizeZ = fovCalculation.viewAngle(vision,self.body.size.x)
        self.angle = vp.cone(pos=self.body.pos, axis=self.body.axis*-1, size=vp.vector(sizeX,sizeY,sizeZ), color=self.body.color/2)
        
    
    def pos(self):
        if abs(self.body.pos.x) >= envSizes[0]/2 or abs(self.body.pos.z) >= envSizes[2]/2:
            self.body.axis *= -1 
        
        displacement = self.body.axis * self.genomes["speed"]
        self.body.pos += displacement
        
        self.idText.pos = self.body.pos
        self.idText.pos.y = self.body.size.y*0.75
        
        self.angle.pos = self.body.pos  #dikkatt pozisyonları düzelt görüş açısının canlı üzerindeki konumunu düzelt
        self.angle.pos.y += 3
        self.angle.axis = self.body.axis * -1
    

    def collide(self,foods):
        for food in foods.values():

            distances = food.body.pos - self.body.pos
            distancePythagor = (distances.x**2+distances.y**2+distances.z**2)**(0.5)
            
            if distances.z != 0:
                bodyfoodAngle =  math.atan(distances.x/distances.z)*(180/math.pi)
                # sıfıra bölme hatası bi tarama fonk oluştur bir radius içerisinde arat ve gördükleri içinden yakın olana hedef gönder
                
                if bodyfoodAngle <= (self.genomes["vision"]/2) and((distances.x>0 and distances.z>0)or(distances.x<0 and distances.z>0)):
                #yukarıdaki if direkt fovCalculation.insight() ile hesaplanacak
                
                    if distancePythagor<=(self.body.size.x+food.body.radius) and not food.eat:
                        print(f"{self.id} found food: {food.id}")
                        self.hunger = True 
                        food.body.color = vp.color.red
                        food.eat = True


    def searchFood(self,foods):
        if not self.hunger:
            self.time +=1
            if not self.time%10:
                randAxis = vp.vector(random.randint(0,200)/100-1,0,random.randint(0,200)/100-1)
                self.body.axis = randAxis
                self.pos()
            else:
                self.pos()
            self.collide(foods)
                    
    def mutation(self):
        mutationState,self = mutationFactors.mutationChance(self)
        if mutationState:
            self.body.color = vp.vector(random.randint(0,100)/100, random.randint(0,100)/100, random.randint(0,100)/100)    
            self.idText.color = self.body.color
    
    
class Food:
    def __init__(self, id,size=.75, pos=(0,0,0)):
        self.eat = False
        x,y,z=pos
        self.id = id
        self.body = vp.sphere(radius=size,pos=vp.vector(x,y,z),color= vp.color.green)