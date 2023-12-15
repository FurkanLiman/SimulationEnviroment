import math

canli = 15,20
yem = 0,30

xler =yem[0]-canli[0]
yler =yem[1]-canli[1]


sonuc = math.atan(xler/yler)
sonucderece = sonuc*(180/math.pi)

if yler>0 and xler>0:
    print("1.bölge")
elif yler>0 and xler<0:
    print("2.bölge")
elif yler<0 and xler<0:
    print("3.bölge")
elif yler<0 and xler>0:
    print("4.bölge")
#bana lazım olan 1 ve 2. bölgeler
print(sonucderece)


sonucradyan=45*math.pi/180
print(math.tan(sonucradyan))