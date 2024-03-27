
# -*- coding: utf-8 -*-

import json

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd
import numpy as np

import preprocess
# import bubble

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

species = preprocess.getSpeciesList()

# with open('../src/assets/data/countriesData.json') as data_file:
#     data = json.load(data_file)

# df_2000 = pd.json_normalize(data, '2000')
# df_2015 = pd.json_normalize(data, '2015')

# df_2000 = preprocess.round_decimals(df_2000)
# df_2015 = preprocess.round_decimals(df_2015)

# gdp_range = preprocess.get_range('GDP', df_2000, df_2015)
# co2_range = preprocess.get_range('CO2', df_2000, df_2015)

# df = preprocess.combine_dfs(df_2000, df_2015)
# df = preprocess.sort_dy_by_yr_continent(df)

# fig = bubble.get_plot(df, gdp_range, co2_range)
# fig = bubble.update_animation_hover_template(fig)
# fig = bubble.update_animation_menu(fig)
# fig = bubble.update_axes_labels(fig)
# fig = bubble.update_template(fig)
# fig = bubble.update_legend(fig)

# fig.update_layout(height=600, width=1000)
# fig.update_layout(dragmode=False)
print(np.linspace(1960, 2023, 10, dtype=int))

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('Les arbres de Montréal'),
    ]),
    html.Main(className='viz-container', children=[
        # dcc.Graph(className='graph', figure=fig, config=dict(
        #     scrollZoom=False,
        #     showTips=False,
        #     showAxisDragHandles=False,
        #     doubleClick=False,
        #     displayModeBar=False
        #     )),
        html.Div(id='maps', children=[
            html.Div(id='filter', children=[
                dcc.Dropdown(id='specie',
                    options=species,
                    placeholder='Espèces',
                    multi=True,
                ),
                html.Div(id='date', children=[
                    dcc.RangeSlider(
                        id='dateSlider',
                        min=1960,
                        max=2023,
                        step=1,
                        value=[1960, 2023],
                        marks={2000: ''}
                    ),
                    html.Div(id='minDate', className='cursor min', children=['1960']),
                    html.Div(id='maxDate', className='cursor max', children=['2023'])
                ]),
                html.Div(id='diametre', children=[
                    dcc.RangeSlider(
                        id='diametreSlider',
                        min=0,
                        max=300,
                        step=1,
                        value=[0, 300],
                        marks={100: ''}
                    ),
                    html.Div(id='minDHP', className='cursor min', children=['0']),
                    html.Div(id='maxDHP', className='cursor max', children=['300'])
                ])
                
                
            ]),
            html.Div(id='total'),
            html.Div(id='arrond'),
        ]),
        html.Div(id='swarm')
    ])
])
