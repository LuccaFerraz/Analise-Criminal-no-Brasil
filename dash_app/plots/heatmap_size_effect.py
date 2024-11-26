import plotly.graph_objects as go

def heatmap_size_effect(effect_size_matrix):
    
    # Criar o heatmap
    fig = go.Figure(data=go.Heatmap(
        z=effect_size_matrix.values,              
        x=effect_size_matrix.columns,             
        y=effect_size_matrix.index,               
        colorscale='Blues',               
        colorbar=dict(title="Tamanho de Efeito")  
    ))

    # Adicionar valores diretamente nas células
    fig.update_traces(
        text=effect_size_matrix.round(2).astype(str).values,  
        texttemplate="%{text}",                        
        textfont=dict(size=12)                         
    )

    # Configurar o layout
    fig.update_layout(
        title="Matriz de Tamanho de Efeito entre Regiões",
        xaxis_title="Região 2",
        yaxis_title="Região 1",
        font=dict(color='black'),
        xaxis=dict(tickangle=-45), 
        plot_bgcolor="white",
        paper_bgcolor="rgba(0,0,0,0)",
    
    )

    return fig
