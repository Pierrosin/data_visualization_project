import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.stats import linregress

# Calcule la vitesse moyenne de croissance du tronc des espèces d'arbres
def getGrowthPerSpecie(data):
    try:
        a, _, _, _, _ =  linregress(data['Age'], data['DHP'])
    except:
        tree = data.iloc[0]
        a = tree['DHP'] / tree['Age']
    return round(a*365,2)

# Calcule le diamètre de tronc moyen des espèces d'arbres 
def getMeanDHPPerSpecie(data):
    return data['DHP'].mean()

# Crée un swarmplot des espèces d'arbres avec la taille de bulle selon le diamètre de tronc moyen 
# et la position le long de l'axe des abscisses selon la vitesse moyenne de croissance du tronc
def swarm(data, figSize=(1400, 500), xmin=0, xmax=5, ymin=-25, ymax=25, ystep=0.5, color='#36749d', seed=1):
    np.random.seed(seed)
    
    # Pour chaque espèce, on calcule sa vitesse moyenne de croissance du tronc et diamètre de tronc moyen
    uniqueSpecies = pd.unique(data['Essence_fr'])
    species = []
    growth = []
    meanDHP = []
    nbTrees = []
    for specie in uniqueSpecies:
        buffer = data[data['Essence_fr'] == specie]
        buffer = buffer[['Date_plantation', 'Date_releve', 'DHP']].dropna()
        buffer['Age'] = (buffer['Date_releve'] - buffer['Date_plantation']).dt.days
        buffer = buffer[buffer['Age'] > 0]
        if len(buffer) > 0:
            nbTrees.append(len(buffer))
            species.append(specie)
            growth.append(getGrowthPerSpecie(buffer))
            meanDHP.append(getMeanDHPPerSpecie(buffer))
    
    # On retire les outliers
    swarm = pd.DataFrame({'specie': species, 'growth':growth, 'dhp':meanDHP, 'trees':nbTrees}).dropna()
    swarm = swarm[(swarm['growth'] > 0) & (swarm['growth'] < 5)]
    maxDHP = swarm['dhp'].max()
    swarm = swarm[swarm['dhp'] > maxDHP/10]
    species = sorted(swarm['specie'])
    
    # Calcul des tailles, positions x et couleurs des bulles
    swarm = swarm.sort_values('dhp', ascending=False)
    x = swarm['growth'].to_numpy()
    size = swarm['dhp'].to_numpy()/25
    mean_growth = swarm['growth'].mean()
    colors = swarm['specie'].apply(lambda x: color)
    
    # Ratio de hauteur/largeur des bulles
    ratio = figSize[0]*(ymax-ymin)/((figSize[1]-50)*(xmax-xmin))
    
    def isInEllipse(x, y, x0, y0, r1, r2):
        return ((x-x0)/r1)**2 + ((y-y0)/r2)**2 <= 1

    def isOverlapping(x1, y1, r1, x2, y2, r2):
        r12, r22 = r1, r2
        r1, r2 = r12/ratio, r22/ratio
        if isInEllipse(x1, y1, x2, y2, r2, r22) or isInEllipse(x2, y2, x1, y1, r1, r12):
            return True

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

    # Calcul des positions y des bulles
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

    # Création du swarmplot
    fig = go.Figure()
    kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y'}
    points = [go.layout.Shape(x0=x-r/ratio, y0=y-r, x1=x+r/ratio, y1=y+r, fillcolor=c, line=dict(width=1, color='black'), **kwargs) for x, y, r, c in zip(x, y, size, colors)]
    fig.update_layout(shapes=points, width=figSize[0], height=figSize[1], margin=dict(l=20, r=20, t=20, b=20), hoverlabel_bgcolor='rgb(42, 63, 95)', dragmode=False)
    fig.update_xaxes(range=[xmin, xmax])  
    fig.update_yaxes(range=[ymin, ymax], tickvals=[])
    
    # Ajout des hovers
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

    # Légende axe des abscisses
    fig.update_xaxes(title={'text': "<b>Vitesse moyenne de croissance du tronc (cm/an)</b>",
                            'font': dict(
                                size=17,
                                )},
                    dtick=0.5, side='top')
    
    # Ajout de la ligne verticale de moyenne globale
    fig.add_vline(x=mean_growth, line_width=2, line_dash="dash", line_color="black", \
                  annotation_text=f'<b>Moyenne globale</b> : <b>{round(mean_growth, 2)} cm/an</b>',\
                  annotation_position='top right')
    
    return fig, species, swarm

# Met en évidence une espèce d'arbre en grisant toutes les autres espèces
def swarmPlot(fig, swarm, highlight_specie=None, color='#36749d'):
    if highlight_specie:
        colors = swarm['specie'].apply(lambda x: color if x == highlight_specie else 'lightgray')
    else:
        colors = swarm['specie'].apply(lambda x: color)
        
    for i, color in enumerate(colors):
        fig.layout.shapes[i].fillcolor = color
    
    return fig