import plotly.express as px


def histogram(variavel_interesse, df):
    
    fig = px.histogram(df, x=variavel_interesse, marginal='rug',
                   color_discrete_sequence=['rgb(11, 102, 189)'], opacity=0.7)
    fig.update_layout(
        paper_bgcolor = 'rgba(0, 0, 0, 0)',
        font=dict(color='black'))
    fig.update_yaxes(showticklabels=True)
    return fig
