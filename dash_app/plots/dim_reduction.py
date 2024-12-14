import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE, MDS
from umap import UMAP

def dim_reduction(dr_method: str, df: pd.DataFrame,
                  geojson, regiao_intermediaria, geojson_NRGInter) -> go.Figure:
    """
    
    Parâmetros:
    - dr_method: str - tipo de redução de dimensionalidade ('UMAP', 'TSNE', 'PCA', 'MDS', etc.)
    - df: pd.DataFrame - dataframe contendo as colunas 'Municipio', 'NRGInter' e variáveis numéricas.
    
    Retorna:
    - fig: plotly.graph_objects.Figure
    """
    
    non_numeric = ['Municipio', 'NRGInter', 'geometry']
    features = [col for col in df.columns if col not in non_numeric]
    
    X = df[features].dropna(axis=0)  
    municipios = df.loc[X.index, 'Municipio']
    regioes_intermediarias = df.loc[X.index, 'NRGInter']
    
    # Selecionar o método de redução
    dr_method = dr_method.upper()
    if dr_method == 'PCA':
        reducer = PCA(n_components=2)
    elif dr_method == 'TSNE':
        reducer = TSNE(n_components=2, random_state=42)
    elif dr_method == 'UMAP':
        reducer = UMAP(n_components=2, random_state=42)
    elif dr_method == 'MDS':
        reducer = MDS(n_components=2, random_state=42)
    else:
        raise ValueError(f"Method {dr_method} not recognized. Choose from 'UMAP', 'TSNE', 'PCA', 'MDS'.")

    embedding = reducer.fit_transform(X)
    
    x_coords = embedding[:, 0]
    y_coords = embedding[:, 1]
    
    unique_regions = regioes_intermediarias.unique()
    color_map = {region: px.colors.qualitative.Set2[i % len(px.colors.qualitative.Set2)]
                 for i, region in enumerate(unique_regions)}

    # Criar figura iterativa
    fig = go.Figure()
    for region in unique_regions:
        # Filtrar os dados para cada região intermediária
        region_mask = regioes_intermediarias == region
        fig.add_trace(
            go.Scatter(
                x=x_coords[region_mask],
                y=y_coords[region_mask],
                mode='markers',
                marker=dict(
                    size=7,
                    color=color_map[region],  # Cor única para cada região
                ),
                name=region,  # Nome da região para a legenda
                text=municipios[region_mask],
                hovertemplate="<b>Municipio:</b> %{text}<br>" +
                              f"<b>NRGInter:</b> {region}<extra></extra>"
            )
        )

    # Atualizar layout
    fig.update_layout(
        title=f"{dr_method} 2D Projection",
        xaxis_title='Dimension 1',
        yaxis_title='Dimension 2',
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color='black'),
        legend_title="Intermediate Regions",
    )

    map_projection = go.Figure()
    
    map_projection.add_trace(go.Choroplethmap(
        geojson=geojson,
        locations=df.index,
        z=x_coords,
        colorscale='RdBu',
        marker_opacity=0.8,
        marker_line_width=0.5,
        text=df['Municipio'],
        hoverinfo='text+z',
        showscale=True,
        colorbar=dict(
        title=f"{dr_method} 1° Component",  # Substitua pelo título desejado
        titlefont=dict(size=12)  # Tamanho da fonte do título
    ))
                             )

    map_projection.add_trace(go.Choroplethmap(
        geojson=geojson_NRGInter,
        locations=regiao_intermediaria.index,
        z=regiao_intermediaria['const'],
        colorscale=[[0, 'rgba(255, 255, 255, 0)'], [1, 'rgba(255, 255, 255, 0)']],
        marker_opacity=0.4,
        marker_line_width=1.3,
        marker_line_color='rgba(0, 0, 0, 1)',
        showscale=False,
        showlegend=False,
        hoverinfo='skip')
                             
    )
    
    map_projection.update_layout(
        map_zoom=5.6,
        title=f"{dr_method} 1D Map Projection",
        paper_bgcolor = "rgba(0, 0, 0, 0)",
        font=dict(color='black'),
        map_center={"lat": -22.45, "lon": -48.63}, 
        map_style='carto-positron',
    )
    
    
    return fig, map_projection
