import math

def viewAngle(visionAngle,creatureSize):
    visionRadian = (visionAngle*math.pi/180)/2 # düzelt hesap
    angleVision = math.tan(visionRadian) #hesap düzelt
    sizeX=creatureSize # hesapları düzelt
    sizeZ = 2*angleVision*sizeX #düzelt hesap
    sizeY = sizeZ/2
    
    return sizeX,sizeY,sizeZ 

def inSight(bodyfoodAngle,vision):
    
    return True # return true or false