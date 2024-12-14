import plotly.graph_objects as go

def time_series(years, values):

    avg_value = sum(values) / len(values)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=years,
            y=values,
            mode='lines+markers',
            line=dict(color='rgb(11, 102, 189)', width=3),
            marker=dict(size=12, color='black'),
            name='Occurrences'
        )
    )

    # Adicionar a linha média
    fig.add_trace(
        go.Scatter(
            x=years,
            y=[avg_value] * len(years),
            mode='lines',
            line=dict(color='black', dash='dash'),
            name='Average'
        )
    )

    # Atualizar o layout
    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        font=dict(color='black'),
        xaxis=dict(title="Year"),
        yaxis=dict(title="Occurrences"),
        margin=dict(l=20, r=20, t=40, b=20),
    )
    
    return fig




