import plotly.express as px
from datetime import datetime

def get_arrondissement_hover_template():
    hover_template = (
        '<b>Espèce</b> : <span font-weight: normal">%{customdata[0]}</span><br>' +
        '<b>Date plantation</b> : <span font-weight: normal">%{customdata[1]}</span><br>' +
        '<b>Date relevé</b> : <span font-weight: normal">%{customdata[2]}</span><br>' +
        '<b>Diamètre tronc</b> : <span font-weight: normal">%{customdata[3]} cm</span><br>'
    )
    
    return hover_template

def getMap(data, arrondissement, critere, filter):
    especes, min_date_plantation, max_date_plantation, min_dhp, max_dhp = filter
    
    # Sélectionner les arbres de l'arrondissement
    data = data[data['ARROND_NOM'] == arrondissement]
    
    # Filtrer les données en fonction des espèces
    if especes:
        data = data[data['Essence_fr'].isin(especes)]
    
    # Filtrer les données en fonction des dates de plantation
    if min_date_plantation != None and max_date_plantation != None:
        data = data[(data['Date_plantation'] >= min_date_plantation) & (data['Date_plantation'] <= max_date_plantation)]
    
    # # Filtrer les données en fonction des dates de relevé
    # if min_date_releve and max_date_releve:
    #     data = data[(data['Date_releve'] >= min_date_releve) & (data['Date_releve'] <= max_date_releve)]
        
    # Filtrer les données en fonction des dates de relevé
    if min_dhp != None and max_dhp != None:
        data = data[(data['DHP'] >= min_dhp) & (data['DHP'] <= max_dhp)]
    
    # Légende de l'échelle de couleur    
    if critere == 'Date_plantation':
        title = 'Date de plantation'
    elif critere == 'Date_releve':
        title = 'Date de relevé'
    else:
        title = 'Diamètre du tronc (cm)'
        
    # Couleur des points en fonction du critère
    color = data[critere].dt.year if critere in ['Date_plantation', 'Date_releve'] else data[critere]
    
    fig = px.scatter_mapbox(data, color=color, lat='Latitude', lon='Longitude', 
                            zoom=12.5, color_continuous_scale='tempo', hover_data=['Essence_fr', 'Date_plantation_format', 'Date_releve_format', 'DHP'])
    fig.update_layout(mapbox_style="open-street-map", coloraxis_colorbar=dict(title=title))
    fig.update_layout(
        title=f"Vue de l'arrondissement {arrondissement}",
        title_x=0.5,
        coloraxis_colorbar_thickness=23,
        margin=dict(l=60, r=60, t=60, b=60),
    )
    fig.update_traces(hovertemplate=get_arrondissement_hover_template())
    # fig.show(config={'scrollZoom': True})
    
    return fig

# getMap(clean, 'Le Plateau-Mont-Royal', 'Date_plantation', (['Érable argenté', 'Frêne de Pennsylvanie'], datetime(1950, 1, 1), datetime(2000, 12, 31), datetime(2019, 1, 1), datetime(2023, 12, 31)))