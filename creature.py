import vpython as vp
from time import *
import random
from environment import envSizes
import mutationFactors
import math
import fovCalculation

class Creature:
    time = 0
    def __init__(self, idnumber, color=(0,0,1), speed=0.3, vision=30, visionRadius=10, axis=(1,0,0), pos = (0,1,-35)):
        self.genomes = {
        "speed" : speed,
        "vision" : vision,
        "visionRadius": visionRadius
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
        acirad = vision*vp.pi/180
        aci1 = -(acirad)/2 + vp.pi/2
        aci2 = (acirad)/2 + vp.pi/2
        self.arc2D = vp.shapes.circle(radius=visionRadius,angle1=aci1, angle2=aci2)
        self.angle = vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,0.5,0)],shape= self.arc2D, opacity = 0.3, color = self.body.color/2)

    
    def pos(self):
        if abs(self.body.pos.x) >= envSizes[0]/2 or abs(self.body.pos.z) >= envSizes[2]/2:
            self.body.axis *= -1 
        
        displacement = self.body.axis * self.genomes["speed"]
        self.body.pos += displacement
        
        self.idText.pos = self.body.pos
        self.idText.pos.y = self.body.size.y*0.75
        
        self.angle.pos.x = (self.genomes["visionRadius"]/2)*self.body.axis.x + self.body.pos.x
        self.angle.pos.z = (self.genomes["visionRadius"]/2)*self.body.axis.z + self.body.pos.z
        
        self.angle.axis = self.body.axis

    def collide(self,foods):
        for food,distance,angle in foods:

            if distance <= (self.body.size.x+food.body.radius) and not food.eat:
                print(f"{self.id} found food: {food.id}")
                self.hunger = True 
                food.body.color = vp.color.red
                food.eat = True
        
    def foodsinSight(self,foods):
        foodlist = []
        for food in foods.values():
            distances = food.body.pos - self.body.pos
            distancePythagor = (distances.x**2+distances.y**2+distances.z**2)**(0.5)

            isinSight,angle = fovCalculation.inSight(distances, self.body.axis,self.genomes["vision"])
            if  isinSight and (distancePythagor<=self.genomes["visionRadius"]):                
                foodlist.append((food,distancePythagor,angle))
        return foodlist

    def goCloserFood(self, food):
        bodyaci=math.atan(self.body.axis.x/self.body.axis.z)*180/math.pi  if self.body.axis.z != 0 else 90
        if self.body.axis.x < 0 and self.body.axis.z > 0:
            bodyaci = 360+bodyaci
        elif self.body.axis.x <0 and self.body.axis.z < 0:
            bodyaci = 180+bodyaci
        elif self.body.axis.x >0 and self.body.axis.z <0:
            bodyaci = 180+bodyaci
        
        bodyfoodAngle = food[2]
        bodyaci = bodyfoodAngle
        angleRadian = bodyaci*math.pi/180
        axisX = math.sin(angleRadian)
        axisZ = math.cos(angleRadian)
        self.body.axis.x = axisX
        self.body.axis.z = axisZ


    def searchFood(self,foods):
        if not self.hunger:
            
            self.time +=1
            visibleFoods = self.foodsinSight(foods) #
            

            if visibleFoods != []:
                mindistance = visibleFoods[0][1]
                minfood = visibleFoods[0]
                for food,distance,angle in visibleFoods:
                    if distance < mindistance:
                        mindistance = distance
                        minfood = (food,distance,angle)       
                self.goCloserFood(minfood)
            else:
                if not self.time % 10:
                    # random değil ufak açılarla smooth dönüş ekle
                    axis = fovCalculation.randomAxis()
                    self.body.axis = vp.vector(axis[0],0,axis[1])
            self.pos()

            
            self.collide(visibleFoods)
                    
    def mutation(self):
        mutationState,winnerSpec,newSpec = mutationFactors.mutationChance()
        if mutationState:
            self.body.color = vp.vector(random.randint(0,100)/100, random.randint(0,100)/100, random.randint(0,100)/100)    
            self.idText.color = self.body.color
            print(f"{self.id}: Got Mutation for --{winnerSpec}-- old spec:{self.genomes[winnerSpec]} -- new:{newSpec}")
            self.genomes[winnerSpec] = newSpec
            if winnerSpec == "speed":
                self.genomes["speed"] = newSpec
            elif winnerSpec == "vision":
                self.genomes["vision"] = newSpec
                acirad = newSpec*vp.pi/180
                aci1 = -(acirad)/2 + vp.pi/2
                aci2 = (acirad)/2 + vp.pi/2
                self.arc2D = vp.shapes.circle(radius=self.genomes["visionRadius"],angle1=aci1, angle2=aci2, pos= [5,-20])
                self.angle = vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,1,0)],shape= self.arc2D, opacity = 0.5, color = self.body.color/2)
            elif winnerSpec == "visionRadius":
                self.genomes["visionRadius"] = newSpec
                acirad = self.genomes["vision"]*vp.pi/180
                aci1 = -(acirad)/2 + vp.pi/2
                aci2 = (acirad)/2 + vp.pi/2
                self.arc2D = vp.shapes.circle(radius=newSpec,angle1=aci1, angle2=aci2, pos= [5,-20])
                self.angle = vp.extrusion(path=[vp.vec(0,0,0), vp.vec(0,1,0)],shape= self.arc2D, opacity = 0.5, color = self.body.color/2)
            

class Food:
    def __init__(self, id,size=.75, pos=(0,0,0)):
        self.eat = False
        x,y,z=pos
        self.id = id
        self.body = vp.sphere(radius=size,pos=vp.vector(x,y,z),color= vp.color.green)
        #self.idText = vp.label(text=f"{id}",color=vp.color.green*.4,pos=self.body.pos,line=True)
