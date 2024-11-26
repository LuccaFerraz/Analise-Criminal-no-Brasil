# Importar as bases já codificadas para os plots
import plotly.graph_objects as go
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Output, Input
from dash_app.plots.map_distribution import map_dist
import geopandas as gpd



app = Dash(
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True    
)

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

index_page = html.Div([
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(html.H1(children='Análise de Ocorrência Criminal'), width=5)
    ])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname): 
    return index_page

if __name__ == "__main__":
    app.run_server(debug=False)