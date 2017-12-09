__author__ = 'aleksandr'
import random
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import json
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objs as go
import copy
import os
import flask
app = dash.Dash()

app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True



r = lambda: random.randint(30,255)

app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501


# Create global chart template
mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    autosize=True,
    height=500,
    font=dict(color='#CCCCCC'),
    titlefont=dict(color='#CCCCCC', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),
    hovermode="closest",
    plot_bgcolor="#191A1A",
    paper_bgcolor="#020202",
    legend=dict(font=dict(size=10), orientation='h'),

)

USER_COUNTRIES = pd.DataFrame.from_csv(
    'countries_users.csv'
)

USER_CITIES = pd.DataFrame.from_csv(
    'cities_users.csv'
)
POSTS = pd.DataFrame.from_csv(
    'kreed.csv'
)
USERS = pd.DataFrame.from_csv(
    'user_info.csv'
)
USERS['from_id']=USERS['id']
JOINED = pd.merge(POSTS, USERS, on='from_id')
JOINED.index=JOINED['date.1']
JOINED.index = pd.to_datetime(JOINED.index)
COUNTRY=USER_COUNTRIES
CITY=USER_CITIES

new_list=[]
for value in USERS['personal']:
    try:
        #print(type(value))
        json_acceptable_string = value.replace("'", "\"")

        el = json.loads(json_acceptable_string)
        new_list.append(el)
    except:
        pass
#print(el)
TRAITS = pd.DataFrame.from_records(new_list)

for value in USERS['occupation']:
    try:
        #print(type(value))
        json_acceptable_string = value.replace("'", "\"")

        el = json.loads(json_acceptable_string)
        new_list.append(el)
    except:
        pass
#print(el)
PROF = pd.DataFrame.from_records(new_list)

def transform_to_dropdown(data):
    result = [{'label': x, 'value': x} for x in data]
    return result



def get_traits():

    users = USERS['sex'].value_counts()
    total = JOINED['sex'].value_counts()
    users_sum=users.sum()
    total_sum = total.sum()
    female_list = [users.loc[1]/users_sum, total.loc[1]/total_sum]
    male_list = [users.loc[2] / users_sum, total.loc[2] / total_sum]
    headers = ['By users', 'By posts']
    trace1 = go.Bar(
        x= headers,
        y=female_list,
        marker={
            'color': ['#f43084', '#f43084']
        },
        name='Female'
    )
    trace2 = go.Bar(
        x=headers,
        y=male_list,
        marker={
            'color': ['#073cba', '#073cba']
        },
        name='Male'
    )

    data = [trace1, trace2]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'stack'

    fig = go.Figure(data=data, layout=layout_individual)

    return fig

def get_platform():


    trace1 = go.Bar(
        x= JOINED['post_source_platform'].value_counts().index,
        y=JOINED['post_source_platform'].value_counts(),
        marker={
            'color': ['#e9724d', '#d6d727', '#92cad1', '#79ccb3',
                      '#868686']
        },
        name='Platform'
    )
    data = [trace1]


    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    fig = go.Figure(data=data, layout=layout_individual)

    return fig

def get_occupation():


    trace1 = go.Bar(
        x= PROF['type'].value_counts().index,
        y=PROF['type'].value_counts(),
        name='Platform',
        marker={
            'color': ['#92cad1', '#79ccb3',
                      '#868686']
        },
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    fig = go.Figure(data=data, layout=layout_individual)


    return fig

def get_personal():
    traits_dict ={
                1:'Intellect and creativity',
                2:'Kindness and honesty',
                3:'Health and beauty',
                4:'Wealth and power',
                5:'Courage and persistance',
                6:'Humor and love for life'
    }

    t_lst = TRAITS['people_main'].value_counts()

    labels = []
    for i in t_lst.index:
        labels.append(traits_dict[i])


    trace1 = go.Bar(
        x= labels,
        y=t_lst,
        marker={
            'color': ['#e9724d', '#d6d727', '#92cad1', '#79ccb3',
                      '#868686']
        },
        name='Platform'
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    layout_individual['margin'] = dict(
        l=35,
        r=35,
        b=95,
        t=45
    )
    fig = go.Figure(data=data, layout=layout_individual)

    return fig

def get_priority():
    traits_dict ={
                1:'Family and children',
                2:'Career and money',
                3:'Entertainment and leisure',
                4:'Science and research',
                5:'Improving the world',
                6:'personal development',
                7:'Beauty and art',
                8:'Fame and influence'
    }

    t_lst = TRAITS['people_main'].value_counts()

    labels = []
    for i in t_lst.index:
        labels.append(traits_dict[i])


    trace1 = go.Bar(
        x= labels,
        y=t_lst,
        marker={
            'color': ['#e9724d', '#d6d727', '#92cad1', '#79ccb3',
                      '#868686']
        },
        name='Platform'
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    layout_individual['margin'] = dict(
        l=35,
        r=35,
        b=95,
        t=45
    )
    fig = go.Figure(data=data, layout=layout_individual)

    return fig

def get_alcohol():
    traits_dict ={
                1:'Very negative',
                2:'Negative',
                3:'Neutral',
                4:'Positive',
                5:'Very positive'
    }

    t_lst = TRAITS['alcohol'].value_counts()

    labels = []
    for i in t_lst.index:
        labels.append(traits_dict[i])


    trace1 = go.Bar(
        x= labels,
        y=t_lst,
        marker={
            'color': ['#e9724d', '#d6d727',
                      '#868686','#92cad1', '#79ccb3']
        },
        name='Platform'
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    fig = go.Figure(data=data, layout=layout_individual)


    return fig

def get_nicotine():
    traits_dict ={
                1:'Very negative',
                2:'Negative',
                3:'Neutral',
                4:'Positive',
                5:'Very positive'
    }

    t_lst = TRAITS['smoking'].value_counts()

    labels = []
    for i in t_lst.index:
        labels.append(traits_dict[i])


    trace1 = go.Bar(
        x= labels,
        y=t_lst,
        marker={
            'color': ['#e9724d', '#d6d727',
                      '#868686', '#92cad1', '#79ccb3']
        },
        name='Platform'
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    fig = go.Figure(data=data, layout=layout_individual)

    return fig

def get_religion():


    t_lst = TRAITS['religion'].value_counts().head(6)

    trace1 = go.Bar(
        x= t_lst.index,
        y=t_lst,
        name='Platform'
    )
    data = [trace1]
    layout_individual = copy.deepcopy(layout)
    layout_individual['barmode'] = 'bar'
    layout_individual['margin'] = dict(
        l=35,
        r=35,
        b=75,
        t=45
    )
    fig = go.Figure(data=data, layout=layout_individual)

    return fig


def get_new_users_dynamics():
    graphs_lst=[]
    new = POSTS['from_id'].resample('M').nunique()
    graphs_lst.append(go.Scatter(
        x=new.index,
        y=new,
        name='New Users addition',
        line=dict(color='##7F7F7F'),
        opacity=0.8))

    # return None

    #layout_individual = copy.deepcopy(layout)
    layout_individual = go.Layout()
    layout_individual['plot_bgcolor']="#191A1A"
    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['paper_bgcolor'] = "#020202"
    layout_individual['title'] = 'New users coming to topic'
    #layout_individual['margin'] = {'l': 40, 'r': 0, 't': 20, 'b': 30}
    layout_individual['xaxis'] = dict(
                       rangeselector=dict(
                           buttons=list([
                               dict(count=7,
                                    label='W',
                                    step='day',
                                    stepmode='backward'),
                               dict(count=1,
                                    label='M',
                                    step='month',
                                    stepmode='backward'),
                               dict(count=1,
                                    label='Y',
                                    step='year',
                                    stepmode='backward'),
                               dict(step='all')
                           ])
                       ),
                       rangeslider=dict(),
                       type='date'

                   )


    return_value = {
        'data': graphs_lst,
        'layout': layout_individual
    }
    return return_value

def get_total_reacts():
    graphs_lst=[]
    like = POSTS['likes'].resample('D').sum()
    graphs_lst.append(go.Scatter(
        x=like.index,
        y=like,
        name='Total Reactions',
        line=dict(
            shape="spline",
            smoothing=2,
            width=1,
            color='#fac1b7'
        )))

    # return None



    layout_individual = go.Layout()
    layout_individual['plot_bgcolor'] = "#191A1A"
    layout_individual['paper_bgcolor'] = "#020202"
    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['title'] = 'Total interest to Egor Kreed in social media'
    #layout_individual['margin'] = {'l': 40, 'r': 0, 't': 20, 'b': 30}

    layout_individual['xaxis'] = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='W',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='M',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='Y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'

    )

    return_value = {
        'data': graphs_lst,
        'layout': layout_individual
    }
    return return_value
#TODO make axises binded fro first graphs
app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='graph-total_reacts',
            figure=get_total_reacts()

        ),
        dcc.Graph(
            id='graph-new_users',
            figure=get_new_users_dynamics()
        ),
        html.H4('Main DataTable'),
        dt.DataTable(
            rows=USERS.to_dict('records'),

            # optional - sets the order of columns
            columns=sorted(USERS.columns),

            row_selectable=True,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            id='datatable-gapminder'
        ),
        html.Div(id='selected-indexes'),

        dcc.Graph(
            id='graph-gapminder'

        ),
        dcc.Graph(
            id='graph-posts'
        ),
        html.Div([
            html.Div([
                html.H2('User Traits global'),

                dcc.Graph(
                    id='graph-user-sex',
                    figure=get_traits()

                )], className='six columns'),
            html.Div([
                html.H2('User Platforms global'),
                dcc.Graph(
                    id='graph-user-platform',
                    figure=get_platform()

                )], className = 'six columns')],
                className='row'),
        html.Div([
            html.Div([
                html.H2('User Religion'),
                dcc.Graph(
                    id='graph-user-religion',
                    figure=get_religion()

                )], className='six columns'),
            html.Div([
                html.H2('User Occupation global'),
                dcc.Graph(
                    id='graph-user-occupation',
                    figure=get_occupation()

                )], className='six columns')],
                className='row'),
        html.Div([
            html.Div([
                html.H2('User global priorities'),
                dcc.Graph(
                    id='graph-user-priority',
                    figure=get_priority()

                )], className='six columns'),

        html.Div([
            html.H2('User Important in others global'),
            dcc.Graph(
                id='graph-user-personal',
                figure=get_personal()

            )
        ], className='six columns')],
        className='row'),

    html.Div([
        html.Div([
            html.H2('User Alcohol views'),
            dcc.Graph(
                id='graph-user-alcohol',
                figure=get_alcohol()

            )], className='six columns'),

        html.Div([
            html.H2('User Nicotine views'),
            dcc.Graph(
                id='graph-user-nicotine',
                figure=get_nicotine()

            )], className='six columns')],
        className='row'),

        #dcc.Graph(
        #    id='graph-country-city',
        #    figure=get_figure()

        #),
        dcc.Dropdown(
            id='my-country',
            options=transform_to_dropdown(COUNTRY['country']),
            value=None
        ),
        dcc.Graph(
            id='agg-country'

        ),
        dcc.Dropdown(
            id='my-city',
            options=transform_to_dropdown(CITY['city'])
        ),
        dcc.Graph(
            id='agg-city'

        ),
        html.Div(dcc.Input(id='input-box', type="text")),
        html.Button('Enter number of top influencers', id='button'),
        html.Div(dcc.Textarea(id='output-container-button',
                disabled=True,
                rows=15,
                style={'width': '100%'},
                value="Select city, or remove for global influencers"))

    ], className="eleven columns"),
 #   html.Div([
 #
 #       dcc.Dropdown(
 #           id='my-city',
 #           options=transform_to_dropdown(CITY['city'])
 #           ),
  #      ], className="four rows")
], className="twelve columns")

@app.callback(
    Output('output-container-button', 'value'),
    [Input('button', 'n_clicks')],
    [State('input-box', 'value'),
    State('my-city', 'value')])
def update_output(n_clicks, value,city):
    if city:
        df = JOINED[JOINED['city'] == city]
    else:
        df= JOINED

    posts_count = df.groupby('from_id').count().sort_values(by='id_x', ascending=False)
    posts_reactions = df.groupby('from_id').sum().sort_values(by='likes', ascending=False)

    weighted_lst = []
    counter = 0
    for index, row in posts_count.iterrows():
        if index < 0: continue
        df_iter_for_author = posts_reactions.loc[index]
        # print (df_iter_for_author)


        reactions_sum = df_iter_for_author['likes']
        comments_sum = df_iter_for_author['comments_count']

        weighted_reactions_sum = reactions_sum / row['id_x']

        entry = {}
        # weighted_comments_sum = comments_sum
        user = USERS[USERS['id'] == index]
        entry['name']=(user['first_name'] + ' ' + user['last_name'])
        entry['reactions_sum']=reactions_sum
        entry['weighted'] = weighted_reactions_sum
        weighted_lst.append(entry)

    if not value:
        value = 10
    newlist = sorted(weighted_lst, key=lambda k: k['weighted'], reverse=True)[:int(value)]

    result = [ '\n' + ("User  \"{}\" has sum of reactions {} with weight {} for one post \n".format(
                    entry['name'].item(),
                    entry['reactions_sum'],
                    entry['weighted']
                )) for entry in newlist]

    return result


@app.callback(
    Output('agg-country', 'figure'),
    [Input('my-country', 'value')])
def update_selected_row_indices(value):

    graph = [go.Scatter(
                                    x=JOINED.resample('D').mean().index,
                                    y=JOINED[JOINED['country']==value]['id_x'].resample('D').count(),
                                    name=value,
                                    line=dict(
                                        shape="spline",
                                        smoothing=2,
                                        width=1,
                                        color='#92d8d8'
                                    ))]

    layout_individual = go.Layout()
    layout_individual['plot_bgcolor'] = "#191A1A"
    layout_individual['paper_bgcolor'] = "#020202"
    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['title'] = 'Posts by Country'
    #layout_individual['margin'] = {'l': 40, 'r': 0, 't': 20, 'b': 30}
    layout_individual['xaxis'] = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='W',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='M',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='Y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'

    )

    return_value = {
        'data': graph,
        'layout': layout_individual
    }


    return return_value


@app.callback(
    Output('agg-city', 'figure'),
    [Input('my-city', 'value')])
def update_selected_indexes(value):

    graph = [go.Scatter(
                                    x=JOINED.resample('D').mean().index,
                                    y=JOINED[JOINED['city']==value]['id_x'].resample('D').count(),
                                    name=value,
                                    line=dict(
                                        shape="spline",
                                        smoothing=2,
                                        width=1,
                                        color='#a9bb95'
                                    ))]

    layout_individual = go.Layout()
    layout_individual['plot_bgcolor'] = "#191A1A"
    layout_individual['paper_bgcolor'] = "#020202"
    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['title'] = 'Posts by City'
    #layout_individual['margin'] = {'l': 40, 'r': 0, 't': 20, 'b': 30}
    layout_individual['xaxis'] = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='W',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='M',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='Y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'

    )

    return_value = {
        'data': graph,
        'layout': layout_individual
    }
    return return_value

#TODO how much live overal kreed interested

@app.callback(
    Output('datatable-gapminder', 'selected_row_indices'),
    [Input('graph-gapminder', 'clickData')],
    [State('datatable-gapminder', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph-gapminder', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    graphs_lst = []

    for i in selected_row_indices:
        data = POSTS[POSTS['from_id'] == dff[i:i+1]['id'].item()]
        name = dff[i:i+1]['first_name'].item() + ' ' + dff[i:i+1]['last_name'].item()
        color = dict(color='#%02X%02X%02X' % (r(),r(),r()))
        graphs_lst.append(go.Scatter(
                                    x=data.resample('D').index,
                                    y=data['likes'].resample('D').sum(),
                                    name=name,
                                    line=color,
                                    opacity=0.8))

    layout_individual = go.Layout()
    layout_individual['plot_bgcolor'] = "#191A1A"
    layout_individual['paper_bgcolor'] = "#020202"

    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['title'] = 'Reactions got by User'

    layout_individual['xaxis'] = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='W',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='M',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='Y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'

    )

    return_value = {
        'data': graphs_lst,
        'layout': layout_individual
    }

    return return_value


@app.callback(
    Output('graph-posts', 'figure'),
    [Input('datatable-gapminder', 'rows'),
     Input('datatable-gapminder', 'selected_row_indices')])
def update_figure(rows, selected_row_indices):
    dff = pd.DataFrame(rows)
    graphs_lst = []
    for i in selected_row_indices:
        data = POSTS[POSTS['from_id'] == dff[i:i+1]['id'].item()]
        name = dff[i:i+1]['first_name'].item() + ' ' + dff[i:i+1]['last_name'].item()
        color = dict(color='#%02X%02X%02X' % (r(),r(),r()))
        graphs_lst.append(go.Scatter(
                                    x=data.resample('D').index,
                                    y=data['id'].resample('D').count(),
                                    name=name,
                                    line=color,
                                    opacity=0.8))

    #return None
    # return Non
    layout_individual = go.Layout()
    layout_individual['plot_bgcolor'] = "#191A1A"
    layout_individual['paper_bgcolor'] = "#020202"

    layout_individual['font'] = dict(color='#CCCCCC')
    layout_individual['title'] = 'Reactions got by User'
    #layout_individual['margin'] = {'l': 40, 'r': 0, 't': 20, 'b': 30}
    layout_individual['xaxis'] = dict(
        rangeselector=dict(
            buttons=list([
                dict(count=7,
                     label='W',
                     step='day',
                     stepmode='backward'),
                dict(count=1,
                     label='M',
                     step='month',
                     stepmode='backward'),
                dict(count=1,
                     label='Y',
                     step='year',
                     stepmode='backward'),
                dict(step='all')
            ])
        ),
        rangeslider=dict(),
        type='date'

    )

    return_value = {
        'data': graphs_lst,
        'layout': layout_individual
    }

    return return_value

STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.server.route('/static/<resource>')
def serve_static(resource):
    return flask.send_from_directory(STATIC_PATH, resource)

app.css.append_css({
    "external_url": "/static/styles.css"
})

#dcc._css_dist[0]['relative_package_path'].append('styles.css')

if __name__ == '__main__':
    app.run_server(debug=True)
