import math
import random


def inSight(distances,bodyAxis,vision):
    bodyaci=math.atan(bodyAxis.x/bodyAxis.z)*180/math.pi  if bodyAxis.z != 0 else 90
    if bodyAxis.x < 0 and bodyAxis.z > 0:
        bodyaci = 360+bodyaci
    elif bodyAxis.x <0 and bodyAxis.z < 0:
        bodyaci = 180+bodyaci
    elif bodyAxis.x >0 and bodyAxis.z <0:
        bodyaci = 180+bodyaci
    
    bodyfoodAngle =  math.atan(distances.x/distances.z)*(180/math.pi) if distances.z != 0 else 90
    if distances.x < 0 and distances.z > 0:
        bodyfoodAngle = 360+bodyfoodAngle
    elif distances.x <0 and distances.z < 0:
        bodyfoodAngle= 180+bodyfoodAngle
    elif distances.x >0 and distances.z <0:
        bodyfoodAngle = 180+bodyfoodAngle
    
    fark = abs(bodyfoodAngle-bodyaci)
    if (fark <= (vision/2)):
        return (True,bodyfoodAngle)
    else:
        return (False, bodyfoodAngle)

def chooseCloserFood(food):
    pass

def randomAxis():
    angle = random.randint(0,360)
    angleRadian = angle*math.pi/180
    axisX = math.sin(angleRadian)
    axisZ = math.cos(angleRadian)
    return axisX,axisZ
    