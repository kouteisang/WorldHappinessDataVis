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
    html.H1("World Happiness Report Data Visulization from 2015 to 2021", style={'text-align': 'center','background-color':'#4797c6','color':'white'}),
    html.Div(id='output_container', children=[]),
    dcc.Slider(
        id="select_year",
        min=2015,
        max=2021,
        marks={i: 'Year {}'.format(i) for i in range(2015,2022,1)},
        value=2015,
    ),
    html.Div(
        [    dcc.Graph(id='world_map_happiness', style={'width':'55%','float':'left'}),
            dcc.Graph(id='country_top_ten', style={'width':'45%','float':'left'})]
    ),
    html.Div([
        dcc.RadioItems(
            options=[
                {'label': 'Region', 'value': 'Region'},
                {'label': 'Economy', 'value': 'Economy'},
            ],
            value='Region',
            id="select_region_economy",
            style={'float':'left'}
        ),
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
            style={'float': 'right','width':'60%','margin-right':'10%'}
        ),
    ]),
    html.Div([
        dcc.Graph(id='pie_region_economy', style={'width': '40%', 'float': 'left'}),
        dcc.Graph(id='dot_factor_graph', style = {'width':'60%', 'float':'right'})
        ]
    ),
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': k, 'value': k} for k in all_country_option
            ],
            value=['Denmark'],
            multi=True,
            style={'padding-left':'1%','width':'65%'},
            placeholder="Select a Country or Region to see the change of the rank of happiness during 2015-2021",
            id='select_country',
        )
    ], style={'padding-top':'10%'}),
    html.Div(
        [dcc.Graph(id='all_country_compare_score', style={'width': '45%', 'float': 'left'}),
         dcc.Graph(id='all_country_compare_rank', style={'width': '45%','float': 'left'})],

    ),

])

#remember to change in the future
def getValue(year, way):
    countries = pd.read_csv("2021.csv", nrows=50)
    values = [0] * 10
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

    if way == 'Region':
        for index, country in countries.iterrows():
            print(country['Region'])
            values[dict.get(country['Region'])] += 1
    return values



@app.callback(
    Output(component_id='dot_factor_graph', component_property='figure'),
    [
        Input(component_id='select_year', component_property='value'),
        Input(component_id='select_factor', component_property='value')
    ]
)
def getFactorInfluence(year, factor):
    print(year)
    print(factor)
    fileName = "2021.csv"
    countries = pd.read_csv(fileName)
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
    return fig


@app.callback(
    Output(component_id='pie_region_economy', component_property='figure'),
    [
        Input(component_id='select_year', component_property= 'value'),
        Input(component_id='select_region_economy', component_property= 'value')
    ]
)
def percentRegionEconomy(year, way):
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

    values = getValue(year, way)
    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    return fig

#input : country be chosen
#output:countries score during 2015-2021 lien chart
@app.callback(
    [   Output(component_id='all_country_compare_score', component_property='figure'),
        Output(component_id='all_country_compare_rank', component_property='figure'),
    ],
    [Input(component_id='select_country', component_property='value')]
)
def allCountryCompare(choseCountries):
    scoreFig = go.Figure()
    rankFig = go.Figure()
    years = [2015, 2016, 2017, 2018, 2019, 2020, 2021]
    for country in choseCountries:
        happiness_score = []
        for year in years:
            file = pd.read_csv(str(year)+".csv")
            for index, data in file.iterrows():
                if data["Country"] == country:
                    happiness_score.append(data["Happiness Score"])
                    print(happiness_score)
                    break
        scoreFig.add_trace(go.Scatter(
            x=years,
            y=happiness_score,
            name=country,
            connectgaps=True
        ))

    j = 0
    # Create figure
    points = []
    for country in choseCountries:
        happiness_score = []
        happiness_rank = []
        for year in years:
            file = pd.read_csv(str(year) + ".csv")
            for index, data in file.iterrows():
                if data["Country"] == country:
                    happiness_score.append(data["Happiness Score"])
                    happiness_rank.append(data["Happiness Rank"])
                    break
        j += 1
        j*= 10
        points.append(go.Scatter(
                x=years, y=happiness_rank,
                mode='markers',
                marker_size=[np.exp(int(happiness_score[i]))/10 for i in range(len(happiness_score))],
                name=country
            ))
        print([j for i in range(len(happiness_score))])
        print([int(happiness_score[i]*3) for i in range(len(happiness_score))])
    rankFig = go.Figure(data=points)
    scoreFig.update_layout(title_text="Countries score change from 2015 to 2021")
    rankFig.update_layout(title_text="Countries rank change from 2015 to 2021")
    return scoreFig, rankFig


@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='world_map_happiness', component_property="figure"),
        Output(component_id='country_top_ten', component_property="figure"),
    ],
    [Input(component_id='select_year', component_property='value')]
)
def yearCompare(year):
    container = "The year chosen by user is: {}".format(year)
    #fileName = str(year)+".csv"
    fileName = "2021.csv"
    #Get all countries name
    countryMap = pd.read_csv(fileName)
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
    world_title = "{0} World Happiness map".format(year)
    fig.update_layout(
        title_text=world_title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        annotations=[dict(
            x=0.55,
            y=0.1,
            xref='paper',
            yref='paper',
            showarrow=False
        )]
    )

    top10CountryName = []
    economy = []
    social_support = []
    health = []
    freedom = []
    generosity = []
    trust = []
    dystopia_residual = []
    countries = pd.read_csv("2021.csv", nrows=10)
    for index, country in countries.iterrows():
        top10CountryName.append(country["Country"])
        economy.append(country["Economy (GDP per Capita)"])
        social_support.append(country["Social support"])
        health.append(country["Health (Life Expectancy)"])
        freedom.append(country["Freedom"])
        generosity.append(country["Generosity"])
        trust.append(country["Trust (Government Corruption)"])
        dystopia_residual.append(country["Dystopia Residual"])


    top10BarChart = go.Figure(data=[
        go.Bar(name='Economy (GDP per Capita)', x=top10CountryName, y=economy),
        go.Bar(name='Social support', x=top10CountryName, y=social_support),
        go.Bar(name='Health (Life Expectancy)', x=top10CountryName, y=health),
        go.Bar(name='Freedom to make life choice', x=top10CountryName, y=freedom),
        go.Bar(name='Generosity', x=top10CountryName, y=generosity),
        go.Bar(name='Trust (Government Corruption)', x=top10CountryName, y=trust),
        go.Bar(name='Dystopia Residual', x=top10CountryName, y=dystopia_residual)
    ])
    top10BarChart.update_layout(barmode='stack')
    title = "The top 10 happiest countries in {0}".format(year)
    top10BarChart.update_layout(title_text=title)
    return container, fig, top10BarChart






if __name__ == '__main__':
    app.run_server(host="0.0.0.0", port="8080", debug=True)
