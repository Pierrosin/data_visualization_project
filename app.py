
# -*- coding: utf-8 -*-

import json

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import preprocess
import choropleth
import arrond_map
import bar_chart
import swarmplot
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning) 
# import bubble

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

server = app.server



# Fichier geojson pour le choropleth
with open('assets/montreal.json', encoding='utf-8') as data_file:
    montreal_data = json.load(data_file)

# Fichier contenant les données sur les arbres
data = pd.read_csv('assets/arbres-publics.csv')

data = preprocess.removeOutliers(data)
data = preprocess.preprocess_df(data)
species = preprocess.getSpeciesList(data)

locations = preprocess.get_neighborhoods(montreal_data)

date_plantation_min = data['Date_plantation'].min()
date_plantation_max = data['Date_plantation'].max()

dhp_min = data['DHP'].min()
dhp_max = data['DHP'].max()

arrondissement = 'Le Plateau-Mont-Royal'
especes = sorted(data['Essence_fr'].unique())

nb_arbres_arrondissement = preprocess.get_nb_trees_district(data, date_plantation_min, date_plantation_max, dhp_min, dhp_max)
missing_arrondissement = preprocess.get_missing_districts(nb_arbres_arrondissement, locations)
data_arrondissement = preprocess.add_density(nb_arbres_arrondissement, 'assets/montreal.json')
choropleth_fig = choropleth.get_choropleth(data_arrondissement, missing_arrondissement, montreal_data, densite=False)
carte_arrond = arrond_map.getMap(data, arrondissement, 'Date_plantation', (None, None, None, None, None))

bar_chart_ville = bar_chart.draw_bar_chart(data, None, 'Rue', True)
bar_chart_arrond = bar_chart.draw_bar_chart(data, arrondissement, 'Rue', True)

swarm = swarmplot.swarm(data)
swarm_plot = swarmplot.swarmPlot(swarm)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Les arbres de la Ville de Montréal'),
    ]),
    html.Main(className='viz-container', children=[
        html.Div(id='maps', children=[
            html.Div(id='filter', children=[
                dcc.Dropdown(id='specie',
                    options=species,
                    placeholder='Espèces',
                    multi=True,
                ),
                html.Div(id='date', children=[
                    html.H6('Date de plantation'),
                    dcc.RangeSlider(
                        id='dateSlider', className='slider',
                        min=1960,
                        max=2023,
                        step=1,
                        value=[1960, 2023],
                        allowCross=False,  
                        marks=None,  
                        tooltip={
                            "always_visible": True,
                            "placement": "bottom",
                            "style": {"color": "LightSteelBlue", "fontSize": "15px"},
                        },
                    ),
                ]),
                html.Div(id='diametre', children=[
                    html.H6('Diamètre du tronc'),
                    dcc.RangeSlider(
                        id='diametreSlider', className='slider',
                        min=0,
                        max=300,
                        step=1,
                        value=[0, 300],
                        allowCross=False,  
                        marks=None, 
                        tooltip={
                            "always_visible": True,
                            "placement": "bottom",
                            "style": {"color": "LightSteelBlue", "fontSize": "15px"},
                        },
                    ),
                ])
                
                
            ]),
            
            html.Div(id='total', children=[
                        # Div du choroplethe
                        html.Div(id='div_critere_choropleth', children=[
                            dcc.Dropdown(id='critere_choropleth',
                                options=["Nombre d'arbres", "Densité d'arbres"],
                                value="Nombre d'arbres",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "50%"},),
                        dcc.Graph(figure=choropleth_fig, id='choropleth',
                            config=dict(
                            scrollZoom=False, displayModeBar=False))       
            ]),

            html.Div(id='arrond', children=[
                        # Div de la carte de l'arrondissement
                        html.Div(id='div_critere_carte_arrond', children=[
                            dcc.Dropdown(id='critere_carte_arrond',
                                options={"Date_plantation": "Date de plantation",
                                         "Date_releve": "Date de relevé",
                                         "DHP": "Diamètre du tronc"},
                                value="Date_plantation",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "50%"},),
                        dcc.Graph(figure=carte_arrond, id='carte_arrond',
                            config=dict(
                            scrollZoom=True, displayModeBar=False))       
            ]),
        ]),
        html.Div(id='barCharts', children=[
            html.Div(id='divBarChartVille', children=[
                        html.Div(id='div_critere_bar_chart_ville', children=[
                            dcc.Dropdown(id='critere_bar_chart_ville',
                                options={"Rue": "Rues",
                                         "Emplacement": "Emplacements",
                                         "Essence_fr": "Espèces"},
                                value="Rue",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "50%"},),
                        dcc.Graph(figure=bar_chart_ville, id='barChartVille',
                            config=dict(
                            scrollZoom=False, displayModeBar=False))       
            ]),

            html.Div(id='DivBarChartArrond', children=[
                        html.Div(id='div_critere_bar_chart_arrond', children=[
                            dcc.Dropdown(id='critere_bar_chart_arrond',
                                options={"Rue": "Rues",
                                         "Emplacement": "Emplacements",
                                         "Essence_fr": "Espèces"},
                                value="Rue",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "50%"},),
                        dcc.Graph(figure=bar_chart_arrond, id='barChartArrond',
                            config=dict(
                            scrollZoom=False, displayModeBar=False))       
            ]),
        ]),
        html.Div(id='swarm', children=[
                    html.Div(id='div_espece_swarm', children=[
                        dcc.Dropdown(id='espece_swarm',
                            options=especes,
                            placeholder='Espèce',
                            multi=False,
                            searchable=True,
                            clearable=True)
                        ], 
                            style={"margin" : "10px", "width": "50%"}),
                    dcc.Graph(figure=swarm_plot, id='swarm_plot',
                        config=dict(
                        scrollZoom=False, displayModeBar=False))       
        ])
    ])
])


@app.callback(
    Output('choropleth', 'figure'),
    Output('carte_arrond', 'figure'),
    Output('barChartVille', 'figure'),
    Output('barChartArrond', 'figure'),
    Input('choropleth', 'clickData'),
    Input('critere_choropleth', 'value'),
    Input('critere_carte_arrond', 'value'),
    Input('dateSlider', 'value'),
    Input('diametreSlider', 'value'),
    Input('specie', 'value'),
    Input('critere_bar_chart_ville', 'value'),
    Input('critere_bar_chart_arrond', 'value'),
    prevent_initial_call=True
)
def update_maps(clickData, critere_choropleth, critere_carte_arrond, date_range, dhp_range, species, critere_bar_chart_ville, critere_bar_chart_arrond):
    global arrondissement
    
    densite = critere_choropleth == "Densité d'arbres"
    nb_arbres_arrondissement = preprocess.get_nb_trees_district(data, pd.to_datetime(str(date_range[0]), format='%Y'), \
                                                                pd.to_datetime(str(date_range[1] + 1), format='%Y'), \
                                                                dhp_range[0], dhp_range[1], species)
    missing_arrondissement = preprocess.get_missing_districts(nb_arbres_arrondissement, locations)
    data_arrondissement = preprocess.add_density(nb_arbres_arrondissement, 'assets/montreal.json')
    choropleth_updated = choropleth.get_choropleth(data_arrondissement, missing_arrondissement, montreal_data, densite=densite)
        
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'choropleth' and clickData is not None:
        arrondissement = clickData['points'][0]['location']
                
    arrond_map_updated = arrond_map.getMap(data, arrondissement, critere_carte_arrond, (species, pd.to_datetime(str(date_range[0]), format='%Y'), pd.to_datetime(str(date_range[1] + 1), format='%Y'), dhp_range[0], dhp_range[1]))
    
    bar_chart_ville_updated = bar_chart.draw_bar_chart(data, None, critere_bar_chart_ville, True)
    bar_chart_arrond_updated = bar_chart.draw_bar_chart(data, arrondissement, critere_bar_chart_arrond, True)
    
    return choropleth_updated, arrond_map_updated, bar_chart_ville_updated, bar_chart_arrond_updated


@app.callback(
    Output('swarm_plot', 'figure'),
    Input('espece_swarm', 'value'),
    prevent_initial_call=True
)
def update_swarm(espece_swarm):
    swarm_plot_updated = swarmplot.swarmPlot(swarm, espece_swarm)
    
    return swarm_plot_updated

if __name__ == '__main__':
    app.run_server(debug=True)