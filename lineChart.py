import matplotlib.pyplot as plt
import numpy as np
from mutationFactors import specs

def lineResult(EoDStats):
    
    if len(list(EoDStats.values())):
        days = list(EoDStats.keys())
        allStats = list(EoDStats.values())

        plt.figure(figsize=(10, 10))

        plt.subplot(2, 1, 1)
        
        for i, category in enumerate(specs.keys()):
            plt.plot(days, [data[i] for data in allStats], label=category)

        plt.title('Daily Average Specifications')
        plt.xlabel('Day')
        plt.ylabel('Specs')
        plt.legend()
        plt.grid(True)
        plt.xticks(days)

        plt.subplot(2, 1, 2)

        changeRates = []
        for i in range(len(allStats[0])):
            changeRates.append(allStats[-1][i] /allStats[0][i])

        plt.bar(range(1, len(changeRates) + 1),changeRates, color='skyblue', width=0.3)
        plt.title('Attributes Change Rate')
        plt.xlabel('Attributes')
        plt.ylabel('Rates')
        plt.xticks(range(1, len(changeRates) + 1), [f"{i}" for i in specs.keys()])
        plt.grid(axis='y')

        plt.tight_layout()
        plt.savefig("results/lineChart.png")
        plt.show(block=False)
    

