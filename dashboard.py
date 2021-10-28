'''
Data visualization project using dash and plotly with python
by:
Mohamed Salah Helal
Walaa Helmy
'''

import dash
from dash import html
from dash import dcc
from dash.dcc.Input import Input
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date

df = pd.read_csv('SeoulBikeData.csv', encoding='ISO-8859-1')
df.drop(columns=['Dew point temperature(°C)','Humidity(%)', 
'Visibility (10m)', 'Rainfall(mm)', 'Snowfall (cm)'], inplace=True)
df.columns = ['date', 'bikeCount', 'hour', 'temperature', 'wind', 
'solarRadiation', 'seasons', 'holiday', 'functioningDay']

df["date"]=pd.to_datetime(df["date"],format="%d/%m/%Y") 
df["month"]=df["date"].dt.month
df["day"]=df["date"].dt.day
df["year"]=df["date"].dt.year
df['weekDay'] = df['date'].dt.weekday
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df['weekDay'] = df.weekDay.apply(lambda x:days[x])
df = df[df['functioningDay'] == 'Yes']

mon = ['Jan','Feb','Mar','Apr','May', 'Jun','Jul','Aug','Sep','Oct','Nov','Dec']
df1 = df[df.year==2018].groupby('seasons').sum()['bikeCount'].reset_index()
pie = px.pie(
    df1, names='seasons', values='bikeCount', 
    color_discrete_sequence=['gold','purple','teal','brown'],
    title='Bike Rent / Seasons',
)
pie.update_layout(
    title=dict(font={'size': 15}, x=0.5, xanchor='center'),
    legend=dict(x=-.1, y=1, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
    margin=dict(l=0, r=0, t=30, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
)    

df2 = df.groupby('month').mean()[['bikeCount', 'year']].reset_index()
bar=px.bar(
        df2, x="month", y="bikeCount",
        title='Bike Rents / Month',
    )
bar.update_layout(
    title=dict(font={'size': 15}, x=0.5, xanchor='center'),
    legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
    margin=dict(l=0, r=0, t=30, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    legend_title_text='',
    xaxis = dict(
        tickmode = 'array',
        tickvals = list(range(1,13)),
        ticktext = mon
    )
)    

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.Div([
        html.H2('Seoul Bike Sharing Demand', style={'textAlign': 'center', 'padding':'15px', 'color':'white'}),
        html.Div([
            dcc.Graph(
                id='mg1', figure=pie,
                style={
                    "border":"2px darkgray solid", "borderRadius": "10px", 
                    'background-color':'#f7f1e3', 'padding':'15px', 
                    'height':'300px',
                    'margin-right':'10px'
                    }, 
                ),
            dcc.Graph(
                id='mg2', figure=bar,
                style={
                    "border":"2px darkgray solid", "borderRadius": "10px", 
                    'background-color':'#f7f1e3',
                    'height':'300px',
                    'padding':'15px'
                    }, 
            ),
            html.Div([  
                html.H4('For more Details, Pick a Date..', style={'textAlign': 'center'}),
                dcc.DatePickerSingle(
                    id='date',
                    month_format='MMM Do, YY',
                    placeholder='MMM Do, YY',
                    date=date(2017, 11, 1),
                    style={
                        'margin-left':'140px',
                        'textAlign': 'center'}
                ),
                html.Div(id='h1')
                ], style={
                    "border":"2px darkgray solid", "borderRadius": "10px", 
                    'background-color':'#f7f1e3',
                    'height':'300px',
                    'padding':'15px',
                    'color':'#273c75',
                    'margin-left':'10px'} 
            ),], style={
                "display": "grid",
                'margin-left':'20px', 
                'margin-right':'20px',
                'margin-bottom':'10px',
                "grid-template-columns": "33% 34% 33%"
            }
        )
    ]),
    
    html.Div([
        html.Div([
            html.Br(),
            dcc.Graph(
                id='g5', 
                style={
                    "border":"2px darkgray solid", "borderRadius": "10px",
                    'background-color':'#f7f1e3',
                    'height':'350px',
                    'padding':'15px'
                }
            ),
            dcc.Checklist(
                id='check1',
                options=[
                    {'label': 'Holiday', 'value': 'Holiday'},
                    {'label': 'Work Day', 'value': 'No Holiday'},
                ],
                value=['Holiday', 'No Holiday'],
                style={
                    'vertical-align': 'top', 'margin-top': '13vw',
                    'color':'white'
                    ,}
            ),
            dcc.Graph(
                id='g4', 
                style={
                    "border":"2px darkgray solid", "borderRadius": "10px",
                    'background-color':'#f7f1e3',
                    'height':'350px',
                    'padding':'15px'
                }
            ),
            dcc.Checklist(
                id='check2',
                options=[
                    {'label': 'Sat', 'value': 'Saturday'},
                    {'label': 'Sun', 'value': 'Sunday'},
                    {'label': 'Mon', 'value': 'Monday'},
                    {'label': 'Tues', 'value': 'Tuesday'},
                    {'label': 'Wed', 'value': 'Wednesday'},
                    {'label': 'Thur', 'value': 'Thursday'},
                    {'label': 'Fri', 'value': 'Friday'},
                ],
                value=days,
                style={
                    'vertical-align':'top', 'margin-top': '13vw',
                    'color':'white'
                    }
            ),
        ], style={"display": "grid", "grid-template-columns": "5% 40% 7% 40% 5%"}),
        html.Br(),
        html.Div([
            html.Br(),
            dcc.RangeSlider(
                id='temperature',
                min=-10,
                max=40,
                marks={i:str(i)+'°C' for i in range(-10,41,5)},
                tooltip={"placement": "bottom", "always_visible": True},
                value=[-10,40],
            ),
            html.Br()
            ], 
            style={
                "display": "grid", "grid-template-columns": "10% 80% 10%",
            }
        ),
        html.Br()
    ])  
], style={'background-color':'#57606f', "border":"2px darkgray solid", "borderRadius": "10px",})

@app.callback(
    [
        Output(component_id='g4', component_property='figure'),
        Output(component_id='g5', component_property='figure'),
    ],
    [
        Input(component_id='temperature', component_property='value'),
        Input(component_id='check1', component_property='value'),
        Input(component_id='check2', component_property='value'),
    ] 
)
def fig1(temp, day, day2):
    df0 = df[(df.temperature<=temp[1]) & (df.temperature>=temp[0]) &(df.holiday.isin(day))]
    df00 = df[(df.temperature<=temp[1]) & (df.temperature>=temp[0])]
    df44 = df00.groupby(['weekDay', 'hour'])['bikeCount'].mean().reset_index()
    df44 = df44[df44.weekDay.isin(day2)]

    df5 = df0[df0.holiday=='Holiday'].groupby('hour').mean().reset_index()
    df5['holiday'] = 'Holiday'
    df6 = df0[df0.holiday=='No Holiday'].groupby('hour').mean().reset_index()
    df6['holiday'] = 'No Holiday'
    df7 = pd.concat([df5,df6], ignore_index=True)

    bar4 = px.line(
        df44, x='hour', y='bikeCount', color='weekDay', range_x=[0,24],
        title='Bike rents vs. Hours through the week',
        )
    bar4.update_layout(
        title=dict(font={'size': 15}, x=0.5, xanchor='center'),
        legend=dict(x=0, y=1, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='',
        xaxis = dict(
            tickmode = 'array',
            tickvals = list(range(0,24)),
            ticktext = list(range(0,24))
        )
    )
    
    bar5=px.bar(
        df7, x="hour", y="bikeCount",
        title='Bike rents vs. Hours at working days and holidays',
        color='holiday', barmode='group', range_x=[0,24],
    )
    bar5.update_layout(
        title=dict(font={'size': 15}, x=0.5, xanchor='center'),
        legend=dict(x=-0, y=1, bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
        margin=dict(l=0, r=0, t=30, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend_title_text='',
        xaxis = dict(
            tickmode = 'array',
            tickvals = list(range(0,24)),
            ticktext = list(range(0,24))
        )
    )
    return bar4,bar5

@app.callback(
    Output(component_id='h1', component_property='children'),
    Input(component_id='date', component_property='date') 
)
def fig1(d):
    y,mn,dy=list(d.split('-'))
    dff = df[(df.year==int(y))&(df.month==int(mn))&(df.day==int(dy))]
    if dff.bikeCount.empty:
        return html.H5('')
    return html.Div([
        html.H5('Number of Rented Bikes: '+str(dff.bikeCount.values[0])),
        html.H5('Temperature: '+str(dff.temperature.values[0])+' °C'),
        html.H5('Wind Speed: '+str(dff.wind.values[0])+' m/s')
    ], style={'margin-left':'35px'})
        

if __name__ == '__main__':
    app.run_server(debug=True)