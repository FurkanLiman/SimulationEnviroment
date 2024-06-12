import vpython as vp
import random
from environment.environment import envSizes
from creature.mutationFactors import specs

# lethal disasters - permanent effect - red
# harmful disasters - permanent effect - yellow-orange
# instant disasters - not permanent effect - slowing, getting blind 
# all disasters must have posibilities with selection (user can select danger and frequency)
# chars in disaster will be marked
class Disasters:
    sizeRatio = [0.05,0.15]    # Minimum and maximum size range, relative to the entire area. 
    def __init__(self, disasterHarsness=0,disasterTime=720):
        
        areaRatio =  random.randint(int(self.sizeRatio[0]*100),int(self.sizeRatio[1]*100))/100
        area = int((envSizes[0]*envSizes[2]*areaRatio))
        self.radius = int(area**(0.5))
        
        posXs = [(((-1)*envSizes[0]//2)+self.radius),((envSizes[0]//2)-self.radius)]
        posYs = [(((-1)*envSizes[2]//2)+self.radius),((envSizes[2]//2)-self.radius)]
        
        self.posX = random.randint(min(posXs),max(posXs))
        self.posY = random.randint(min(posYs),max(posYs))

        self.disasterHarsness =  disasterHarsness
        self.disasterTime = disasterTime
        
        if self.disasterHarsness == 1:
            self.disasterHarsness = random.randint(11,30)/10
        
        self.lethalChars = []
        if self.disasterHarsness >= 2.8:
            self.lethalDisaster()
        elif self.disasterHarsness < 2.8 and  self.disasterHarsness>=2:
            self.harsnessLevel = (self.disasterHarsness-2)*3
            self.harmfulDisaster()
        elif self.disasterHarsness <2 and self.disasterHarsness >=1:
            self.harsnessLevel = (self.disasterHarsness-1)
            self.instantDisasters()
          
    def collideCheck(self, chars):
        self.disasterTime -= 1

        if self.disasterTime >0:
            charlist = []
            for id , char in list(chars.items()):
                distances = char.body.pos - self.body.pos
                distancePythagor = (distances.x**2+distances.y**2+distances.z**2)**(0.5)
                if  (distancePythagor<=(self.radius/2)):                
                    charlist.append(id)
                    
            if self.state == 2:
                leavin = [item for item in self.lethalChars if item not in charlist]
                enterin = [item for item in charlist if item not in self.lethalChars]
                self.lethalChars = charlist
                for id in enterin:
                    chars[id].updateAttribute(self.category, byfactor=1-self.harsnessLevel)
                for id in leavin:
                    chars[id].updateAttribute(self.category, byfactor=(1/(1-self.harsnessLevel)))
            else:
                for id in charlist:
                    if not chars[id].diseased:

                        if self.state==0: # lethal disaster    
                            chars[id].unVisible()
                            del chars[id].body
                            del chars[id].idText
                            del chars[id].angle
                            chars.pop(id)
                        elif self.state == 1: # harmful disaster
                            
                            if (self.immunity in chars[id].genomes["immunity"]) and (self.harsnessLevel <= chars[id].durability):
                                # bağ + , direnç +
                                chars[id].diseased[self.category] = [1-(self.harsnessLevel/6),False,self.immunity,False]
                                
                            elif not (self.immunity in chars[id].genomes["immunity"]) and (self.harsnessLevel <= chars[id].durability):
                                # bağ - , direnç +
                                chars[id].diseased[self.category] = [1-(self.harsnessLevel/3),False, self.immunity,False]
                            else:
                                # bağ - , direnç -
                                if random.randint(0,1):
                                    chars[id].diseased[self.category] = [1-(self.harsnessLevel/3),True, self.immunity,False]
                                    
                                else:
                                    print("ölüm")
                                    chars[id].unVisible()
                                    del chars[id].body
                                    del chars[id].idText
                                    del chars[id].angle
                                    chars.pop(id)
                            """
                            # canlı girdiği afetten sonra 3 şey olabilir:
                            # eğer bağışıklığı varsa ve durability yüksekse, hastalığı çok az etkiyle tur sonuna kadar sahip olur ve sonraki güne düzelir.
                            # eğer bağışıklığı yoksa ve durabilty yüksekse, o tur dezavantajlı kalıp sonraki tura düzelir ve bağışıklık kazanabilir.
                            # eğer bağışıklığı yoksa ve durability düşükse, şansa bağlı 2 seçenek var:
                            #   ya ölür, 
                            #   ya da yaşar ama özür kalıcı hale geçer ve yeni bir özürlü sülale oluşur."""

            return chars,True
        else:
            self.disasterTime = 0
            self.body.visible = False
            self.Text.visible = False
            del self.body
            del self.Text
            return chars,False
        
    def lethalDisaster(self):
        self.state = 0
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.radius,self.radius), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.red,
                                opacity = 0.5)
        self.Text = vp.label(text=f"Lethal ",color=vp.color.red,pos=self.body.pos,line=True)

    def harmfulDisaster(self):
        self.state = 1
        self.immunity = random.randint(specs["immunity"][0],specs["immunity"][1])
        keys = list(specs.keys())
        keys.remove("durability")
        self.category = random.choice(keys)
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.radius,self.radius), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.orange,
                                opacity= 0.5)
        self.Text = vp.label(text=f"{self.category} - {self.harsnessLevel:.2f}",color=vp.color.orange,pos=self.body.pos,line=True)

    def instantDisasters(self):
        self.state = 2
        keys = list(specs.keys())
        keys.remove("immunity")
        keys.remove("durability")
        self.category = random.choice(keys)
        self.body = vp.cylinder(pos=vp.vector(self.posX,1,self.posY),
                                size=vp.vector(2,self.radius,self.radius), 
                                axis=vp.vector(0,-1,0),
                                color= vp.color.yellow,
                                opacity= 0.5)
        self.Text = vp.label(text=f"{self.category} - {self.harsnessLevel:.2f}",color=vp.color.yellow,pos=self.body.pos,line=True)

