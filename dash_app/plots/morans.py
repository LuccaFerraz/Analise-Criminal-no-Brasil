import plotly.graph_objects as go
from plotly.subplots import make_subplots

def morans_i(autocorr, morans_i_lag, geojson,
             geojson_regiao_imediata, indices_regiao_imediata,
             constante, variavel_interesse, variavel_interesse_lag):
    
    # Plot Morans'I e LISA
    fig = make_subplots(rows=1,
                        cols=2,
                        subplot_titles=(f"Moran's I Scatter Plot: {morans_i_lag.I:.3f}, p-valor: {morans_i_lag.p_sim}", "LISA Cluster Map"),
                        specs=[[{'type': 'scatter'}, {'type': 'choroplethmap'}]])

    fig.add_trace(
        go.Scatter(
            x=autocorr[variavel_interesse],
            y=autocorr[variavel_interesse_lag],
            mode='markers',
            text=autocorr['Municipio'],
            marker=dict(size=8, color='rgba(23, 28, 66, 0.7)'),
            showlegend=False),

        row=1, col=1
    )

    fig.add_trace(
        go.Scatter(
            x=[autocorr[variavel_interesse].min(), autocorr[variavel_interesse].max()],
            y=[autocorr[variavel_interesse_lag].min(), autocorr[variavel_interesse_lag].max()],
            mode='lines',
            line=dict(color='rgba(0, 0, 0, 0.6)', dash='dash'),
            showlegend=False
        ),
        row=1, col=1
    )

    fig.update_xaxes(title_text=f"Valores Observados ({variavel_interesse})", row=1, col=1) 
    fig.update_yaxes(title_text=f"Lag Espacial ({variavel_interesse_lag})", row=1, col=1)       

    fig.add_trace(
        go.Choroplethmap(
            geojson=geojson,
            locations=autocorr.index,
            z=autocorr['quadrant'],
            colorscale=[
            [0, 'lightgray'],
            [0.25, 'rgb(23, 28, 66)'],
            [0.5,'rgb(72, 202, 228)'],
            [0.75,'rgb(224, 30, 55)' ],
            [1, 'rgb(120, 14, 40)']
            ],
            marker_opacity=0.8,
            marker_line_width=0.5,
            text=autocorr['Municipio'],
            hoverinfo='text+z',
            showscale=False

    ), row=1, col=2)

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

    ), row=1, col=2)

    fig.update_layout(
        map_zoom=5.4,
        map_center={"lat": -22.45, "lon": -48.63},
        map_style ='carto-positron',
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font=dict(color='black')

    )

    return fig