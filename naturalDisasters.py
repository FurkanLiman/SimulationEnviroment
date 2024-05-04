import vpython as vp
import random
from environment import envSizes

# lethal disasters - permanent effect - red
# harmful disasters - permanent effect - yellow-orange
# instant disasters - not permanent effect - slowing, getting blind - another color
# all disasters must have posibilities with selection (user can select danger and frequency)
class Disasters:
    sizeRatio = [0.1,0.25]    # Minimum and maximum size range, relative to the entire area. 
    def __init__(self):
        
        areaRatio =  random.randint(int(self.sizeRatio[0]*100),int(self.sizeRatio[1]*100))/100
            
        area = int((envSizes[0]*envSizes[2]*areaRatio))
        self.sizeX = int((area**(0.5))*(random.randint(80,100)/100))
        self.sizeY= area//self.sizeX
        
        posXs = [(((-1)*envSizes[0]//2)+self.sizeX),((envSizes[0]//2)-self.sizeX)]
        posYs = [(((-1)*envSizes[2]//2)+self.sizeY),((envSizes[2]//2)-self.sizeY)]
        self.posX = random.randint(min(posXs),max(posXs))
        self.posY = random.randint(min(posYs),max(posYs))

        sec = random.randint(0,2) # burayı düzelt kullanıcıya bağla, arayüzden olasılıkları değiştirebilsinler 

        if sec == 0:
            self.lethalDisaster()
        elif sec == 1:
            self.harmfulDisaster()
        else:
            self.instantDisasters()
        
    def lethalDisaster(self):
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.sizeX,self.sizeY), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.red,
                                opacity = 0.5) # topla burayı yükseklikler dengesiz
            
    def harmfulDisaster(self):
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.sizeX,self.sizeY), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.orange,
                                opacity= 0.5) # topla burayı yükseklikler dengesiz

    def instantDisasters(self):
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.sizeX,self.sizeY), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.green,
                                opacity= 0.5) # topla burayı yükseklikler dengesiz
