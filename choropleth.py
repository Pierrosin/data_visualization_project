import plotly.express as px

def choropleth_hovertemplate() : 
    hover_template = "<b>%{customdata[0]}</b><br>" + \
                     "<b>Nombre d'arbres</b>: %{customdata[1]}<br>" + \
                     "<b>Densité d'arbres</b>: %{customdata[2]} arbres par km<sup>2</sup><br>"
    return hover_template + "<extra></extra>"

def choropleth_hovertemplate_no_data() : 
    hover_template = "<b>%{customdata[0]}</b><br>" + \
                     "Pas de donnée"
    return hover_template + "<extra></extra>"

def get_choropleth(data_arrondissement, missing_data, montreal_data, densite=False) : 

    if densite : 
        color = 'Densite'
        title = "Nombre d'arbres <br> par km<sup>2</sup>"
    else : 
        color = 'Nombre_Arbres'
        title="Nombre d'arbres"

    fig = px.choropleth_mapbox(data_arrondissement, geojson=montreal_data, color=color,
                            locations="ARROND_NOM", featureidkey="properties.NOM", color_continuous_scale=px.colors.sequential.Greens,
                            center={"lat": 45.569260, "lon": -73.727014},
                            mapbox_style="carto-positron", zoom=8.7, hover_data=["ARROND_NOM", "Nombre_Arbres", "Densite"])

    missing_areas = px.choropleth_mapbox(missing_data, geojson=montreal_data, color="Nombre_Arbres",color_discrete_sequence =['#CDD1C4'],
                                        locations="ARROND_NOM", featureidkey="properties.NOM",
                                        center={"lat": 45.569260, "lon": -73.707014}, hover_data=["ARROND_NOM", "Nombre_Arbres", "Densite"])

    fig.update_traces(
        hovertemplate=choropleth_hovertemplate()
    )

    for trace in missing_areas.data:
        trace.hovertemplate = choropleth_hovertemplate_no_data()
        fig.add_trace(trace)


    fig.update_layout(
        title="Vue de la Ville de Montréal",
        title_x=0.5,
        coloraxis_colorbar_thickness=23,
        coloraxis_colorbar=dict(title=title),
        coloraxis_colorbar_y=0.60,
        legend=dict(y=0),
        margin=dict(l=60, r=60, t=60, b=60),
    )
    
    return fig
