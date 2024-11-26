import plotly.graph_objects as go
import pandas as pd
from typing import Union, List, Dict

def G_local(Municipios: pd.Series,
            gi: Union[pd.Series, List[float]],
            geojson: Dict, 
            indices: Union[pd.Series, List[Union[str, int]]]) -> go.Figure:

    """
    Plots a Choropleth map to identify Hotspots and Coldspots using Gi* statistics.

    Args:
        Municipios (pd.Series or list of str): A series or list containing the names of the municipalities.
        gi (pd.Series or list of float): A series or list containing the Gi* Z-scores for each municipality.
        geojson (dict): A GeoJSON dictionary containing the geographical features of the municipalities.
        indices (pd.Series or list of str or int): A series or list containing the indices or IDs matching the 'locations' in the GeoJSON.

    Returns:
        go.Figure: A Plotly Figure object containing the Choropleth map.
        
    """
    
    hover = 'Município: ' + Municipios + '<br> Z-score: ' + gi.round(2).astype(str)

    fig = go.Figure()
    fig.add_trace(go.Choroplethmap(
        geojson=geojson,
        locations=indices,
        z=gi,
        marker_opacity=1,
        marker_line_width=0.5,
        text=hover,
        hoverinfo='text',
        colorscale=[[0, 'rgb(23, 28, 66)'], [0.5, 'lightgray'], [1, 'rgb(120, 0, 0)']],
        colorbar=dict(title="Categorias",
                      tickvals=[gi.min(), gi.median(), gi.max()],
                      ticktext=['Coldspot', 'Não significativo', 'Hotspot']))
    )
    
    fig.update_layout(
        title = "Identificação de Hot e Coldspots pela Gi*",
        map_zoom=5.4,
        map_center={"lat": -22.45, "lon": -48.63},
        map_style ='carto-positron',
    )
  
    return fig

