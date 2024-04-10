import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import linregress

def getGrowthPerSpecie(data, specie):
    buffer = data[data['Essence_fr'] == specie]
    growth = pd.DataFrame({'Plantation':buffer['Date_plantation'], 'Releve': buffer['Date_releve'], 'Diametre':buffer['DHP']}).dropna()

    growth['Plantation'] = pd.to_datetime(growth['Plantation'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    growth['Releve'] = pd.to_datetime(growth['Releve'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    growth = growth.dropna()
    growth['Age'] = ((growth['Releve'] - growth['Plantation']) / np.timedelta64(1, 'Y')).astype(int)
    a, b, r, _, _ =  linregress(growth['Age'], growth['Diametre'])
    
    return a, b, r

def getMeanDHPPerSpecie(data, specie):
    buffer = data[data['Essence_fr'] == specie]
    meanDHP = buffer['DHP'].mean()
    
    return meanDHP

def swarm(data):
    species = pd.unique(data['Essence_fr'])
    growth = []
    meanDHP = []
    nbTrees = []
    
    for specie in species:
        try:
            a, b, r = getGrowthPerSpecie(data, specie)
            growth.append(a)
        except Exception as e:
            tree = data[data['Essence_fr']==specie].iloc[0]
            a = tree['DHP'] / (tree['Date_releve'].year - tree['Date_plantation'].year)
            growth.append(a)
        
        meanDHP.append(getMeanDHPPerSpecie(data, specie))
        nbTrees.append(data[data['Essence_fr'] == specie].shape[0])
    
    swarm = pd.DataFrame({'specie': species, 'growth':growth, 'dhp':meanDHP, 'trees':nbTrees})
    swarm = swarm[(swarm['growth'] > 0) & (swarm['growth'] < 5)]
    maxDHP = swarm['dhp'].max()
    swarm = swarm[swarm['dhp'] > maxDHP/10].sort_values('dhp', ascending=False)
    
    return swarm

def swarmPlot(swarm, highlight_specie=None, figSize=(1400, 500), xmin=0, xmax=5, ymin=-25, ymax=25, ystep=0.5, color='#36749d', seed=0):
    np.random.seed(seed)
    
    x = swarm['growth'].to_numpy()
    size = swarm['dhp'].to_numpy()/30
    
    if highlight_specie:
        colors = swarm['specie'].apply(lambda x: color if x == highlight_specie else 'lightgray')
    else:
        colors = swarm['specie'].apply(lambda x: color)
    
    ratio = figSize[0]*(ymax-ymin)/(figSize[1]*(xmax-xmin))
    
    def isInEllipse(x, y, x0, y0, r1, r2):
        return ((x-x0)/r1)**2 + ((y-y0)/r2)**2 <= 1

    def isOverlapping(x1, y1, r1, x2, y2, r2):
        r12, r22 = r1, r2
        r1, r2 = r12/ratio, r22/ratio
        theta = np.arctan((y2-y1)/(x2-x1))
        if x2 < x1:
            theta += np.pi
        x3 = r1*r12 / np.sqrt(r12**2 + (r1*np.tan(theta))**2)
        if x2 < x1:
            x3 = -x3
        y3 = y1 + x3*np.tan(theta)
        x3 = x1 + x3
        return isInEllipse(x3, y3, x2, y2, r2, r22)

    def anyOverlapping(x, y, r, xClose, yClose, rClose):
        for x2, y2, r2 in zip(xClose, yClose, rClose):
            if isOverlapping(x, y, r, x2, y2, r2):
                return True
        return False

    rmax = size.max()
    indexes = np.arange(len(x))
    y = []
    for xi, ri in zip(x, size):
        yi = 0
        dir = np.random.choice([1, -1])
        closeIndexes = indexes[np.abs(x - xi) < 2*rmax/ratio]
        closeIndexes = closeIndexes[closeIndexes < len(y)]
        xClose = x[closeIndexes] if len(closeIndexes) > 0  else []
        yClose = np.array(y)[closeIndexes] if len(closeIndexes) > 0  else []
        rClose = size[closeIndexes] if len(closeIndexes) > 0  else []
        while anyOverlapping(xi, yi, ri, xClose, yClose, rClose):
            yi+=ystep*dir
        y.append(yi)

    fig = go.Figure()
    kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y'}
    points = [go.layout.Shape(x0=x-r/ratio, y0=y-r, x1=x+r/ratio, y1=y+r, fillcolor=c, line=dict(width=1, color='black'), **kwargs) for x, y, r, c in zip(x, y, size, colors)]
    fig.update_layout(shapes=points, width=figSize[0], height=figSize[1], margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(range=[xmin, xmax])  
    fig.update_yaxes(range=[ymin, ymax], tickvals=[])
    
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='markers',
        marker=dict(size=size*0),
        customdata=swarm[['specie', 'growth', 'dhp', 'trees']],
        hovertemplate=('<b>Espèce</b> : %{customdata[0]}<br>' +
                      '<b>Nombre d\'arbres</b> : %{customdata[3]}<br>' +
                      '<b>Diamètre du tronc moyen</b> : %{customdata[2]:.2f} cm<br>' +
                      '<b>Vitesse de croissance du tronc</b> : %{customdata[1]:.2f} cm/an<br>'
                      ) + "<extra></extra>"
    ))

    fig.update_xaxes(title="Vitesse moyenne de croissance du tronc (cm/an)", dtick=0.5, side='top')
    
    return fig