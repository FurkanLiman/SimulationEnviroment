import math
import random


def inSight(distances,bodyAxis,vision):
    bodyAngle=math.atan(bodyAxis.x/bodyAxis.z)*180/math.pi  if bodyAxis.z != 0 else 90
    if bodyAxis.x < 0 and bodyAxis.z > 0:
        bodyAngle = 360+bodyAngle
    elif bodyAxis.x <0 and bodyAxis.z < 0:
        bodyAngle = 180+bodyAngle
    elif bodyAxis.x >0 and bodyAxis.z <0:
        bodyAngle = 180+bodyAngle
    
    bodyfoodAngle =  math.atan(distances.x/distances.z)*(180/math.pi) if distances.z != 0 else 90
    if distances.x < 0 and distances.z > 0:
        bodyfoodAngle = 360+bodyfoodAngle
    elif distances.x <0 and distances.z < 0:
        bodyfoodAngle= 180+bodyfoodAngle
    elif distances.x >0 and distances.z <0:
        bodyfoodAngle = 180+bodyfoodAngle
    
    gap = abs(bodyfoodAngle-bodyAngle)
    if (gap <= (vision/2)):
        return (True,bodyfoodAngle)
    else:
        return (False, bodyfoodAngle)

def randomAxis():
    angle = random.randint(0,360)
    angleRadian = angle*math.pi/180
    axisX = math.sin(angleRadian)
    axisZ = math.cos(angleRadian)
    return axisX,axisZ
    