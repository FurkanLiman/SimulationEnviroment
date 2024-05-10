import matplotlib.pyplot as plt
from mutationFactors import specs

def lineResult(EoDStats, population):
    
    if len(list(EoDStats.values())):
        days = list(EoDStats.keys())
        allStats = list(EoDStats.values())

        plt.figure(figsize=(10, 10))

        plt.subplot(3, 1, 1)
        
        for i, category in enumerate(specs.keys()):
            plt.plot(days, [data[i] for data in allStats], label=category)

        plt.title('Daily Average Specifications')
        plt.xlabel('Day')
        plt.ylabel('Specs')
        plt.legend()
        plt.grid(True)
        plt.xticks(days)

        plt.subplot(3, 1, 2)

        changeRates = []
        for i in range(len(allStats[0])):
            changeRates.append(allStats[-1][i] /allStats[0][i])

        plt.bar(range(1, len(changeRates) + 1),changeRates, color='skyblue', width=0.3)
        plt.title('Attributes Change Rate')
        plt.xlabel('Attributes')
        plt.ylabel('Rates')
        plt.xticks(range(1, len(changeRates) + 1), [f"{i}" for i in specs.keys()])
        plt.grid(axis='y')

        plt.subplot(3, 1, 3)

        dayss = list(population.keys())
        populations = []
        disastersLethal =[]
        disastersHarmful =[]
        disastersInstant = []
        for days,[total, winner, loser, isdisaster] in population.items():
            populations.append([total,winner,loser])
            if isdisaster == 1:
                disastersLethal.append(total)
                disastersHarmful.append(None)
                disastersInstant.append(None)
            elif isdisaster ==2:
                disastersLethal.append(None)
                disastersHarmful.append(total)
                disastersInstant.append(None)
            elif isdisaster ==3:
                disastersLethal.append(None)
                disastersHarmful.append(None)
                disastersInstant.append(total)
            else:
                disastersLethal.append(None)
                disastersHarmful.append(None)
                disastersInstant.append(None)
                    
        plt.plot(dayss,populations,label=["population","winners","losers"])
        plt.scatter(dayss, disastersLethal, color='red', label='Lethal Disasters',s=150)
        plt.scatter(dayss, disastersHarmful, color='orange', label='Harmful Disasters',s=150)
        plt.scatter(dayss, disastersInstant, color='yellow', label='Instant Disasters',s=150)

        plt.title('Daily pop')
        plt.xlabel('Day')
        plt.ylabel('pop')
        plt.legend()
        plt.grid(True)
        plt.xticks(dayss)
        
        plt.tight_layout()
        plt.savefig("results/lineResult.png")
        plt.show(block=False)
    
def populationDistribution(chars):
    
    if len(list(chars.keys())):
       
        variables = list(chars[list(chars.keys())[0]].genomes.keys())

        plt.figure(figsize=(15, 5))

        for i, (var, params) in enumerate(specs.items(), start=1):
            
            minVal,maxVal = params
            intervalSize = (maxVal - minVal) / 10
            intervals = [(minVal + i * intervalSize, minVal + (i + 1) * intervalSize) for i in range(10)]

            counts = [0] * 10
            for value in [chars[id].genomes[var] for id in chars]:
                if var == "immunity":
                    value = len(value)
                for j, (start, end) in enumerate(intervals):
                    if start <= value < end:
                        counts[j] += 1
                        break

            plt.subplot(1, len(variables), i)
            plt.bar(range(1, 11), counts, color='skyblue')
            plt.title(var)
            plt.xlabel('Attribute')
            plt.ylabel('Population')
            plt.xticks(range(1, 11), [f"{interval[0]:.2f}-{interval[1]:.2f}" for interval in intervals], rotation=45)

        plt.tight_layout()
        plt.savefig("results/populationDistribution.png")
        plt.show(block=False)
