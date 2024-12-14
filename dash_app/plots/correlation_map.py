import plotly.graph_objects as go 

def correlation_map(df_selected):

    # Calculate the correlation matrix
    corr_matrix = df_selected.corr()

    # Create the heatmap figure
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.index,
        colorscale='RdBu',
        colorbar=dict(title="Correlation"),
        zmin=-1,
        zmax=1
    ))

    # Add correlation values on the heatmap
    fig.update_traces(
        text=corr_matrix.round(2).astype(str).values,
        texttemplate="%{text}",
        textfont=dict(size=12),
        hovertemplate='x - %{x}<br>y - %{y}<br>Correlation - %{z:.2f}<extra></extra>'
    )

    # Update layout
    fig.update_layout(      
        xaxis_title="Variables",
        yaxis_title="Variables",
        font=dict(color='black'),
        xaxis=dict(tickangle=-45),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig
