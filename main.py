import json
import math
import random
import numpy as np
import pandas as pd
import plotly.express as px  # (version 4.7.0)
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import wordcloud
import statsmodels

#add external stylesheet
external_stylesheets = [
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    }
]



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
all_country_option = ['Finland', 'Denmark', 'Switzerland', 'Iceland', 'Netherlands', 'Norway', 'Sweden', 'Luxembourg', 'New Zealand', 'Austria', 'Australia', 'Israel', 'Germany', 'Canada', 'Ireland', 'Costa Rica', 'United Kingdom', 'Czech Republic', 'United States', 'Belgium', 'France', 'Bahrain', 'Malta', 'Taiwan Province of China', 'United Arab Emirates', 'Saudi Arabia', 'Spain', 'Italy', 'Slovenia', 'Guatemala', 'Uruguay', 'Singapore', 'Kosovo', 'Slovakia', 'Brazil', 'Mexico', 'Jamaica', 'Lithuania', 'Cyprus', 'Estonia', 'Panama', 'Uzbekistan', 'Chile', 'Poland', 'Kazakhstan', 'Romania', 'Kuwait', 'Serbia', 'El Salvador', 'Mauritius', 'Latvia', 'Colombia', 'Hungary', 'Thailand', 'Nicaragua', 'Japan', 'Argentina', 'Portugal', 'Honduras', 'Croatia', 'Philippines', 'South Korea', 'Peru', 'Bosnia and Herzegovina', 'Moldova', 'Ecuador', 'Kyrgyzstan', 'Greece', 'Bolivia', 'Mongolia', 'Paraguay', 'Montenegro', 'Dominican Republic', 'North Cyprus', 'Belarus', 'Russia', 'Hong Kong S.A.R. of China', 'Tajikistan', 'Vietnam', 'Libya', 'Malaysia', 'Indonesia', 'Congo (Brazzaville)', 'China', 'Ivory Coast', 'Armenia', 'Nepal', 'Bulgaria', 'Maldives', 'Azerbaijan', 'Cameroon', 'Senegal', 'Albania', 'North Macedonia', 'Ghana', 'Niger', 'Turkmenistan', 'Gambia', 'Benin', 'Laos', 'Bangladesh', 'Guinea', 'South Africa', 'Turkey', 'Pakistan', 'Morocco', 'Venezuela', 'Georgia', 'Algeria', 'Ukraine', 'Iraq', 'Gabon', 'Burkina Faso', 'Cambodia', 'Mozambique', 'Nigeria', 'Mali', 'Iran', 'Uganda', 'Liberia', 'Kenya', 'Tunisia', 'Lebanon', 'Namibia', 'Palestinian Territories', 'Myanmar', 'Jordan', 'Chad', 'Sri Lanka', 'Swaziland', 'Comoros', 'Egypt', 'Ethiopia', 'Mauritania', 'Madagascar', 'Togo', 'Zambia', 'Sierra Leone', 'India', 'Burundi', 'Yemen', 'Tanzania', 'Haiti', 'Malawi', 'Lesotho', 'Botswana', 'Rwanda', 'Zimbabwe', 'Afghanistan', 'Finland', 'Denmark', 'Switzerland', 'Iceland', 'Netherlands', 'Norway', 'Sweden', 'Luxembourg', 'New Zealand', 'Austria', 'Australia', 'Israel', 'Germany', 'Canada', 'Ireland', 'Costa Rica', 'United Kingdom', 'Czech Republic', 'United States', 'Belgium', 'France', 'Bahrain', 'Malta', 'Taiwan Province of China', 'United Arab Emirates', 'Saudi Arabia', 'Spain', 'Italy', 'Slovenia', 'Guatemala', 'Uruguay', 'Singapore', 'Kosovo', 'Slovakia', 'Brazil', 'Mexico', 'Jamaica', 'Lithuania', 'Cyprus', 'Estonia', 'Panama', 'Uzbekistan', 'Chile', 'Poland', 'Kazakhstan', 'Romania', 'Kuwait', 'Serbia', 'El Salvador', 'Mauritius', 'Latvia', 'Colombia', 'Hungary', 'Thailand', 'Nicaragua', 'Japan', 'Argentina', 'Portugal', 'Honduras', 'Croatia', 'Philippines', 'South Korea', 'Peru', 'Bosnia and Herzegovina', 'Moldova', 'Ecuador', 'Kyrgyzstan', 'Greece', 'Bolivia', 'Mongolia', 'Paraguay', 'Montenegro', 'Dominican Republic', 'North Cyprus', 'Belarus', 'Russia', 'Hong Kong S.A.R. of China', 'Tajikistan', 'Vietnam', 'Libya', 'Malaysia', 'Indonesia', 'Congo (Brazzaville)', 'China', 'Ivory Coast', 'Armenia', 'Nepal', 'Bulgaria', 'Maldives', 'Azerbaijan', 'Cameroon', 'Senegal', 'Albania', 'North Macedonia', 'Ghana', 'Niger', 'Turkmenistan', 'Gambia', 'Benin', 'Laos', 'Bangladesh', 'Guinea', 'South Africa', 'Turkey', 'Pakistan', 'Morocco', 'Venezuela', 'Georgia', 'Algeria', 'Ukraine', 'Iraq', 'Gabon', 'Burkina Faso', 'Cambodia', 'Mozambique', 'Nigeria', 'Mali', 'Iran', 'Uganda', 'Liberia', 'Kenya', 'Tunisia', 'Lebanon', 'Namibia', 'Palestinian Territories', 'Myanmar', 'Jordan', 'Chad', 'Sri Lanka', 'Swaziland', 'Comoros', 'Egypt', 'Ethiopia', 'Mauritania', 'Madagascar', 'Togo', 'Zambia', 'Sierra Leone', 'India', 'Burundi', 'Yemen', 'Tanzania', 'Haiti', 'Malawi', 'Lesotho', 'Botswana', 'Rwanda', 'Zimbabwe', 'Afghanistan']
app.layout = html.Div([
    html.H1("World Happiness Report Data Visualization from 2015 to 2021", style={'text-align': 'center','background-color':'#4797c6','color':'white'}),
    html.Div(id='output_container', children=[]),
    # initial select year
    dcc.Slider(
        id="select_year",
        min=2015,
        max=2021,
        marks={i: 'Year {}'.format(i) for i in range(2015,2022,1)},
        value=2015,
    ),
    # initial world happiness map
    html.Div(
        [    dcc.Graph(id='world_map_happiness', style={'width':'100%'}),
        ]
    ),
    html.Div(
        [
            dcc.Graph(id='factors_country', style={'width': '63%', 'height':'370px', 'float':'left'}),
            dcc.Graph(id='figTotal', style={'width': '36%', 'height': '370px', 'float':'left'})
        ],style={'height':'370px'}
    ),
    #initial select region dropdown
    html.Div([
        #select area
        # dcc.Dropdown(
        #     options=[
        #         {'label': 'Total Countries', 'value': 'Total Countries'},
        #         {'label': 'Commonwealth of Independent States', 'value': 'Commonwealth of Independent States'},
        #         {'label': 'Southeast Asia', 'value': 'Southeast Asia'},
        #         {'label': 'Middle East and North Africa', 'value': 'Middle East and North Africa'},
        #         {'label': 'Western Europe', 'value': 'Western Europe'},
        #         {'label': 'Latin America and Caribbean', 'value': 'Latin America and Caribbean'},
        #         {'label': 'North America and ANZ', 'value': 'North America and ANZ'},
        #         {'label': 'Sub-Saharan Africa', 'value': 'Sub-Saharan Africa'},
        #         {'label': 'East Asia', 'value': 'East Asia'},
        #         {'label': 'South Asia', 'value': 'South Asia'},
        #     ],
        #     value='Middle East and North Africa',
        #     placeholder="select a factor",
        #     id="select_region",
        #     style={'width': '40%', 'float':'left'}
        # ),
        #select compare
        dcc.RadioItems(
            options=[
                {'label': 'Region', 'value': 'Region'},
                {'label': 'Country category', 'value': 'Economy'},
            ],
            value='Region',
            id="select_region_economy",
            style={'width': '20%', 'float':'left','margin-left':'10px'}
        ),
        #select relationship dropdown
      #cheng
    ],style={'margin-top':'0px'},),
    #initial stack area chart radar chart scatterplot
    html.Div(
        [
            dcc.Graph(id='radar_region_economy', style={'width': '55%', 'float': 'left', }),
            dcc.Graph(id='country_top_ten', style={'width': '45%', 'float':'left'}),
            #, 'margin-top':'-400px'
            #'margin-left':'-380px'
        ],style={'height':'450px','margin-top':'25px'}
    ),
    html.Div(
        [

            # Output('radar_trust', 'figure'),
            # Output('radar_freedom', 'figure'),
            # Output('radar_health', 'figure'),
            # Output('radar_support', 'figure'),
            # Output('radar_generosity', 'figure'),

            dcc.Graph(id='radar_economy', style={'float': 'left', 'width': '20%'}),
            dcc.Graph(id='radar_freedom', style={'float': 'left', 'width': '20%'}),
            dcc.Graph(id='radar_trust', style={'float': 'left', 'width': '20%'}),
            dcc.Graph(id='radar_health', style={'float': 'left', 'width': '20%'}),
            dcc.Graph(id='radar_support', style={'float': 'left', 'width': '20%'}),

        ],
    ),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'Economy (GDP per Capita)', 'value': 'Economy (GDP per Capita)'},
                {'label': 'Social support', 'value': 'Social support'},
                {'label': 'Health (Life Expectancy)', 'value': 'Health (Life Expectancy)'},
                {'label': 'Freedom to make life choice', 'value': 'Freedom'},
                {'label': 'Generosity', 'value': 'Generosity'},
                {'label': 'Trust (Government Corruption)', 'value': 'Trust (Government Corruption)'},
            ],
            value='Economy (GDP per Capita)',
            placeholder="select a factor",
            id="select_factor",
            style={'width': '40%', 'float': 'right', 'margin-right': '100px'}
        ),
    ]),
    #initial parallel plot
    html.Div(
        [
            dcc.Graph(id='factor_parallel_plot',style={'width':'50%','float':'left'}),
            dcc.Graph(id='dot_factor_graph', style={'width': '50%', 'float': 'right'})
        ], style={'height':'500px'}
    ),
    html.Div([
        # dcc.Dropdown(
        #     options=[
        #         {'label': k, 'value': k} for k in all_country_option
        #     ],
        #     value=['Denmark'],
        #     multi=True,
        #     style={'padding-left':'1%','width':'65%', 'float':'left'},
        #     placeholder="Select a Country or Region to see the change of the rank of happiness during 2015-2021",
        #     id='select_country',
        # ),
        # dcc.Dropdown(
        #     options=[
        #         {'label': k, 'value': k} for k in all_country_option
        #     ],
        #  #   style={'width': '60%', 'float': 'right', 'margin-right':'10%'},
        #     style={'width':'50%', 'float':'left','margin-top':'-18px', 'margin-left':'33%'},
        #     placeholder="Select a Country or Region to see the change of different factors during 2015-2021",
        #     id='select_factor_by_country',
        #     searchable=True
        # )
    ]),
    html.Div([
        # dcc.Graph(id='radar_region_economy', style={'width': '45%', 'float': 'left'}),
        # dcc.Graph(id='factors_country', style={'width': '45%', 'float': 'left', 'margin-left':'10px'})
      ]
    ),
    html.Div(
        [
            html.Img(
                src=app.get_asset_url('allCountries1.png')
            )
        ], style={'width':'100%'}
    )
])

#remember to change in the future
def getValue(year, way, factor):
    file = str(year) + "_new3.csv"
    countries = pd.read_csv(file)
    values = [0] * 10
    num = [0] * 10
    dict = {'Central and Eastern Europe':0,
            'Commonwealth of Independent States':1,
            'Southeast Asia':2,
            'Middle East and North Africa':3,
            'Western Europe':4,
            'Latin America and Caribbean':5,
            'North America and ANZ':6,
            'Sub-Saharan Africa':7,
            'East Asia':8,
            'South Asia':9}
    dict_value = {
        'developed':0,
        'developing':1,
        'least':2
    }
    if way == 'Region':
        for index, country in countries.iterrows():
            values[dict.get(country['Region'])] += float(country[factor])
            num[dict.get(country['Region'])] += 1
    elif way == 'Economy':
        for index, country in countries.iterrows():
            values[dict_value.get(country['TYPE'])] += float(country[factor])
            num[dict_value.get(country['TYPE'])] += 1
    for i in range(len(values)):
        if num[i] == 0:
            values[i] = 0
        else:
            values[i] = values[i]*1.0/num[i]
    return values

@app.callback(
    Output(component_id='dot_factor_graph', component_property='figure'),
    [
        Input(component_id='select_year', component_property='value'),
        Input(component_id='select_factor', component_property='value')
    ]
)
def getFactorInfluence(year, factor):
    file = str(year) + "_new3.csv"
    countries = pd.read_csv(file)
    factorScore = []
    totalScore = []
    countryName = []
    for index, country in countries.iterrows():
        factorScore.append(country[factor])
        totalScore.append(country["Happiness Score"])
        countryName.append(country["Country"])
    df = {}
    df[factor]=factorScore
    df["Total Score"] = totalScore
    fig = px.scatter(df, x=factor, y="Total Score", trendline="ols", hover_name=countryName)
    fig.update_layout(plot_bgcolor="white")
    return fig


@app.callback(
    Output(component_id='radar_region_economy', component_property='figure'),
    [
        Input(component_id='select_year', component_property= 'value'),
        Input(component_id='select_region_economy', component_property= 'value'),
        Input(component_id='radar_region_economy', component_property='clickData')
    ]
)
def percentRegionEconomy(year, way, clickData):
    file = str(year) + "_new3.csv"
    fig = go.Figure()
    if way == 'Region':
        labels = ['Central and Eastern Europe',
                  'Commonwealth of Independent States',
                  'Southeast Asia',
                  'Middle East and North Africa',
                  'Western Europe',
                  'Latin America and Caribbean',
                  'North America and ANZ',
                  'Sub-Saharan Africa',
                  'East Asia',
                  'South Asia']
        Central_and_Eastern_Europe = []
        Commonwealth_of_Independent_States = []
        Southeast_Asia = []
        Middle_East_and_North_Africa =[]
        Western_Europe = []
        Latin_America_and_Caribbean = []
        North_America_and_ANZ = []
        sub_Saharan_Africa = []
        east_asia = []
        south_asia = []
        countries = pd.read_csv(file)
        for index, country in countries.iterrows():
            if country['Region'] == 'Central and Eastern Europe':
                Central_and_Eastern_Europe.append(country['Happiness Score'])
            elif country['Region'] == 'Commonwealth of Independent States':
                Commonwealth_of_Independent_States.append(country['Happiness Score'])
            elif country['Region'] == 'Southeast Asia':
                Southeast_Asia.append(country['Happiness Score'])
            elif country['Region'] == 'Middle East and North Africa':
                Middle_East_and_North_Africa.append(country['Happiness Score'])
            elif country['Region'] == 'Western Europe':
                Western_Europe.append(country['Happiness Score'])
            elif country['Region'] == 'Latin America and Caribbean':
                Latin_America_and_Caribbean.append(country['Happiness Score'])
            elif country['Region'] == 'North America and ANZ':
                North_America_and_ANZ.append(country['Happiness Score'])
            elif country['Region'] == 'Sub-Saharan Africa':
                sub_Saharan_Africa.append(country['Happiness Score'])
            elif country['Region'] == 'East Asia':
                east_asia.append(country['Happiness Score'])
            elif country['Region'] == 'South Asia':
                south_asia.append(country['Happiness Score'])
        fig.add_trace(go.Box(
            y=Central_and_Eastern_Europe,
            name="Central and Eastern Europe",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=Commonwealth_of_Independent_States,
            name="Commonwealth of Independent States",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=Southeast_Asia,
            name="Southeast Asia",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=Middle_East_and_North_Africa,
            name="Middle East and North Africa",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=Western_Europe,
            name="Western Europe",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=Latin_America_and_Caribbean,
            name="Latin America and Caribbean",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=North_America_and_ANZ,
            name="North America and ANZ",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=sub_Saharan_Africa,
            name="Sub-Saharan Africa",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=east_asia,
            name="East Asia",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=south_asia,
            name="South Asia",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
    elif way == 'Economy':
        label_economy = [
            'Developed Country',
            'Developing Country',
            'Least Developed Country'
        ]
        countries = pd.read_csv(file)
        developed = []
        developing = []
        least = []
        for index, country in countries.iterrows():
            if country['TYPE'] == 'developed':
                developed.append(country['Happiness Score'])
            elif country['TYPE'] == 'developing':
                developing.append(country['Happiness Score'])
            else:
                least.append(country['Happiness Score'])
        fig.add_trace(go.Box(
            y=developed,
            name="Developed Country",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=developing,
            name="Developing Country",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
        fig.add_trace(go.Box(
            y=least,
            name="Least Developed Country",
            boxpoints=False,  # no data points
            marker_color='rgb(9,56,125)',
            line_color='rgb(9,56,125)'
        ))
    # values = getValue(year, way)
    # if way == 'Region':
    #     fig = go.Figure(data=go.Scatterpolar(
    #         r=values,
    #         theta=labels,
    #         fill='toself'
    #     ))
    # elif way == 'Economy':
    #     fig = go.Figure(data=go.Scatterpolar(
    #         r=values,
    #         theta=label_economy,
    #         fill='toself'
    #     ))
    # fig.update_layout(
    #     polar=dict(
    #         radialaxis=dict(
    #             visible=True
    #         ),
    #     ),
    #     showlegend=False,
    #     title_text="The Happiness Average Score in Region"
    # )


    fig.update_layout(title_text="Compare with different Regions")
    fig.update_layout(plot_bgcolor="white")
    return fig

#input : country be chosen
#output:countries score during 2015-2021 lien chart
# @app.callback(
#        Output(component_id='all_country_compare_score', component_property='figure'),
#         # Output(component_id='all_country_compare_rank', component_property='figure'),
#
#     [Input(component_id='select_country', component_property='value')]
# )
# def allCountryCompare(choseCountries):
#     worldCloudText = ''
#     scoreFig = go.Figure()
#     rankFig = go.Figure()
#     years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
#     for country in choseCountries:
#         happiness_score = []
#         for year in years:
#             file = pd.read_csv(str(year)+"_new3.csv")
#             for index, data in file.iterrows():
#                 if data["Country"] == country:
#                     happiness_score.append(data["Happiness Score"])
#                     break
#         scoreFig.add_trace(go.Scatter(
#             x=years,
#             y=happiness_score,
#             name=country,
#             connectgaps=True
#         ))
#
#     j = 0
#     # Create figure
#     points = []
#     for country in choseCountries:
#         happiness_score = []
#         happiness_rank = []
#         for year in years:
#             file = pd.read_csv(str(year) + "_new3.csv")
#             for index, data in file.iterrows():
#                 if data["Country"] == country:
#                     happiness_score.append(data["Happiness Score"])
#                     happiness_rank.append(data["Happiness Rank"])
#                     worldCloudText += ' '
#                     worldCloudText += str(year)
#                     worldCloudText += country
#                     worldCloudText += 'RANK'
#                     worldCloudText += str(data["Happiness Rank"])
#                     break
#         j += 1
#         j*= 10
#         points.append(go.Scatter(
#                 x=years, y=happiness_rank,
#                 mode='markers',
#                 marker_size=[np.exp(int(happiness_score[i]))/10 for i in range(len(happiness_score))],
#                 name=country
#             ))
#     rankFig = go.Figure(data=points)
#     scoreFig.update_layout(title_text="Countries score change from 2015 to 2021")
#     rankFig.update_layout(title_text="Countries rank change from 2015 to 2021")
#     return scoreFig


@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='world_map_happiness', component_property="figure"),
        Output(component_id='country_top_ten', component_property="figure"),
    ],
    [Input(component_id='select_year', component_property='value'),
     Input(component_id='radar_region_economy', component_property='clickData')
     ]
)
def yearCompare(year, clickData):
    region = 'Total Countries'
    if clickData == None:
        region = 'Total Countries'
    else:
        # print("clickData = ", clickData)
        # print(clickData['points'][0]['x'])
        region = clickData['points'][0]['x']
    if region == "Developed Country":
        region = 'developed'
    elif region == 'Developing Country':
        region = 'developing'
    elif region == 'Least Developed Country':
        region = 'least'
    container = "The year chosen by user is: {}".format(year)
    #fileName = str(year)+".csv"
    file = str(year) + "_new3.csv"
    #Get all countries name
    countryMap = pd.read_csv(file)
    fig = go.Figure(data=go.Choropleth(
        locations=countryMap['CODE'],
        z=countryMap['Happiness Score'],
        text=countryMap['Country'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Total score',
    ))
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    world_title = "{0} World Happiness map".format(year)
    fig.update_layout(
        title_text=world_title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )
    regionBar = []
    economy = []
    social_support = []
    health = []
    freedom = []
    generosity = []
    trust = []
    dystopia_residual = []
    countryName = []
    if region == 'Total Countries':
        countries = pd.read_csv(file, nrows=10)
        for index, country in countries.iterrows():
            countryName.append(country["Country"])
            economy.append(country["Economy (GDP per Capita)"])
            social_support.append(country["Social support"])
            health.append(country["Health (Life Expectancy)"])
            freedom.append(country["Freedom"])
            generosity.append(country["Generosity"])
            trust.append(country["Trust (Government Corruption)"])
            dystopia_residual.append(country["Dystopia Residual"])
    elif region == 'developed':
        countries = pd.read_csv(file)
        for index, country in countries.iterrows():
            if country["TYPE"] == region:
                countryName.append(country["Country"])
                economy.append(country["Economy (GDP per Capita)"])
                social_support.append(country["Social support"])
                health.append(country["Health (Life Expectancy)"])
                freedom.append(country["Freedom"])
                generosity.append(country["Generosity"])
                trust.append(country["Trust (Government Corruption)"])
                dystopia_residual.append(country["Dystopia Residual"])
    elif region == 'developing':
        countries = pd.read_csv(file)
        for index, country in countries.iterrows():
            if country["TYPE"] == region:
                countryName.append(country["Country"])
                economy.append(country["Economy (GDP per Capita)"])
                social_support.append(country["Social support"])
                health.append(country["Health (Life Expectancy)"])
                freedom.append(country["Freedom"])
                generosity.append(country["Generosity"])
                trust.append(country["Trust (Government Corruption)"])
                dystopia_residual.append(country["Dystopia Residual"])
    elif region == 'least':
        countries = pd.read_csv(file)
        for index, country in countries.iterrows():
            if country["TYPE"] == region:
                countryName.append(country["Country"])
                economy.append(country["Economy (GDP per Capita)"])
                social_support.append(country["Social support"])
                health.append(country["Health (Life Expectancy)"])
                freedom.append(country["Freedom"])
                generosity.append(country["Generosity"])
                trust.append(country["Trust (Government Corruption)"])
                dystopia_residual.append(country["Dystopia Residual"])
    else:
        countries = pd.read_csv(file)
        for index, country in countries.iterrows():
            if country["Region"] == region:
                countryName.append(country["Country"])
                economy.append(country["Economy (GDP per Capita)"])
                social_support.append(country["Social support"])
                health.append(country["Health (Life Expectancy)"])
                freedom.append(country["Freedom"])
                generosity.append(country["Generosity"])
                trust.append(country["Trust (Government Corruption)"])
                dystopia_residual.append(country["Dystopia Residual"])
    regionBar = go.Figure(data=[
        go.Bar(name='Economy (GDP per Capita)', y=countryName, x=economy,orientation='h'),
        go.Bar(name='Social support', y=countryName, x=social_support,orientation='h'),
        go.Bar(name='Health (Life Expectancy)', y=countryName, x=health,orientation='h'),
        go.Bar(name='Freedom to make life choice', y=countryName, x=freedom,orientation='h'),
        go.Bar(name='Generosity', y=countryName, x=generosity,orientation='h'),
        go.Bar(name='Trust (Government Corruption)', y=countryName, x=trust,orientation='h'),
        go.Bar(name='Dystopia Residual', y=countryName, x=dystopia_residual,orientation='h')
    ])

    regionBar.update_layout(barmode='stack')
    if region == 'developed' or region == 'developing':
        region += ' countries'
    elif region == 'least':
        region = 'least developed countries'
    if region == 'Total Countries':
        title = "The top 10 happiest countries in {0}".format(year)
    else:
        title = "The happiness rank in {0} in {1}".format(region, year)
    regionBar.update_layout(title_text=title)
    regionBar.update_layout(plot_bgcolor="white")

    return container, fig, regionBar


#initial parallel data
#remember if only one output never use []
@app.callback(
    Output(component_id='factor_parallel_plot', component_property='figure'),
    [
        Input(component_id='select_year', component_property='value')
    ]
)
def getParallelData(year):
    file = str(year) + "_new3.csv"
    df = pd.read_csv(file)
    fig = go.Figure(data=
    go.Parcoords(
        dimensions=list([
            dict(range=[3, 8],
                 label='Happiness Score', values=df['Happiness Score']),
            dict(range=[0, 2],
                 label='Economy (GDP per Capita)', values=df['Economy (GDP per Capita)']),
            dict(range=[0, 1],
                 label='Health (Life Expectancy)', values=df['Health (Life Expectancy)']),
            dict(range=[0, 1],
                 label='Freedom', values=df['Freedom']),
            dict(range=[0, 1],
                 label='Generosity', values=df['Generosity']),
            dict(range=[0, 1],
                 label='Trust (Government Corruption)', values=df['Trust (Government Corruption)'])
        ])
    )
    )

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    return fig

#
# @app.callback(
#     Output(component_id='factors_country', component_property='figure'),
#     [
#         Input(component_id='select_factor_by_country', component_property='value')
#     ]
# )
# def select_country_by_factor(country):
#     factorFig = go.Figure()
#     years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
#     happiness_score = []
#     economy = []
#     social = []
#     health = []
#     Freedom = []
#     Generosity = []
#     Trust = []
#     for year in years:
#         file = pd.read_csv(str(year)+"_new3.csv")
#         for index, data in file.iterrows():
#             if data["Country"] == country:
#                 happiness_score.append(data["Happiness Score"])
#                 economy.append(data['Economy (GDP per Capita)'])
#                 social.append(data['Social support'])
#                 health.append(data['Health (Life Expectancy)'])
#                 Freedom.append(data['Freedom'])
#                 Generosity.append(data['Generosity'])
#                 Trust.append(data['Trust (Government Corruption)'])
#                 break
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=economy,
#         name="Economy (GDP per Capita)",
#         connectgaps=True
#     ))
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=social,
#         name="Social support",
#         connectgaps=True
#     ))
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=health,
#         name="Health (Life Expectancy)",
#         connectgaps=True
#     ))
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=Freedom,
#         name="Freedeom to make life choice",
#         connectgaps=True
#     ))
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=Generosity,
#         name="Generosity",
#         connectgaps=True
#     ))
#     factorFig.add_trace(go.Scatter(
#         x=years,
#         y=Trust,
#         name="Government Corruption",
#         connectgaps=True
#     ))
#     factorFig.update_layout(title_text="Happiness factor change from 2015 to 2021")
#     return factorFig


@app.callback(
    [Output('factors_country', 'figure'),
     Output('figTotal', 'figure')
     ],
    [Input('world_map_happiness', 'clickData')]
)
def mapClickEvent(clickData):
    if clickData == None:
        clickData ={'points': [{'curveNumber': 0, 'pointNumber': 63, 'pointIndex': 63, 'location': 'RUS', 'z': 5.716, 'text': 'China', 'bbox': {'x0': 1142.0527561417348, 'x1': 1142.0527561417348, 'y0': 219.77328636984856, 'y1': 219.77328636984856}}]}
    country = clickData['points'][0]['text']
    factorFig = go.Figure()
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
    happiness_score = []
    economy = []
    social = []
    health = []
    Freedom = []
    Generosity = []
    Trust = []
    HappinessScore = []
    DystopiaResidual=[]
    for year in years:
        file = pd.read_csv(str(year) + "_new3.csv")
        for index, data in file.iterrows():
            if data["Country"] == country:
                happiness_score.append(data["Happiness Score"])
                economy.append(data['Economy (GDP per Capita)'])
                social.append(data['Social support'])
                health.append(data['Health (Life Expectancy)'])
                Freedom.append(data['Freedom'])
                Generosity.append(data['Generosity'])
                Trust.append(data['Trust (Government Corruption)'])
                HappinessScore.append(data['Happiness Score'])
                DystopiaResidual.append(data['Dystopia Residual'])
                break
    regionBar = go.Figure(data=[
        go.Bar(name='Economy (GDP per Capita)', y=economy),
        go.Bar(name='Social support',  y=social ),
        go.Bar(name='Health (Life Expectancy)',  y=health, ),
        go.Bar(name='Freedom to make life choice',  y=Freedom, ),
        go.Bar(name='Generosity',  y=Generosity),
        go.Bar(name='Trust (Government Corruption)', y=Trust),
    ])
    x=[2015,2016,2017,2018,2019,2020,2021]
    fig = go.Figure(go.Bar(name='Economy (GDP per Capita)', y=economy, x=x))
    fig.add_trace(go.Scatter(
        x=years,
        y=HappinessScore,
        name="HappinessScore",
        connectgaps=True
    ))
    fig.add_trace(go.Bar(name='Social support',  y=social,x=x))
    fig.add_trace( go.Bar(name='Health (Life Expectancy)',  y=health,x=x))
    fig.add_trace(go.Bar(name='Generosity',  y=Generosity,x=x))
    fig.add_trace(go.Bar(name='Trust (Government Corruption)', y=Trust,x=x))
    fig.add_trace(go.Bar(name='Generosity', y=Generosity,x=x))
    fig.add_trace(go.Bar(name='Dystopia Residual', y=DystopiaResidual, x=x))

    regionBar.update_layout(barmode='stack')
    factorFig.add_trace(go.Scatter(
        x=years,
        y=economy,
        name="Economy (GDP per Capita)",
        connectgaps=True
    ))
    factorFig.add_trace(go.Scatter(
        x=years,
        y=social,
        name="Social support",
        connectgaps=True
    ))
    factorFig.add_trace(go.Scatter(
        x=years,
        y=health,
        name="Health (Life Expectancy)",
        connectgaps=True
    ))
    factorFig.add_trace(go.Scatter(
        x=years,
        y=Freedom,
        name="Freedeom to make life choice",
        connectgaps=True
    ))
    factorFig.add_trace(go.Scatter(
        x=years,
        y=Generosity,
        name="Generosity",
        connectgaps=True
    ))
    factorFig.add_trace(go.Scatter(
        x=years,
        y=Trust,
        name="Government Corruption",
        connectgaps=True
    ))
    factorFig.update_layout(title_text= country +"'s Happiness Score change from 2015 to 2021",    plot_bgcolor="white")
    figTotal = go.Figure(data=go.Scatter(x=x, y=HappinessScore, name='Happiness Score'))
   # fig.update_layout(barmode='stack')
    figTotal.update_layout( plot_bgcolor="white")
    return factorFig, figTotal

@app.callback(
    [
        Output('radar_economy', 'figure'),
        Output('radar_trust', 'figure'),
        Output('radar_freedom', 'figure'),
        Output('radar_health', 'figure'),
        Output('radar_support', 'figure'),
    ],
    [
        Input(component_id='select_year', component_property='value'),
        Input('select_region_economy', component_property='value')
    ]
)
def radar_all(year, radar_factor):
    file = str(year) + "_new3.csv"
    countries = pd.read_csv(file)
    if radar_factor == 'Region':
        labels = ['Central and Eastern Europe',
                  'Commonwealth of Independent States',
                  'Southeast Asia',
                  'Middle East and North Africa',
                  'Western Europe',
                  'Latin America and Caribbean',
                  'North America and ANZ',
                  'Sub-Saharan Africa',
                  'East Asia',
                  'South Asia']
    elif radar_factor == 'Economy':
        labels = [
            'Developed Country',
            'Developing Country',
            'Least Developed Country'
        ]
    economy = getValue(year, radar_factor, 'Economy (GDP per Capita)')
    fig_economy = go.Figure(data=go.Scatterpolar(
        r=economy,
        theta=labels,
        fill='toself',
        marker_color='rgb(9,56,125)',
        line_color='rgb(9,56,125)'
    ))
    trust = getValue(year, radar_factor, 'Trust (Government Corruption)')
    fig_trust = go.Figure(data=go.Scatterpolar(
        r=trust,
        theta=labels,
        fill='toself',
        marker_color='rgb(9,56,125)',
        line_color='rgb(9,56,125)'
    ))
    freedom = getValue(year, radar_factor, 'Freedom')
    fig_freedom = go.Figure(data=go.Scatterpolar(
        r=freedom,
        theta=labels,
        fill='toself',
        marker_color='rgb(9,56,125)',
        line_color='rgb(9,56,125)'
    ))
    health = getValue(year, radar_factor, 'Health (Life Expectancy)')
    fig_health = go.Figure(data=go.Scatterpolar(
        r=health,
        theta=labels,
        fill='toself',
        marker_color='rgb(9,56,125)',
        line_color='rgb(9,56,125)'
    ))
    support = getValue(year, radar_factor, 'Social support')
    fig_support = go.Figure(data=go.Scatterpolar(
        r=support,
        theta=labels,
        fill='toself',
        marker_color='rgb(9,56,125)',
        line_color='rgb(9,56,125)'
    ))

    fig_economy.update_layout(title_text="Economy")
    fig_trust.update_layout(title_text="Trust of Government")
    fig_freedom.update_layout(title_text="Freedom to make life Choice")
    fig_health.update_layout(title_text="Health")
    fig_support.update_layout(title_text="Social Support")

    return fig_economy,fig_trust,fig_freedom,fig_health,fig_support


if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8081", debug=True)
