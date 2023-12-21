import random

mutationProbability = 0.5 #0-1
specs = {
"speed": [0.2,2], 
"vision" : [10,90],
"visionRadius":[2,30]
}


def mutationChance():
    probInt = int(mutationProbability**(-1))
    result = random.randint(0,probInt)

    if result == 0:
        winnerSpec = chooseSpec()
        newSpec = getMutation(winnerSpec)
        
        return True, winnerSpec,newSpec
    else:
        return False, None, None

def chooseSpec():
    whichSpec = random.randint(0,len(specs)-1)
    specslist = list(specs.keys())
    return specslist[whichSpec]
    
def getMutation(winnerSpec):
    a = specs[winnerSpec][0]*100
    b= specs[winnerSpec][1]*100
    newSpec = random.randint(a,b)
    return newSpec/100
