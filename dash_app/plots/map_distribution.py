import geopandas.geoseries
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import geopandas
import pandas as pd
import json
from typing import Union, Dict, List

def mapa_dist(geojson: Dict,
              indices: Union[pd.Series, List[Union[str, int]]],
              municipios: Union[pd.Series, List[str]],
              variavel_interesse: Union[pd.Series, List[float]],
              nome_variavel_interesse: str,
              geojson_regiao_imediata: Dict,
              indices_regiao_imediata: Union[pd.Series, List[Union[str, int]]],
              constante: Union[pd.Series, List[float]]) -> go.Figure:   
    
    """
    Plots a choropleth map showing the distribution of a variable of interest across municipalities,
    with immediate regions overlaid.

    Args:
        geojson (dict): GeoJSON data for the municipalities.
        indices (pd.Series or list): Municipality indices corresponding to the 'locations' in the GeoJSON.
        municipios (pd.Series or list): Municipality names.
        variavel_interesse (pd.Series or list): Values of the variable of interest for each municipality.
        nome_variavel_interesse (str): Name of the variable of interest (for labeling).
        geojson_regiao_imediata (dict): GeoJSON data for the immediate regions.
        indices_regiao_imediata (pd.Series or list): Region indices corresponding to the GeoJSON.
        constante (pd.Series or list): Constant values used to overlay the immediate regions.

    Returns:
        go.Figure: A Plotly Figure object containing the choropleth map.
    """
    
    colorscale = px.colors.diverging.balance
    
    fig = go.Figure()
    fig.add_trace(go.Choroplethmap(
        geojson=geojson,
        locations=indices,
        z=variavel_interesse,
        colorscale=colorscale,
        marker_opacity=0.8,
        marker_line_width=0.5,
        colorbar_title=f"Valor do {nome_variavel_interesse}",
        text=municipios,
        hoverinfo='text+z'
    ))
    
    fig.add_trace(go.Choroplethmap(
    geojson=geojson_regiao_imediata,
    locations=indices_regiao_imediata,
    z=constante,
    colorscale=[[0, 'rgba(255, 255, 255, 0)'], [1, 'rgba(255, 255, 255, 0)']],
    marker_opacity=0.4,
    marker_line_width=1.3,
    marker_line_color='rgba(0, 0, 0, 1)',
    showscale=False,
    showlegend=False,
    hoverinfo='skip',
    ))
    
    fig.update_layout(
        map_zoom=5.6,
        map_center={"lat": -22.45, "lon": -48.63}, 
        margin={"r":0,"t":0,"l":0,"b":0},
        map_style='carto-positron',
        paper_bgcolor = "rgba(0, 0, 0, 0)",
        font=dict(color='black'),
    )
    
    return fig
    



