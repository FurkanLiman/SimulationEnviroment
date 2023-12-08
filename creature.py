import vpython as vp
from time import *
from environment import envSizes

class Creature:
    def __init__(self, idnumber, color=(0,0,1), speed=0.1, axis=(1,0,0)):
        self.speed = speed
        x,y,z = axis
        r,g,b= color
        self.id = idnumber
        self.body = vp.ellipsoid(size = vp.vector(2,7,2), axis = vp.vector(x,y,z), color=vp.vector(r,g,b))
        self.idText = vp.text(text=f"{idnumber}",align="center",color=vp.vector(r,g,b))


    def pos(self):
        if abs(self.body.pos.x) > envSizes[0]/2 or abs(self.body.pos.y) > envSizes[1]/2 or abs(self.body.pos.z) > envSizes[2]/2:
            pass
        else:
            positions = self.body.pos
            disX,disY,disZ=self.displacement()
            posX=positions.x+disX
            posY=positions.y+disY
            posZ=positions.z+disZ
            self.body.pos = vp.vector(posX,posY,posZ)
            self.idText.pos = self.body.pos
            self.idText.pos.y = self.body.size.y
    
    def displacement(self):
        axiss=self.body.axis
        x = self.speed*axiss.x
        y = self.speed*axiss.y
        z = self.speed*axiss.z
        return x,y,z
    
    def collide(self,foods):
        for food in foods.values():
            charX = self.body.pos.x
            charY = self.body.pos.y
            charZ = self.body.pos.z
            foodX = food.body.pos.x
            foodY = food.body.pos.y
            foodZ = food.body.pos.z
            distanceX = abs(foodX-charX)
            distanceY = abs(foodY-charY)
            distanceZ = abs(foodZ-charZ)
            distancePythagor = (distanceX**2+distanceY**2+distanceZ**2)**(0.5)
            if distancePythagor<=(self.body.size.z/2+food.body.radius):
                print("Collison Detected id:",self.id)
                return id
                
    
    
class Food:
    def __init__(self, size=.75, pos=(0,0,0)):
        x,y,z=pos
        self.body = vp.sphere(radius=size,pos=vp.vector(x,y,z),color= vp.color.green)