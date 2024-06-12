import json
import os

Veri = {
    "Day":[],
    "Population" : [],
    "Winners": [],
    "Losers": [],
    "DisasterType": [],
    "speed": [],
    "vision": [],
    "visionRadius": [],
    "immunity": [],
    "durability": [],
    "mutationRate": []
}


def saveJsonWithUniqueName(data, directory, filename):
    base_name, extension = os.path.splitext(filename)
    unique_filename = filename
    counter = 1

    # Dosya adının benzersiz olup olmadığını kontrol et
    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    # JSON verisini dosyaya kaydet
    with open(os.path.join(directory, unique_filename), 'w') as json_file:
        json.dump(data, json_file, indent=4)


def writeFile():
    global Veri
    filePath = "results/aiData"
    fileName = f'{Veri["Day"][-1]}.json'
    if not os.path.exists(filePath):
        os.makedirs(filePath)
    
    saveJsonWithUniqueName(Veri,filePath, fileName)
    
    print(f"Veri {fileName} dosyasına başarıyla yazıldı.")

def collectData(day, lenWinners, lenLosers,isDisasterInDay,meanSpeed,meanVision,meanVisionRadius,meanImmunity,meanDurability,mutationFactors):
    global Veri 
    Veri["Day"].append(day)
    Veri["Population"].append(lenWinners+lenLosers)
    Veri["Winners"].append(lenWinners)
    Veri["Losers"].append(lenLosers)
    Veri["DisasterType"].append(isDisasterInDay)
    Veri["speed"].append(meanSpeed)
    Veri["vision"].append(meanVision)
    Veri["visionRadius"].append(meanVisionRadius)
    Veri["immunity"].append(meanImmunity)
    Veri["durability"].append(meanDurability)
    Veri["mutationRate"].append(mutationFactors)
    
    
    
    
