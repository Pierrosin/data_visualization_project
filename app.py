
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
arrondissements = sorted(pd.unique(data['ARROND_NOM']))

nb_arbres_arrondissement = preprocess.get_nb_trees_district(data, date_plantation_min, date_plantation_max, dhp_min, dhp_max)
missing_arrondissement = preprocess.get_missing_districts(nb_arbres_arrondissement, locations)
data_arrondissement = preprocess.add_density(nb_arbres_arrondissement, 'assets/montreal.json')
choropleth_fig = choropleth.get_choropleth(data_arrondissement, missing_arrondissement, montreal_data, densite=False)
carte_arrond = arrond_map.getMap(data, arrondissement, 'Date_plantation', (None, None, None, None, None))

bar_chart_ville = bar_chart.draw_bar_chart(data, None, 'Rue', True)
bar_chart_arrond = bar_chart.draw_bar_chart(data, arrondissement, 'Rue', True)

swarm_plot, especes, swarm = swarmplot.swarm(data)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1(html.Strong('Les arbres de la Ville de Montréal')),
    ]),
    html.Main(className='viz-container', children=[
        html.Div(id='maps', children=[
            html.Div(id='filter', children=[
                html.Div(id='text_filter', children=[
                    html.P('Filtrer par :')
                ]),
                dcc.Dropdown(id='specie',
                    options=species,
                    placeholder='Espèce d\'arbre',
                    multi=False,
                    style={"margin-top" : "3px"}
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
                    html.H6('Diamètre du tronc (cm)'),
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
                ]),
                html.Button(id='btn_info', n_clicks=0, children='?')
            ]),
            
            html.Div(id='total', children=[
                        dcc.Graph(figure=choropleth_fig, id='choropleth',
                            config=dict(
                            scrollZoom=False, displayModeBar=False)),              
                        html.Div(id='div_critere_choropleth', children=[
                            html.Div(id='text_critere_choropleth', children=[
                                html.P('Critère d\'échelle :')
                            ]),
                            dcc.Dropdown(id='critere_choropleth',
                                options=["Nombre d'arbres", "Densité d'arbres"],
                                value="Nombre d'arbres",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "47%", "height": "36px"},)    
            ]),

            html.Div(id='arrond', children=[
                        dcc.Graph(figure=carte_arrond, id='carte_arrond',
                            config=dict(
                            scrollZoom=True, displayModeBar=False)),
                        html.Div(id='div_critere_carte_arrond', children=[
                            html.Div(id='text_critere_carte_arrond', children=[
                                html.P('Critère d\'échelle :')
                            ]),
                            dcc.Dropdown(id='critere_carte_arrond',
                                options={"Date_plantation": "Date de plantation",
                                         "Date_releve": "Date de relevé",
                                         "DHP": "Diamètre du tronc"},
                                value="Date_plantation",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False),
                            html.Div(id='text_arr_carte_arrond', children=[
                                html.P('Arrondissement :')
                            ]),
                            dcc.Dropdown(id='arr_carte_arrond',
                                options=arrondissements,
                                value="Le Plateau-Mont-Royal",
                                multi=False,
                                searchable=False,
                                clearable=False)
                        ],
                        style={"margin" : "10px", "width": "50%", "height": "36px"},)     
            ]),
        ]),
        html.Div(id='barCharts', children=[
            html.Div(id='divBarChartVille', children=[
                        dcc.Graph(figure=bar_chart_ville, id='barChartVille',
                            config=dict(
                            scrollZoom=False, displayModeBar=False)),
                        html.Div(id='div_critere_bar_chart_ville', children=[
                            html.Div(id='text_critere_bar_chart_ville', children=[
                                html.P('Critère classement :')
                            ]),
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
                        style={"margin" : "10px", "width": "47%", "height": "36px"},)       
            ]),

            html.Div(id='DivBarChartArrond', children=[
                        dcc.Graph(figure=bar_chart_arrond, id='barChartArrond',
                            config=dict(
                            scrollZoom=False, displayModeBar=False)),
                        html.Div(id='div_critere_bar_chart_arrond', children=[
                            html.Div(id='text_critere_bar_chart_arrond', children=[
                                html.P('Critère classement :')
                            ]),
                            dcc.Dropdown(id='critere_bar_chart_arrond',
                                options={"Rue": "Rues",
                                         "Emplacement": "Emplacements",
                                         "Essence_fr": "Espèces"},
                                value="Rue",
                                placeholder='Critère',
                                multi=False,
                                searchable=False,
                                clearable=False),
                            html.Div(id='text_arr_bar_chart_arrond', children=[
                                html.P('Arrondissement :')
                            ]),
                            dcc.Dropdown(id='arr_bar_chart_arrond',
                                options=arrondissements,
                                value="Le Plateau-Mont-Royal",
                                multi=False,
                                searchable=False,
                                clearable=False)
                            ],
                            style={"margin" : "10px", "width": "50%", "height": "36px"},),
                        html.Button(id='btn_info_2', n_clicks=0, children='?')
            ]),
        ]),
        html.Div(id='swarm', children=[
                    dcc.Dropdown(id='espece_swarm',
                            options=especes,
                            placeholder='Trouver une espèce d\'arbre',
                            multi=False,
                            searchable=True,
                            clearable=True),
                    
                    html.Button(id='btn_info_3', n_clicks=0, children='?'),
                    
                    html.Div(id='texte_especes_arbres', style={'display': 'flex', 'justify-content': 'flex-end', 'align-items': 'center', "fontSize": "10px"}, children=[
                        html.H2("Espèces\nd'arbres")
                    ]),

                    dcc.Graph(figure=swarm_plot, id='swarm_plot',
                        config=dict(
                        scrollZoom=False, displayModeBar=False)),

                    html.Div(id='swarm_legend',
                    style={'display': 'flex'}, children=[
                        html.P([html.Strong('La taille des bulles'), ' correspond au diamètre du tronc moyen de l\'espèce : ']),
                        html.Div(id='bulle5', children=[
                            html.Div(style={'width': 10, 'height': 10,'border':'1px solid', 'border-radius': 5, 'backgroundColor':'lightgray', 'margin':'auto'}),
                            html.P("15cm"),
                        ]),

                        html.Div(id='bulle10', children=[
                            html.Div(style={'width': 20, 'height': 20,'border':'1px solid', 'border-radius': 10, 'backgroundColor':'lightgray', 'margin':'auto'}),
                            html.P("30cm"),
                        ]),

                        html.Div(id='bulle20', children=[
                            html.Div(style={'width': 30, 'height': 30,'border':'1px solid', 'border-radius': 15, 'backgroundColor':'lightgray', 'margin':'auto'}),
                            html.P("45cm"),
                            
                        ]),

                        html.Div(id='bulle30', children=[
                            html.Div(style={'width': 40, 'height': 40,'border':'1px solid', 'border-radius': 20, 'backgroundColor':'lightgray', 'margin':'auto'}),
                            html.P("60cm"),
                        ])
                    ])       
        ]),
        html.Div(id='methodologie', children=[
            html.P(['Les données sur les arbres du domaine public proviennent du site de la ',
                html.A('Ville de Montréal', href='https://donnees.montreal.ca/dataset/arbres?fbclid=IwAR0kXb318EgUdmDej3XoGVQymQsm_LXBjw-vmkqHNtw37sqwzh1Paqn1iRY', target='_blank'), '.']),
            html.P('Un prétraitement a été effectué sur les données afin de ne garder que les arbres ayant leurs attributs valides (dates, espèce, diamètre du tronc...).')
        ]),
        html.Div(id='info_tooltip', style={'display': 'none'}, children=[
            html.P("Ces deux cartes représentent l'ensemble des arbres du domaine public de la Ville de Montréal."),
            html.P("La carte de gauche affiche chaque arrondissement de Montréal. Quand on passe la souris sur un arrondissement, les informations sur les arbres associées à cet arrondissement apparaissent."),
            html.P("La carte de droite affiche les arbres présents dans l'arrondissement sélectionné. Chaque point représente un arbre et quand on passe la souris sur un point, les informations associées à l'arbre apparaissent."),
            html.P("Vous pouvez filtrer les arbres de ces deux cartes selon l'espèce, la date de plantation et le diamètre du tronc.")
        ]),
        html.Div(id='info_tooltip_2', style={'display': 'none'}, children=[
            html.P("Ces deux graphiques représentent les classements des dix rues, emplacements ou espèces ayant le plus d'arbres selon le critère sélectionné."),
            html.P("Le graphique de gauche considère tous les arbres de la Ville de Montréal, peu importe dans quel arrondissement ils se situent."),
            html.P("Le graphique de droite considère uniquement les arbres présents dans l'arrondissement sélectionné. En particulier, pour le classement des rues, on comptabilise pour chaque rue uniquement les arbres présents dans l'arrondissement sélectionné.")
        ]),
        html.Div(id='info_tooltip_3', style={'display': 'none'}, children=[
            html.P("Ce graphique représente la vitesse moyenne de croissance du tronc et le diamètre moyen du tronc de chaque espèce d'arbre de la Ville de Montréal."),
            html.P("Chaque bulle correspond à une espèce d'arbre, sa position le long de l'axe des abscisses correspond à sa vitesse moyenne de croissance du tronc et sa taille correspond au diamètre de son tronc."),
            html.P("Vous pouvez mettre en évidence une espèce d'arbre grâce à l'outil de recherche.")
        ]),
    ])
])

@app.callback(
    Output('info_tooltip', 'style'),
    [Input('btn_info', 'n_clicks')]
)
def toggle_tooltip(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}
    
@app.callback(
    Output('info_tooltip_2', 'style'),
    [Input('btn_info_2', 'n_clicks')]
)
def toggle_tooltip(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}
    
@app.callback(
    Output('info_tooltip_3', 'style'),
    [Input('btn_info_3', 'n_clicks')]
)
def toggle_tooltip(n_clicks):
    if n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

@app.callback(
    Output('choropleth', 'figure'),
    Input('critere_choropleth', 'value'),
    Input('dateSlider', 'value'),
    Input('diametreSlider', 'value'),
    Input('specie', 'value'),
    prevent_initial_call=True
)
def update_maps(critere_choropleth, date_range, dhp_range, specie):
    densite = critere_choropleth == "Densité d'arbres"
    nb_arbres_arrondissement = preprocess.get_nb_trees_district(data, pd.to_datetime(str(date_range[0]), format='%Y'), \
                                                                pd.to_datetime(str(date_range[1] + 1), format='%Y'), \
                                                                dhp_range[0], dhp_range[1], specie)
    missing_arrondissement = preprocess.get_missing_districts(nb_arbres_arrondissement, locations)
    data_arrondissement = preprocess.add_density(nb_arbres_arrondissement, 'assets/montreal.json')
    choropleth_updated = choropleth.get_choropleth(data_arrondissement, missing_arrondissement, montreal_data, densite=densite)
                        
    return choropleth_updated


@app.callback(
    Output('carte_arrond', 'figure'),
    Input('critere_carte_arrond', 'value'),
    Input('arr_carte_arrond', 'value'),
    Input('dateSlider', 'value'),
    Input('diametreSlider', 'value'),
    Input('specie', 'value'),
    prevent_initial_call=True
)
def update_maps(critere_carte_arrond, arr_carte_arrond, date_range, dhp_range, specie):           
    arrond_map_updated = arrond_map.getMap(data, arr_carte_arrond, critere_carte_arrond, (specie, pd.to_datetime(str(date_range[0]), format='%Y'), pd.to_datetime(str(date_range[1] + 1), format='%Y'), dhp_range[0], dhp_range[1]))
        
    return arrond_map_updated


@app.callback(
    Output('barChartVille', 'figure'),
    Input('critere_bar_chart_ville', 'value'),
    prevent_initial_call=True
)
def update_maps(critere_bar_chart_ville):
    bar_chart_ville_updated = bar_chart.draw_bar_chart(data, None, critere_bar_chart_ville, True)
    
    return bar_chart_ville_updated


@app.callback(
    Output('barChartArrond', 'figure'),
    Input('arr_bar_chart_arrond', 'value'),
    Input('critere_bar_chart_arrond', 'value'),
    prevent_initial_call=True
)
def update_maps(arr_bar_chart_arrond, critere_bar_chart_arrond):
    bar_chart_arrond_updated = bar_chart.draw_bar_chart(data, arr_bar_chart_arrond, critere_bar_chart_arrond, True)
    
    return bar_chart_arrond_updated


@app.callback(
    Output('swarm_plot', 'figure'),
    Input('espece_swarm', 'value'),
    prevent_initial_call=True
)
def update_swarm(espece_swarm):
    swarm_plot_updated = swarmplot.swarmPlot(swarm_plot, swarm, espece_swarm)
    
    return swarm_plot_updated

if __name__ == '__main__':
    app.run_server(debug=True)