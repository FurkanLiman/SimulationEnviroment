import plotly.graph_objects as go
from plotly.subplots import make_subplots
from creature.mutationFactors import specs
import plotly.offline as pyo

def resultChart(EoDStats):

    specLimits = specs
    if len(list(EoDStats.values())):
        charSpecs = list(specLimits.keys())
        rowTotal = max(1, -(-len(EoDStats) // 5))
        colTotal = min(len(EoDStats), 5)
        chart = make_subplots(rows=rowTotal, cols=colTotal, subplot_titles=list(EoDStats.keys()),
                        specs=[[{'type': 'polar'}] * colTotal] * rowTotal)
        
        for i, (day, statics) in enumerate(EoDStats.items()):
            
            for j, spec in enumerate(specLimits.keys()):
                min_deger, max_deger = specLimits[spec]
                statics[j] = (statics[j] / (max_deger - min_deger)) * 100
            
            rowIndex = (i) // colTotal+ 1
            colIndex = (i) % colTotal + 1

            chart.add_trace(go.Scatterpolar(
                r=statics+ [statics[0]],
                theta=charSpecs + [charSpecs[0]],
                fill='toself',
                name=day
            ), row=rowIndex, col=colIndex)

            chart.update_polars(radialaxis_range=[0, 100], row=rowIndex, col=colIndex)
            
        chart.update_layout(
        showlegend=False,
        title="Daily Average Specification Statistics"
        )
        pyo.plot(chart,filename="results/radarChart.html")
