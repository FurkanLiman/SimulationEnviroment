import random

mutationProbability = 0.5 #0-1
specs = {
"speed": [0,2], 
"vision" : [0,15]
}


def mutationChance(char):
    probInt = int(mutationProbability**(-1))
    result = random.randint(0,probInt)

    if result == 0:
        winnerSpec = chooseSpec()
        newSpec = getMutation(winnerSpec)
        print(f"{char.id}: Got Mutation for --{winnerSpec}-- old spec:{char.genomes[winnerSpec]} -- new:{newSpec}")
        char.genomes[winnerSpec] = newSpec
        return True, char
    else:
        return False, char

def chooseSpec():
    whichSpec = random.randint(0,len(specs)-1)
    specslist = list(specs.keys())
    return specslist[whichSpec]
    
def getMutation(winnerSpec):
    a = specs[winnerSpec][0]*100
    b= specs[winnerSpec][1]*100
    newSpec = random.randint(a,b)
    return newSpec/100
