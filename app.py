# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:24:16 2019

@author: Matthew
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype
import numpy as np
import plotly
import plotly.graph_objs as go
from KMEAN import KMeans

df = pd.read_excel(r'C:\Users\Matthew\Desktop\Working Here\dashboarding\data.xlsx',index_col=0)


stats = []
for col in df.columns:
    if(is_numeric_dtype(df[col])):
        stats.append(col)
stat_labels = []
for stat in stats:
    stat_labels.append({'label':stat,'value':stat})
pos=[]

for posi in df['Pos'].unique():
    pos.append({'label':posi,'value':posi})
    
app = dash.Dash(__name__)
marks = {}
for i in range(df['MP'].min(),df['MP'].max()):
    if(not(i%200)):
        marks[i] = str(i)

means = []
for i in range(1,7):
    means.append({'label':str(i),'value':i})


app.layout = html.Div([
    
   html.Div([
           html.H3('Analysis Description',className="gs-header gs-text-header padded"),

           html.P("K-Means analysis is a method of finding similarities within a group of data.\
                            The K-Means that minimize the squared error of the data are calculated by\
                            iterating of the dataset, assignined each data point to one of the clusters\
                            The error is calculated as thedistance between each point and the mean of the\
                            cluster to which is has been assigned\""),], className="six columns"),     
        
        
    html.Div(children =[
        html.H3('Minutes Range'),
        dcc.RangeSlider(
                id='mp-slider',
                count=1,
                min=df['MP'].min(),
                max=df['MP'].max(),
                step=200,
                marks=marks,
                value=[df['MP'].min(), df['MP'].max()])],
                style={'margin': '25px'}),
                
    dcc.RadioItems(
            id = 'Dimesion-Select',
            options=[{'label': 'Two Variables', 'value': 1},{'label': 'Three Variables', 'value': 0}],
            value=1
    ),
    
    html.Div(children = [ 
            html.H4('X-Axis Select |',style={'width': '7%', 'display': 'inline-block'}),
            html.H4('Y-Axis Select |',style={'width': '7%', 'display': 'inline-block'}),
            html.H4('Z-Axis Select |',style={'width': '7%', 'display': 'inline-block'}),
            html.H4('Position Select',style={'width': '7%', 'display': 'inline-block'}),
            html.H4('',style={'width': '25%', 'display': 'inline-block'}),
            html.H4('Number of Means',style={'width': '10%', 'display': 'inline-block'})
            ]),
    
    html.Div(children = [ 
            html.Div(children=[dcc.Dropdown(
                id='x-stat-select',
                options=stat_labels,
                value='PTS')],style={'width': '7%', 'display': 'inline-block'}), 
            html.Div(children=[dcc.Dropdown(
                    id='y-stat-select',
                    options=stat_labels,
                    value='AST')],style={'width': '7%', 'display': 'inline-block'}),
            html.Div(children=[dcc.Dropdown(
                    id='z-stat-select',
                    options=stat_labels,
                    value='TOV')],style={'width': '7%', 'display': 'inline-block','visibilty':'hidden'}),        
            html.Div(children=[dcc.Dropdown(
                    id='pos-select',
                    options=pos,
                    multi=True,
                    value=['PG','SG','SF','PF','C'])],style={'width': '20%', 'display': 'inline-block'}),
            html.H4('',style={'width': '20%', 'display': 'inline-block'}),
            html.Div(children=[dcc.Dropdown(
                    id='numMeans',
                    options=means,
                    value=2)],style={'width': '10%', 'display': 'inline-block'})
    ]),
    
     html.Div(children = [ 
            dcc.Graph(id='main-graph',style={'width': '50%', 'display': 'inline-block'}),
            dcc.Graph(id='mean-graph',style={'width': '50%', 'display': 'inline-block'})])
    
])
            
@app.callback(
    Output('main-graph', 'figure'),
    [Input('mp-slider', 'value'),
     Input('x-stat-select','value'),
     Input('y-stat-select','value'),
     Input('z-stat-select','value'),
     Input('pos-select','value'),
     Input('Dimesion-Select','value')])
def update_figure(minute_range,sel_x,sel_y,sel_z,sel_pos,dim):
    filtered_df = df[df.MP < minute_range[1]]
    filtered_df = filtered_df[filtered_df.MP > minute_range[0]] 
    traces = []
    
    if(dim):
        for i in sel_pos:
            df_by_Pos = filtered_df[filtered_df['Pos'] == i]
            traces.append(go.Scatter(
                x=df_by_Pos[sel_x],
                y=df_by_Pos[sel_y],
                text=df_by_Pos['Player'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))
        return {
            'data': traces,
            'layout': dict(title = 'Selected Comparison',
                           yaxis = dict(title = sel_y,gridcolor='#bdbdbd'),
                           xaxis = dict(title = sel_x,gridcolor='#bdbdbd'))
            }
    else:
        for i in sel_pos:
            df_by_Pos = filtered_df[filtered_df['Pos'] == i]
            traces.append(go.Scatter3d(
                x=df_by_Pos[sel_x],
                y=df_by_Pos[sel_y],
                z=df_by_Pos[sel_z],
                text=df_by_Pos['Player'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))
        return {
            'data': traces,
            'layout':
                    dict(
                    title='Selected Comparison',
                    scene = dict(xaxis = dict(title=sel_x,gridcolor='#bdbdbd'),
                                 yaxis = dict(title=sel_y,gridcolor='#bdbdbd'),
                                 zaxis = dict(title=sel_z,gridcolor='#bdbdbd'))
                    )
                }

@app.callback(
    Output('mean-graph', 'figure'),
    [Input('mp-slider', 'value'),
     Input('x-stat-select','value'),
     Input('y-stat-select','value'),
     Input('z-stat-select','value'),
     Input('pos-select','value'),
     Input('Dimesion-Select','value'),
     Input('numMeans','value')])
def update_figure1(minute_range,sel_x,sel_y,sel_z,sel_pos,dim,k):
  
    filtered_df = pd.DataFrame(columns = df.columns)
    for i in range(len(sel_pos)):
        filtered_df = pd.concat([filtered_df,df[df['Pos']== sel_pos[i]]],ignore_index = True)
        
    filtered_df = filtered_df[filtered_df.MP < minute_range[1]]
    filtered_df = filtered_df[filtered_df.MP > minute_range[0]]
    
    kmean = KMeans(k)
    if(dim):
        kmean.train(list(zip(filtered_df[sel_x],filtered_df[sel_y])))
    else:
        kmean.train(list(zip(filtered_df[sel_x],filtered_df[sel_y],filtered_df[sel_z])))
    traces = []

    for i in range(k):
        x_data = filtered_df[sel_x].iloc[kmean.clusters[i]]
        y_data = filtered_df[sel_y].iloc[kmean.clusters[i]]
        players = filtered_df['Player'].iloc[kmean.clusters[i]]
        if(dim):
            traces.append(go.Scatter(
                x=x_data,
                y=y_data,
                text=players,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=str(kmean.means[i])))
        else:
            z_data = filtered_df[sel_z].iloc[kmean.clusters[i]]
            traces.append(go.Scatter3d(
                x=x_data,
                y=y_data,
                z=z_data,
                text=players,
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 5,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=str(kmean.means[i])))
    if(dim):
        return {
            'data': traces,
            'layout': dict(    title='{} Means Analysis'.format(str(k)),
                               yaxis = dict(title = sel_y,gridcolor='#bdbdbd'),
                               xaxis = dict(title = sel_x,gridcolor='#bdbdbd'))}
    else:
        return {
            'data': traces,
            'layout':
                    dict(
                    title='{} Means Analysis'.format(str(k)),
                    scene = dict(xaxis = dict(title=sel_x,gridcolor='#bdbdbd'),
                                 yaxis = dict(title=sel_y,gridcolor='#bdbdbd'),
                                 zaxis = dict(title=sel_z,gridcolor='#bdbdbd'))
                    )
                }
                                                

if __name__ == '__main__':
    app.run_server(debug=True)