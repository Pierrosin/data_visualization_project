import plotly.graph_objects as go
import numpy as np

def swarmPlot(x, size, figSize=(1000, 500), xmin=0, xmax=4, ymin=-25, ymax=25, ystep=1, seed=0):
    np.random.seed(seed)
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
        closeIndexes = indexes[np.abs(x - xi) < rmax]
        closeIndexes = closeIndexes[closeIndexes < len(y)]
        xClose = x[closeIndexes] if len(closeIndexes) > 0  else []
        yClose = np.array(y)[closeIndexes] if len(closeIndexes) > 0  else []
        rClose = size[closeIndexes] if len(closeIndexes) > 0  else []
        while anyOverlapping(xi, yi, ri, xClose, yClose, rClose):
            yi+=ystep*dir
        y.append(yi)

    fig = go.Figure()
    kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y', 'fillcolor': '#a86022'}
    points = [go.layout.Shape(x0=x-r/ratio, y0=y-r, x1=x+r/ratio, y1=y+r, **kwargs) for x, y, r in zip(x, y, size)]
    fig.update_layout(shapes=points, width=figSize[0], height=figSize[1], margin=dict(l=20, r=20, t=20, b=20))
    fig.update_xaxes(range=[xmin, xmax])  
    fig.update_yaxes(range=[ymin, ymax])
    
    return fig