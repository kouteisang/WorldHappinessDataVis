import pandas as pd
import plotly.express as px  # (version 4.7.0)
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("World Happiness Report Data Visulization", style={'text-align': 'center'}),
    html.Div(id='output_container', children=[]),
    dcc.Dropdown(id="select_year",
                 options=[
                     {"label": "2015", "value": 2015},
                     {"label": "2016", "value": 2016},
                     {"label": "2017", "value": 2017},
                     {"label": "2018", "value": 2018},
                     {"label": "2019", "value": 2019},
                     {"label": "2020", "value": 2020},
                     {"label": "2021", "value": 2021}],
                 multi=False,
                 value=2015,
                 style={'width': "40%"}
                 ),
    html.Br(),
    html.Div(
        [    dcc.Graph(id='world_map_happiness', style={'width':'60%','float':'left'}),
            dcc.Graph(id='country_top_ten', style={'width':'40%','float':'left'})]
    )

])

@app.callback(
    [
        Output(component_id='output_container', component_property='children'),
        Output(component_id='world_map_happiness', component_property="figure"),
        Output(component_id='country_top_ten', component_property="figure"),
    ],
    [Input(component_id='select_year', component_property='value')]
)
def getYear(year):
    container = "The year chosen by user is: {}".format(year)
    #fileName = str(year)+".csv"
    fileName = "2021.csv"
    countryMap = pd.read_csv(fileName)
    fig = go.Figure(data=go.Choropleth(
        locations=countryMap['CODE'],
        z=countryMap['Ladder score'],
        text=countryMap['Country name'],
        colorscale='Blues',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title='Total score',
    ))

    fig.update_layout(
        title_text='2021 World Happiness',
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
    top10CountryScore = []
    countryMap = pd.read_csv("2021.csv", nrows=10)
    countries = pd.read_csv("2021.csv", nrows=10)
    for index, country in countries.iterrows():
        top10CountryName.append(country["Country name"])
        top10CountryScore.append(country["Ladder score"])

    top10BarChart = go.Figure([go.Bar(x=top10CountryName, y=top10CountryScore)])

    return container, fig, top10BarChart






if __name__ == '__main__':
    app.run_server(debug=True)
