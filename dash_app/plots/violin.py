import plotly.express as px
import pandas as pd

def groupby_violin(variavel_interesse: str,
                   df: pd.Series) -> px.violin:
    
    color_sequence = ["#012a4a", "#0a395b", "#13496c", "#1c587d", "#25678e",
                  "#277099", "#1e558a", "#153a7b", '#0c1f6d', "#081165",
                  "#03045e"]   
    
    fig = px.violin(
        df,
        x='NRGInter',
        y=f'{variavel_interesse}',
        box=True,
        color='NRGInter',
        color_discrete_sequence=color_sequence,
        labels={"NRGInter": "Região Intermediária"}
    )

    fig.update_layout(
        xaxis_title="Regiões Intermediárias",
        yaxis_title=f"{variavel_interesse}",
        paper_bgcolor= 'rgba(0,0,0,0)',
        font=dict(color='black')
        
    )
    
    return fig