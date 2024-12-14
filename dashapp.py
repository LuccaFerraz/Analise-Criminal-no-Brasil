# Importar as bases já codificadas para os plots
import dash_bootstrap_components as dbc
from dash import html, dcc, Dash, Output, Input, ctx, State
import pandas as pd
from dash_app.shapefiles.leitura_shapefiles import carregar_shapefiles, shp_to_json
from dash_app.data_preprocessing.data_preprocessing import acessar_dataframe, spatial_weights, autocorr_stats, agg_crime
from dash_app.plots.map_distribution import mapa_dist
from dash_app.plots.histogram import histogram
from dash_app.plots.violin import groupby_violin
from dash_app.auxiliary_functions.auxx import kruskal_stats, post_hoc_dull_stats, effect_size_matrix
from dash_app.plots.heatmap_size_effect import heatmap_size_effect
from dash_app.plots.morans import morans_i
from dash_app.plots.getis_ord import G_local
from dash_app.plots.time_series import time_series
from dash_app.plots.correlation_map import correlation_map
from dash_app.plots.dim_reduction import dim_reduction

app = Dash(
    external_stylesheets=[dbc.themes.LUX],
    suppress_callback_exceptions=True    
)

server = app.server

# Acessar o dataframe para criar os dropdowns da secção 4 da página 1
divisao_regional = acessar_dataframe('2014', colunas=['Municipio', 'NRGInter', 'NRGIme'])

# Pré-processamento para a página
regioes_imediatas = carregar_shapefiles(
    diretorio_base='dash_app/shapefiles/Shapefiles_auxiliares',
    shapefile_name="Regiao Geografica Imediata"
)
# Converter o shapefile para GeoJSON
regioes_imediatas_shp, geojson_regioes_imediatas = shp_to_json(regioes_imediatas)

crime_map = {
    'Vehicle Theft': 'FV',
    'Other Theft': 'FO',
    'Involuntary Manslaughter (Other)': 'HC',
    'Involuntary Manslaughter (Traffic)': 'HCA',
    'Armed Robbery': 'Lat',
    'Unintentional Bodily Injury (Other)': 'LCC',
    'Unintentional Bodily Injury (Traffic)': 'LCCA',
    'Intentional Bodily Injury': 'LCD',
    'Homicide Victims': 'VH',
    'Homicide Attempt': 'TH',
    'Total Rape': 'TE',
    'Total Robbery': 'TR',
}

# Page 1
section_1_layout = dbc.Container([
    
    html.H2("Data-Driven Analysis of Crime Patterns in São Paulo", style={'fontWeight': 'bold', 'marginBottom': '20px'}),
    html.P("This web project aims to provide a practical and accessible exploratory analysis "
            "to uncover crime patterns in the state of São Paulo. By visualizing various variables "
            "aggregated at the municipal level, the platform facilitates comparisons of regional "
            "distributions, highlights the practical significance of these differences, and explores spatial autocorrelation."),
    html.Br(),
])

section_2_layout = dbc.Container([
        dbc.Row([
            
            dbc.Col(
                html.Img(
                    src = "assets/image.png",
                    style={'width': '100%',       
                           'height': 'auto',     
                           'border-radius': '10px'}
                ),
                width=8
            ),
            
            dbc.Col(
                html.Div([
                    html.H4("The Datasources"),
                    html.P("Drawing from a combination of publicly available datasets, the analysis "
                           "integrates over 50 variables across four distinct years (2014, 2016, 2018, and 2020)." 
                           "These datasets, sourced from entities such as SEADE and the São Paulo State Department "
                           "of Public Safety (SSP), offer a comprehensive view of the factors shaping criminal activity, as illustrated alongside."
                           )
                    
                ]),
                width=4
            )
            
        ], align='center', justify='center', style={'margin-top': '20px'}),
        html.Br(),
        html.Br(),
])
 
section_3_layout = dbc.Container([
    # Linha para os botões de ano e o dropdown lado a lado
    
    dbc.Row([
            dbc.Col(
                [
                    html.H4("Adapted Crime Index for SSP Data"),
                    html.P(
                        "Given the discrepancies between the crime categories in our dataset and those outlined in the original article—such as differing classifications and granularities of crimes like homicide—we have made thoughtful adjustments to the weighting system. For instance, while homicide is unified in the article's dataset, our data differentiates between specific types of homicide, as demonstrated in the table above. These differences necessitate a tailored approach to ensure accuracy and relevance."
                    ),
                    html.P(
                        "To address these variations, we expanded the weighting scale from 1–4 to 1–6. Below, we detail the reasoning behind each weight adjustment:"
                    ),
                    html.Ul(
                        [
                            html.Li(
                                html.Strong("Weights Retained:"),
                                style={"marginBottom": "5px"},
                            ),
                            html.Ul(
                                [
                                    html.Li("Vehicle Theft (Weight 1): No significant deviation from the original classification."),
                                    html.Li("Other Thefts (Weight 1): Consistent societal impact across datasets."),
                                    html.Li("Total Robberies (Weight 2): Maintained due to similar considerations."),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                            html.Li(
                                html.Strong("Weights Adjusted Due to Crime Specificity:"),
                                style={"marginBottom": "5px"},
                            ),
                            html.Ul(
                                [
                                    html.Li(
                                        "Involuntary Manslaughter in Traffic (Weight 4.5): Increased slightly to account for aggravating factors such as concurrent crimes like driving under the influence."
                                    ),
                                    html.Li(
                                        "Other Involuntary Manslaughter (Weight 4): Lowered by 0.5 as no aggravating factors are explicitly involved."
                                    ),
                                    html.Li(
                                        "Intentional Homicide (Weight 5): Reflects the severe societal and legal consequences of the crime."
                                    ),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                            html.Li(
                                html.Strong("New Weights for Additional Crimes:"),
                                style={"marginBottom": "5px"},
                            ),
                            html.Ul(
                                [
                                    html.Li("Robbery-Murder (Weight 6): Highest weight due to its dual severity."),
                                    html.Li("Unintentional Bodily Harm (Other) (Weight 2.5): Lower societal impact than intentional crimes."),
                                    html.Li("Unintentional Bodily Harm in Traffic (Weight 3):"),
                                    html.Li("Intentional Bodily Harm (Weight 3.5):"),
                                    html.Li("Total Rape (Weight 5):"),
                                    html.Li("Attempted Homicide (Weight 4.5): Reduced to reflect the lack of consummation of the act."),
                                ],
                                style={"marginLeft": "20px"},
                            ),
                        ]
                    ),
                    html.P(
                        "Additionally, to make the index more robust and fair across municipalities, we’ve adopted a per capita crime rate instead of raw crime occurrences. This adjustment ensures the index reflects the relative safety of municipalities, unaffected by population size disparities. These refinements aim to deliver a comprehensive and equitable measure of criminal activity."
                    ),
                ],
                width=12,
            )
        ],
        style={"marginBottom": "20px", "marginLeft": "60px"},
        
    ),

        html.H4("Population Data", style={'fontWeight': 'bold', 'marginTop': '30px', 'marginLeft': '60px'}),
    html.P([
    "As population data is not collected annually, we used population estimates provided by the ",
    html.A(
        "Brazilian Institute of Geography and Statistics (IBGE)",
        href="https://sidra.ibge.gov.br/tabela/6579",
        target="_blank",
        style={"color": "blue", "textDecoration": "underline"}
    ),
    ". For 2022, we used the ",
    html.A(
        "Preliminary Census Data",
        href="https://www.ibge.gov.br/estatisticas/sociais/populacao/22827-censo-demografico-2022.html?edicao=35938&t=resultados",
        target="_blank",
        style={"color": "blue", "textDecoration": "underline"}
    ),
    " released by the IBGE."
    
    ], style={"marginLeft": "60px"}),
    html.Br(),
    
    dbc.Row([
        # Botões de seleção de ano
        dbc.Col([
            html.Div([
                html.H4("Select Year of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dbc.ButtonGroup(
                    [
                        dbc.Button("2014", id="btn-2014", className="year-button"),
                        dbc.Button("2016", id="btn-2016", className="year-button"),
                        dbc.Button("2018", id="btn-2018", className="year-button"),
                        dbc.Button("2020", id="btn-2020", className="year-button"),
                    ],
                    size="lg",
                )
            ], style={'marginLeft': '50px'})  # Adiciona margem à esquerda
        ], width=4),  # Largura dos botões

        # Dropdown de variável de interesse
        dbc.Col([
            html.Div([
                html.H4("Select Variable of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='home-variavel_interesse-dropdown',
                    options=[
                        {'label': "IPDM", 'value': "IPDM"},
                        {'label': "Wealth Indicator", 'value': "IndRiq"},
                        {'label': "Longevity Indicator", 'value': "IndLong"},
                        {'label': "Education Indicator", 'value': "IndEsc"},
                        {'label': "Crime Index", 'value': "IC"}
                    ],
                    value='IC',
                    style={'width': '100%'}
                )
            ])  # Adiciona margem à esquerda
        ], width=3),
        
        dbc.Col([
            
        ], width=5)
    ], align="left", style={'marginBottom': '30px'}),

    # Gráficos lado a lado
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='histograma')
        ], width=5),
        dbc.Col([
            dcc.Graph(id='mapa-distribuicao')
        ], width=6),
    ]),
    html.Br()
], fluid=True)

section_methodology_layout = dbc.Container([
    # Título da seção
    html.H2("Methodology of the Crime Index", style={'fontWeight': 'bold', 'marginBottom': '20px', 'marginLeft': '60px'}),
    
    html.P([
    "This section details the methodology used to calculate the Crime Index, based on adaptations "
    "from the study ",
    html.A(
        "Definition of Strategies for Crime Prevention and Combat Using Fuzzy Clustering and Formal Concept Analysis",
        href="https://www.researchgate.net/publication/320024255_Definition_of_Strategies_for_Crime_Prevention_and_Combat_Using_Fuzzy_Clustering_and_Formal_Concept_Analysis",
        target="_blank",
        style={"color": "blue", "textDecoration": "underline"}  # Estilo opcional
    ),
    ". Adjustments were made to accommodate additional crime categories and local data variations."
    ], style={'marginLeft': '60px'}),

    # Original weights and formula
    html.H4("Original Weight Table and Formula", style={'fontWeight': 'bold', 'marginTop': '20px', 'marginLeft': '60px'}),
    dbc.Table.from_dataframe(
        pd.DataFrame({
            'Crime': [
                "Theft (victim not present)", "Robbery", "Homicide", "Drug Traffic"
            ],
            'Factor': [1, 2, 3, 4],
            'Weight Formula': [
                "Weight = Factor × Number of occurrences",
                "Weight = Factor × Number of occurrences",
                "Weight = Factor × Number of occurrences",
                "Weight = Factor × Number of occurrences"
            ]
        }),
        bordered=True,
        hover=True,
        responsive=True,
        style={
            'marginBottom': '20px',
            'width': '60%',  # Tamanho reduzido da tabela
            'marginLeft': '60px',  # Alinhado à esquerda
        }
    ),
    
    dbc.Row(
        [
            dbc.Col(
                [
                    html.H4("Original Crime Index Formula"),
                    html.P("The formula for the original crime index calculation is presented below:"),
                    html.Div(
                        children=[
                            html.Strong(
                                "Danger Level = (Theft.W + Robbery.W + Homicide.W + Drug.Traffic.W) / Total.Weight"
                            )
                        ],
                        style={"fontSize": "16px", "marginBottom": "10px"},
                    ),
                    html.P(
                        [
                            "As detailed in the article, the weights assigned to each crime type were determined by experts in the field. ",
                            html.Em(
                                '"The weighting of each type of crime was defined using common sense and the opinion of experts."'
                            ),
                            " This approach ensures that the index reflects a balanced perspective, emphasizing the relative societal impact of each crime category.",
                        ]
                    ),
                ],
                width=12,
            )
        ],
        style={"marginBottom": "20px", 'marginLeft': '60px'},
    )

], fluid=True)

section_4_layout = dbc.Container([
    dbc.Row([
        # Dropdown Região Intermediária
        dbc.Col([
            html.H4("Região Intermediária", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dropdown-regiao-intermediaria',
                options=[{'label': 'Todos', 'value': 'Todos'}] +
                        [{'label': reg, 'value': reg} for reg in divisao_regional['NRGInter'].unique()],
                value='Todos'
            )
        ], width=3),
        
        dbc.Col([
            html.H4("Região Imediata", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dropdown-regiao-imediata',
                options=[],
                value='Todos'
            )
        ], width=3),

         dbc.Col([
            html.H4("Município", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dropdown-municipio',
                options=[],
                value='Todos'
            )
        ], width=3),
         
        dbc.Col([
            html.H4("Crime Type", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dropdown-tipo-crime',
                options=[{'label': nome, 'value': sigla} for nome, sigla in crime_map.items()],
                value='FV'  
            )
        ], width=3),
    ]),
    
    dbc.Row([
        dcc.Graph(id='plot_time_series'),
    ]),
    html.Br(),
])

@app.callback(
    Output('dropdown-regiao-imediata', 'options'),
    Input('dropdown-regiao-intermediaria', 'value')
)

def update_regiao_imediata_options(selected_intermediaria):
    if selected_intermediaria == 'Todos':
        return [{'label': 'Todos', 'value': 'Todos'}]
    filtered_imediata = divisao_regional[divisao_regional['NRGInter'] == selected_intermediaria]['NRGIme'].unique()
    return [{'label': 'Todos', 'value': 'Todos'}] + [{'label': reg, 'value': reg} for reg in filtered_imediata]

@app.callback(
    Output('dropdown-municipio', 'options'),
    [Input('dropdown-regiao-intermediaria', 'value'),
     Input('dropdown-regiao-imediata', 'value')]
)

def update_municipio_options(selected_intermediaria, selected_imediata):
    if selected_intermediaria == 'Todos':
        return [{'label': 'Todos', 'value': 'Todos'}]
    if selected_imediata == 'Todos':
        filtered_municipios = divisao_regional[divisao_regional['NRGInter'] == selected_intermediaria]['Municipio'].unique()
    else:
        filtered_municipios = divisao_regional[
            (divisao_regional['NRGInter'] == selected_intermediaria) & (divisao_regional['NRGIme'] == selected_imediata)
        ]['Municipio'].unique()
    return [{'label': 'Todos', 'value': 'Todos'}] + [{'label': mun, 'value': mun} for mun in filtered_municipios]

@app.callback(
    Output('plot_time_series', 'figure'),
    [Input('dropdown-regiao-intermediaria', 'value'),
     Input('dropdown-regiao-imediata', 'value'),
     Input('dropdown-municipio', 'value'),
     Input('dropdown-tipo-crime', 'value')]
)
def update_lineplot(selected_intermediaria, selected_imediata, selected_municipio, crime_interesse):
    
    anos = ['2014', '2016', '2018', '2020']
    resultados = []
    
    for ano in anos:
        variavel_interesse = f"{crime_interesse}{ano}"
        colunas = ['cod_ibge', 'Municipio', 'NRGInter', 'NRGIme', variavel_interesse]
        df_ano = acessar_dataframe(ano, colunas)

        # Filtrar o dataframe com base nas seleções
        df_filtered = df_ano.copy()

        if selected_intermediaria != 'Todos':
            df_filtered = df_filtered[df_filtered['NRGInter'] == selected_intermediaria]
        if selected_imediata != 'Todos':
            df_filtered = df_filtered[df_filtered['NRGIme'] == selected_imediata]
        if selected_municipio != 'Todos':
            df_filtered = df_filtered[df_filtered['Municipio'] == selected_municipio]

        valor_total = df_filtered[variavel_interesse].sum()
        resultados.append(valor_total)

    plot_time_series = time_series(anos, resultados)
    
    return plot_time_series

home_layout = html.Div([

    section_1_layout,
    section_methodology_layout,
    section_4_layout,
    section_3_layout,
    section_2_layout,
    
])

@app.callback(
    [Output('mapa-distribuicao', 'figure'),
     Output('histograma', 'figure')],
    [Input('btn-2014', 'n_clicks'),
     Input('btn-2016', 'n_clicks'),
     Input('btn-2018', 'n_clicks'),
     Input('btn-2020', 'n_clicks'),
     Input('home-variavel_interesse-dropdown', 'value')]
)

def update_graphs(btn_2014, btn_2016, btn_2018, btn_2020, variavel_interesse):
    
    selected_year = '2014'

    # Identificar qual botão foi clicado
    ctx_trigger = ctx.triggered
    if ctx_trigger:
        button_id = ctx_trigger[0]['prop_id'].split('.')[0]
        if button_id.startswith('btn-'):
            selected_year = button_id.split('-')[1]
            
    try:
        fig_map, fig_hist = update_home_plots(selected_year, variavel_interesse)
        return fig_map, fig_hist
    except Exception as e:
        print(f"Error updating graphs: {e}")
        return {}, {} 
    
def update_home_plots(selected_year, variavel_interesse):
    
    """
    Args:
        selected_year (_type_): 2014, 2016, 2018, 2022
        variavel_interesse (_type_): IPDM, IndRiq, IndLong, IndEsc, IC
    """
    
    if variavel_interesse == 'IC':
        variavel_interesse = f'IC{selected_year}'
        
    colunas = ['cod_ibge', 'Municipio', 'NRGInter', 'NRGIme', 'geometry', f'{variavel_interesse}']
        
    df_ano = acessar_dataframe(selected_year, colunas)
    df_ano, geojson = shp_to_json(df_ano)
    
    fig_hist = histogram(variavel_interesse, df_ano)
    
    df_ano = df_ano[df_ano['Municipio'] != 'Ilha Comprida']
    
    fig_map = mapa_dist(geojson, df_ano.index, df_ano['Municipio'],
                        df_ano[variavel_interesse], variavel_interesse, geojson_regioes_imediatas,
                        regioes_imediatas_shp.index, regioes_imediatas_shp['const'])
    
    fig_map.update_layout(
        title=f"Geographic Distribution of {variavel_interesse} - Year {selected_year}",
        title_font=dict(size=14),
        title_x = 0.5,
        height=400,
        width=700,# Altura do gráfico
        margin=dict(l=10, r=10, t=30, b=10)  # Margens internas
    )
    
    # Configurar tamanho no histograma
    fig_hist = histogram(variavel_interesse, df_ano)
    fig_hist.update_layout(
        title=f"Histogram of {variavel_interesse} - Year {selected_year}",
        title_font=dict(size=14),
        title_x=0.5,  
        height=400,  # Altura do gráfico
        margin=dict(l=10, r=10, t=30, b=10)  # Margens internas
    )
    
    return fig_map, fig_hist


# Page 2

section_1_page2_layout = dbc.Container([
        # Título e Introdução
    html.H2("Distribution Comparison", style={'fontWeight': 'bold', 'marginBottom': '20px'}),
    html.P(
        "Intermediate regions represent a classification used to group municipalities based on their "
        "geographical, economic, and social characteristics. Comparing distributions across these regions "
        "is essential to identify significant patterns and disparities in the data. "
        "In this section, the Kruskal-Wallis H statistic and its corresponding p-value are applied to test "
        "for differences between the distributions of these regions. Additionally, the Post-Hoc Dunn test is "
        "used to identify pairwise differences. Finally, an effect size matrix is calculated to quantify the "
        "practical significance of these differences."
    ),
    html.Br()
    
])
section_2_page2_layout = html.Div([
    
    dbc.Row([
        # Botões de seleção de ano
        dbc.Col([
            html.Div([
                html.H4("Select Year of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dbc.ButtonGroup(
                    [
                        dbc.Button("2014", id="btn-2014", className="year-button"),
                        dbc.Button("2016", id="btn-2016", className="year-button"),
                        dbc.Button("2018", id="btn-2018", className="year-button"),
                        dbc.Button("2020", id="btn-2020", className="year-button"),
                    ],
                    size="lg",
                )
            ], style={'marginLeft': '50px'})  # Adiciona margem à esquerda
        ], width=4),  # Largura dos botões

        # Dropdown de variável de interesse
        dbc.Col([
            html.Div([
                html.H4("Select Variable of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='comparison-variavel-dropdown',
                    
                    options=[
                        {'label': "IPDM", 'value': "IPDM"},
                        {'label': "Wealth Indicator", 'value': "IndRiq"},
                        {'label': "Longevity Indicator", 'value': "IndLong"},
                        {'label': "Education Indicator", 'value': "IndEsc"},
                        {'label': "Crime Index", 'value': "IC"}
                    ],
                    value='IC',
                    style={'width': '100%'}
                )
            ])  # Adiciona margem à esquerda
        ], width=3),
        
        dbc.Col([
            
        ], width=5)
    ], align="left", style={'marginBottom': '30px'}),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='violin-plot')
        ], width=8),
        
        dbc.Col([
            html.H5(id='subtitle', style={'fontWeight': 'bold', 'marginTop': '30px'}),
            html.Ul(id='stats', style={'fontSize': '16px', 'paddingLeft': '20px'})
            
        ])
        
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='heatmap-plot')
        ])
    ])
    
])

page_2_layout = html.Div([
    
    section_1_page2_layout,
    section_2_page2_layout,
    
])

@app.callback(
    [Output('violin-plot', 'figure'),
     Output('heatmap-plot', 'figure'),
     Output('subtitle', 'children'),
     Output('stats', 'children')],
    [Input('btn-2014', 'n_clicks'),
     Input('btn-2016', 'n_clicks'),
     Input('btn-2018', 'n_clicks'),
     Input('btn-2020', 'n_clicks'),
     Input('comparison-variavel-dropdown', 'value')]
)

def update_distribution_graphs(btn_2014, btn_2016, btn_2018, btn_2020, variavel_interesse):

    selected_year = '2014'

    # Identificar qual botão foi clicado
    ctx_trigger = ctx.triggered
    if ctx_trigger:
        button_id = ctx_trigger[0]['prop_id'].split('.')[0]
        if button_id.startswith('btn-'):
            selected_year = button_id.split('-')[1]
            
    try:
        if variavel_interesse == 'IC':
            variavel_interesse = f'IC{selected_year}'
                
        colunas = ['cod_ibge', 'Municipio', 'NRGInter','NRGIme', 'geometry', f'{variavel_interesse}']
        df_ano = acessar_dataframe(selected_year, colunas)

        # Gráfico Violin
        fig_violin = groupby_violin(f'{variavel_interesse}', df_ano)

        # Estatísticas 
        stat, p, epsilon_squared = kruskal_stats('NRGInter', f'{variavel_interesse}', df_ano)
        
        subtitle = f"Variavel of Interest: {variavel_interesse} - Year: {selected_year}"
        
        stats  = [
        html.Li(f"H Statistic: {stat:.2f}"),
        html.Li(f"p-value: {p:.4f}"),
        html.Li(f"Post Hoc Dunn Test epsilon squared value: {epsilon_squared:.2f}")
        ]
    
        # Matriz de tamanho de efeito e heatmap
        effect_size_matrix_ = effect_size_matrix('NRGInter', f'{variavel_interesse}', df_ano)
        fig_heatmap = heatmap_size_effect(effect_size_matrix_)
        
        fig_violin.update_layout(
        title=f"Distribution of {variavel_interesse} - Year {selected_year}",
        title_font=dict(size=14),
        title_x = 0.5,
        )
        
        fig_heatmap.update_layout(
            title=f"Effect Size matrix of  {variavel_interesse} - Year {selected_year}",
            title_font=dict(size=14),
            title_x = 0.5,
        )

        return fig_violin, fig_heatmap, subtitle, stats
    
    except Exception as e:
        print(f"Error updating graphs: {e}")
        return {}, {} 

# Page 3

# Layout da seção de introdução para a página 3
section_1_page3_layout = dbc.Container([
    
    # Título da página
    html.H2("Autocorrelation Analysis", style={'fontWeight': 'bold', 'marginBottom': '20px'}),
    
    # Introdução
    html.P(
        "Spatial autocorrelation analysis is a powerful statistical tool used to assess the degree to which a "
        "variable is spatially clustered, dispersed, or randomly distributed across a geographical area. "
        "In this analysis, both global and local measures were applied to gain a comprehensive understanding of spatial patterns.",
        style={'textAlign': 'justify', 'marginBottom': '15px'}
    ),
    html.P(
        "The Global Moran's I provides an overall measure of spatial autocorrelation, identifying whether the variable "
        "of interest exhibits clustering or randomness at a global scale. To complement this, the Local Indicators of Spatial Association (LISA) "
        "were used to detect specific regions with significant spatial clusters or outliers.",
        style={'textAlign': 'justify', 'marginBottom': '15px'}
    ),
    html.P(
        "The analysis includes two key local measures: Local Moran's I, which identifies high-high and low-low clusters, "
        "and Getis-Ord Gi*, which highlights hot spots (regions of significantly high values) and cold spots "
        "(regions of significantly low values). These methods together reveal critical spatial patterns and disparities "
        "in the distribution of the analyzed variable.",
        style={'textAlign': 'justify'}
    ),
    html.Br()
])
section_2_page3_layout = dbc.Container([
    
    dbc.Row([
        # Botões de seleção de ano
        dbc.Col([
            html.Div([
                html.H4("Select Year of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dbc.ButtonGroup(
                    [
                        dbc.Button("2014", id="btn-2014", className="year-button"),
                        dbc.Button("2016", id="btn-2016", className="year-button"),
                        dbc.Button("2018", id="btn-2018", className="year-button"),
                        dbc.Button("2020", id="btn-2020", className="year-button"),
                    ],
                    size="lg",
                )
            ], style={'marginLeft': '50px'})  # Adiciona margem à esquerda
        ], width=4),  # Largura dos botões

        # Dropdown de variável de interesse
        dbc.Col([
            html.Div([
                html.H4("Select Variable of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dcc.Dropdown(
                    id='comparison-variavel-dropdown',
                    
                    options=[
                        {'label': "IPDM", 'value': "IPDM"},
                        {'label': "Wealth Indicator", 'value': "IndRiq"},
                        {'label': "Longevity Indicator", 'value': "IndLong"},
                        {'label': "Education Indicator", 'value': "IndEsc"},
                        {'label': "Crime Index", 'value': "IC"}
                    ] + [{'label': name, 'value': code} for name, code in crime_map.items()],
                    value='IC',
                    style={'width': '100%'}
                )
            ])  # Adiciona margem à esquerda
        ], width=3),
        
        # Colocar aqui o dropdown Spatial Weights
        dbc.Col([
            
        ], width=5)
    ], align="left", style={'marginBottom': '30px'}),

    dbc.Row([
        dcc.Graph(id='morans')
    ]),
    
    dbc.Row([
        dcc.Graph(id='gi_star')
    ])
    
])

page_3_layout = html.Div([
    
    section_1_page3_layout,
    section_2_page3_layout
])

@app.callback(
    [Output('morans', 'figure'),
     Output('gi_star', 'figure')],
    [Input('btn-2014', 'n_clicks'),
     Input('btn-2016', 'n_clicks'),
     Input('btn-2018', 'n_clicks'),
     Input('btn-2020', 'n_clicks'),
     Input('comparison-variavel-dropdown', 'value')]
)

def update_autocorr(btn_2014, btn_2016, btn_2018, btn_2020, variavel_interesse):

    selected_year = '2014'

    # Identificar qual botão foi clicado
    ctx_trigger = ctx.triggered
    if ctx_trigger:
        button_id = ctx_trigger[0]['prop_id'].split('.')[0]
        if button_id.startswith('btn-'):
            selected_year = button_id.split('-')[1]
            
    try:
        
        if variavel_interesse in crime_map.values():  
            colunas = ['cod_ibge', 'Municipio', 'populacao','NRGIme', 'geometry', f'{variavel_interesse}{selected_year}']
        
        elif variavel_interesse == 'IC':
            colunas = ['cod_ibge', 'Municipio', 'populacao', 'NRGIme', 'geometry', f'{variavel_interesse}{selected_year}']
            variavel_interesse = f'{variavel_interesse}{selected_year}'

        else:
            colunas = ['cod_ibge', 'Municipio', 'populacao', 'NRGIme', 'geometry', f'{variavel_interesse}']
            
        df_ano = acessar_dataframe(selected_year, colunas)
        regioes_imediatas = carregar_shapefiles(diretorio_base='dash_app\shapefiles\Shapefiles_auxiliares',
                                        shapefile_name="Regiao Geografica Imediata")
        print(regioes_imediatas)
        
        df_ano, geojson = shp_to_json(df_ano)
        
        regioes_imediatas_shp, geojson_regioes_imediatas = shp_to_json(regioes_imediatas)

        if variavel_interesse in crime_map.values():
            df_ano[f"{variavel_interesse}{selected_year} per capta"] = df_ano[f"{variavel_interesse}{selected_year}"] / df_ano['populacao']
            variavel_interesse = f"{variavel_interesse}{selected_year} per capta"
        
        autocorr, y, w = spatial_weights(df_ano, spatial_weights='Distancia Centroides (Apenas Região Imediata)',
                                 variavel_interesse=f"{variavel_interesse}", spatial_lag=False)
        
        global_morans, autocorr = autocorr_stats(y, w, autocorr, metric='Global Morans I')
        
        autocorr = autocorr_stats(y, w, autocorr, metric='Local Morans I')
        autocorr = autocorr_stats(y, w, autocorr, metric='G_local')
        
        morans = morans_i(autocorr, global_morans, geojson,
        geojson_regioes_imediatas, regioes_imediatas_shp.index, regioes_imediatas_shp['const'],
        f'{variavel_interesse}', f"{variavel_interesse}_lag")
        
        morans.update_layout(
            title={
                'text': f"Global and Local Moran's I for {variavel_interesse} - Year {selected_year}",
                'x': 0.5,
                'xanchor': 'center',
            },
            title_font=dict(size=14)
        )
        
        gi = G_local(autocorr['Municipio'], autocorr['Gi*'], geojson, autocorr.index)
        
        gi.update_layout(
            title={
                'text': f"Gi* Statistics (Getis-Ord) for {variavel_interesse} - {selected_year} ",
                'x': 0.5,
                'xanchor': 'center',
            },
            title_font=dict(size=14)
        )
        
        return morans, gi
    
    except Exception as e:
        print(f"Error updating graphs: {e}")
        return {}, {} 
    

# Exploratory Data Analysis Page
# Define your variable groups
ipdm_columns = ['IPDM', 'CAER', 'CAEC',
                'RTF', 'IndRiq', 'TMI', 'TMP', 'TM1539', 'TM6069', 'IndLong', 'TAE03',
                'Prof5ano', 'Prof9ano', 'TDISM', 'IndEsc']

pop_columns = ['Area_Km2', 'populacao', 'homens', 'mulheres', 'razao_sexo',
               'id_media', 'dens_demog']

pib_columns = ['Indústria', 'AdmPub', 'ServExc',
               'ValAdic', 'ImpLiq', 'PIB', 'Agrop']

ocorrencias_columns = ['FV', 'FO', 'HC',
                       'HCA', 'Lat', 'LCC', 'LCCA', 'LCD', 'VH',
                       'TH', 'TE', 'TR']

variable_sets = {
    'ipdm_columns': ipdm_columns,
    'pop_columns': pop_columns,
    'pib_columns': pib_columns,
    'ocorrencias_columns': ocorrencias_columns
}

variables_dict = {
    'Paulista Index of Human Development': 'IPDM',
    'Annual residential electricity consumption': 'CAER',
    'Annual commercial electricity consumption': 'CAEC',
    'Formal work income': 'RTF',
    'Wealth indicator': 'IndRiq',
    'Infant mortality rate': 'TMI',
    'Perinatal mortality rate': 'TMP',
    'Mortality rate (ages 15 to 39)': 'TM1539',
    'Mortality rate (ages 60 to 69)': 'TM6069',
    'Longevity indicator': 'IndLong',
    'School attendance rate (ages 0 to 3)': 'TAE03',
    'Average proportion of 5th grade students proficient in Portuguese and Mathematics': 'Prof5ano',
    'Average proportion of 9th grade students proficient in Portuguese and Mathematics': 'Prof9ano',
    'Age-grade distortion rates in high school': 'TDISM',
    'Education indicator': 'IndEsc',
    ''
    'Intermediate Geographic Region': 'RGInter',
    'Name of Intermediate Geographic Region': 'NRGInter',
    'Immediate Geographic Region': 'RGIme',
    'Name of Immediate Geographic Region': 'NRGIme',
    'Agriculture contribution to GDP': 'Agrop',
    'Public administration contribution': 'AdmPub',
    'Services contribution (excluding public administration)': 'ServExc',
    'Value added to GDP': 'ValAdic',
    'Net taxes on subsidies': 'ImpLiq',
    'GDP per capita': 'PIBpc',
    'Vehicle theft': 'FV',
    'Other thefts': 'FO',
    'Other unintentional homicides': 'HC',
    'Unintentional homicides in traffic accidents': 'HCA',
    'Robbery with murder (Latrocínio)': 'Lat',
    'Other unintentional bodily harm': 'LCC',
    'Unintentional bodily harm in traffic accidents': 'LCCA',
    'Intentional bodily harm': 'LCD',
    'Homicide victims': 'VH',
    'Attempted homicide': 'TH',
    'Total rape cases': 'TE',
    'Total robbery cases': 'TR',
    'Crime Index': 'IC',
    'Final Classification': 'CL',
}

variables_list = list(variables_dict.items())
midpoint = len(variables_list) // 2
variables_col1 = variables_list[:midpoint]
variables_col2 = variables_list[midpoint:]

def generate_variable_cards(var_list):
    """
    Gera uma lista de cartões com bullet points das variáveis.
    """
    cards = []
    for desc, var in var_list:
        card = dbc.ListGroupItem([
            html.Span(f"{var}: ", style={"fontWeight": "bold"}),
            html.Span(desc)
        ])
        cards.append(card)
    return cards

section_1_extra_page = dbc.Container([
    
    html.H2("Exploratory Data Analysis", style={'fontWeight': 'bold', 'marginBottom': '20px', 'marginLeft': '60px'}),
    
    html.P('Exploratory Data Analysis (EDA) encompasses a systematic examination of the dataset to reveal its structure,'
           'relationships, and essential characteristics. This section begins with Data Profiling, offering a concise overview'
           'of variable definitions, dataset size, and key attributes. Following this, correlation analysis quantifies the relationships'
           'between variables, providing insights into their interdependencies. Finally, dimensionality reduction techniques are employed'
           'to project high-dimensional data into a visually interpretable space, enabling the identification of clusters, patterns, and'
           'trends across multiple attributes in a comprehensible manner.', style={'marginLeft': '60px'}),
    
    dbc.Row([
        dbc.Col([
            html.H3("Data Profiling", style={'marginBottom': '20px'}),
            html.P("Below is a list of the dataset's variables, including their abbreviations and brief descriptions."
                   'The dataframe contains 640 instances, as 5 municipalities lacked certain records. Additionally,' 
                   'it includes information on municipal geometry and immediate regions for spatial analysis.'),
        ], width=10, style={'marginLeft': '60px'})
    ]),
    dbc.Row([
        dbc.Col([
            dbc.ListGroup(
                generate_variable_cards(variables_col1),
                style={'maxHeight': '200px', 'overflowY': 'scroll', 'marginLeft': '60px'}  # Altura ajustável
            )
        ], width=6),
        dbc.Col([
            dbc.ListGroup(
                generate_variable_cards(variables_col2),
                style={'maxHeight': '200px', 'overflowY': 'scroll', 'marginLeft': '60px'}  # Altura ajustável
            )
        ], width=6),
    ]),
    
    html.Br(),
    
    
], fluid=True)

section_2_extra_page = dbc.Container([
    
    dbc.Row([
        dbc.Col([
            html.H3("Data Correlation", style={'marginBottom': '20px'}),
        ])
    ]),
    html.Br(),
    
    dbc.Row([
        
            dbc.Col([
            html.Div([
                html.H4("Select Year of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dbc.ButtonGroup(
                    [
                        dbc.Button("2014", id="btn-2014", className="year-button"),
                        dbc.Button("2016", id="btn-2016", className="year-button"),
                        dbc.Button("2018", id="btn-2018", className="year-button"),
                        dbc.Button("2020", id="btn-2020", className="year-button"),
                    ],
                    size="lg",
                )
            ], style={'marginLeft': '50px'})  # Adiciona margem à esquerda
        ], width=4),
            
        dbc.Col([
            html.H4("Select Dataset:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dataset-dropdown',
                options=[
                    {'label': 'IPDM ', 'value': 'ipdm_columns'},
                    {'label': 'POP', 'value': 'pop_columns'},
                    {'label': 'PIB', 'value': 'pib_columns'},
                    {'label': 'Crime Occurrences', 'value': 'ocorrencias_columns'}
                ],
                value='ipdm_columns'
            ),
        ], width=3),
        
        dbc.Col([
            html.H4("Select Variables:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='variables-dropdown',
                options=[],  # será preenchido dinamicamente
                value=[],
                multi=True
            ),
        ], width=5),
        
    ]),
    
    
    dbc.Row([
        
            dcc.Graph(id='corr-plot')
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Dimensionality reduction", style={'marginBottom': '20px'}),
            
            html.P("To perform dimensionality reduction, the variables were selected based on the correlation"
                   " analysis observed above. It is evident that the vast majority of variables in the 'PIB' and"
                   " 'Crime Occurrences' datasets exhibit extremely high correlations. Therefore, only a small"
                   " subset of variables from each dataset was chosen. Additionally, the correlations between the Wealth, Longevity, and Education"
                   " indicators and their respective composing variables were analyzed to identify which would be most valuable for the projection."
                   " As a result, the attributes selected for dimensionality reduction are: 'IndRiq', 'Agrop', 'IndLong', 'TM1539', 'TM6069', 'TDISM', 'dens_demog', 'id_media', 'PIB', 'PIBpc', 'TR', and 'IC'.")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H4("Select Year of Interest", style={'fontWeight': 'bold', 'fontSize': '16px'}),
                dbc.ButtonGroup(
                    [
                        dbc.Button("2014", id="btn-2014", className="year-button"),
                        dbc.Button("2016", id="btn-2016", className="year-button"),
                        dbc.Button("2018", id="btn-2018", className="year-button"),
                        dbc.Button("2020", id="btn-2020", className="year-button"),
                    ],
                    size="lg",
                )
            ], style={'marginLeft': '50px'})
        ], width=4),
        dbc.Col([
            html.H4("Select Dimensionality Reduction Method:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='reduction-method-dropdown',
                options=[
                    {'label': 'UMAP', 'value': 'UMAP'},
                    {'label': 'T-SNE', 'value': 'TSNE'},
                    {'label': 'PCA', 'value': 'PCA'},
                    {'label': 'MDS', 'value': 'MDS'}
                ],
                value='UMAP',  # Método padrão
                clearable=False
            ),
        ], width=4),
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='dim-reduction')
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='map-reduction')  
        ])
    ])

            
])

extra_page_layout = html.Div([
    
    section_1_extra_page,
    section_2_extra_page
])

@app.callback(
    Output('variables-dropdown', 'options'),
    Output('variables-dropdown', 'value'),
    Input('dataset-dropdown', 'value')
)
def update_variable_dropdown(selected_dataset):
    if selected_dataset:
        options = [{'label': var, 'value': var} for var in variable_sets[selected_dataset]]
        default_values = variable_sets[selected_dataset]  # Todas as variáveis do grupo
        return options, default_values
    return [], []

@app.callback(
    Output('corr-plot', 'figure'),
    [Input('btn-2014', 'n_clicks'),
     Input('btn-2016', 'n_clicks'),
     Input('btn-2018', 'n_clicks'),
     Input('btn-2020', 'n_clicks'),
     Input('dataset-dropdown', 'value'),
     Input('variables-dropdown', 'value')]
)
def update_eda(btn_2014, btn_2016, btn_2018, btn_2020, selected_dataset, selected_vars):
    
    selected_year = '2014'
    ctx_trigger = ctx.triggered
    if ctx_trigger:
        button_id = ctx_trigger[0]['prop_id'].split('.')[0]
        if button_id.startswith('btn-'):
            selected_year = button_id.split('-')[1]
    
    if not selected_vars:
        selected_vars = variable_sets[selected_dataset]
    
    if selected_dataset == 'ocorrencias_columns':
        adjusted_vars = [f"{var}{selected_year}" for var in selected_vars]
    else:
        adjusted_vars = selected_vars
    
    try:

        if len(adjusted_vars) < 2:
            raise ValueError("At least two variables are required to generate a correlation map.")
        
        # Acessar o dataframe e gerar o mapa de correlação
        df_ano = acessar_dataframe(selected_year, adjusted_vars)
        corr = correlation_map(df_ano)
        
        corr.update_layout(
            title=f"Correlation matrix - Year {selected_year}"
        )
        return corr

    except Exception as e:
        print(f"Error updating graphs: {e}")
        # Retornar um gráfico vazio em caso de erro
        return {}
    
@app.callback(
    [Output('dim-reduction', 'figure'),
     Output('map-reduction', 'figure')],
    [Input('btn-2014', 'n_clicks'),
     Input('btn-2016', 'n_clicks'),
     Input('btn-2018', 'n_clicks'),
     Input('btn-2020', 'n_clicks'),
     Input('reduction-method-dropdown', 'value')]
)

def update_dim_reduction(btn_2014, btn_2016, btn_2018, btn_2020, reduction_method):
    
    selected_year = '2014'
    ctx_trigger = ctx.triggered
    if ctx_trigger:
        button_id = ctx_trigger[0]['prop_id'].split('.')[0]
        if button_id.startswith('btn-'):
            selected_year = button_id.split('-')[1]
                
    colunas = ['Municipio', 'NRGInter', 'geometry',
               'IndRiq', 'Agrop', 'IndLong',
               'TM1539', 'TM6069', 'TDISM',
               'dens_demog', 'id_media', 'PIB', 'PIBpc', f'TR{selected_year}', f"IC{selected_year}"]
    
    df = acessar_dataframe(selected_year, colunas)
    
    regioes_intermediarias = carregar_shapefiles(diretorio_base='dash_app\shapefiles\Shapefiles_auxiliares',
                                        shapefile_name="Regiao Geografica Intermediaria")
    
    df, geojson = shp_to_json(df)
    regioes_intermediarias, geojson_NRGInter = shp_to_json(regioes_intermediarias)
    
    fig, map_projection = dim_reduction(reduction_method, df, geojson, regioes_intermediarias, geojson_NRGInter)
    
    return fig, map_projection


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dcc.Link('Home', href='/', className='nav-link')),
            dbc.NavItem(dcc.Link('Exploratory Data Analysis', href='/exploratory-analysis', className='nav-link')),
            dbc.NavItem(dcc.Link('Distribution Comparison', href='/distribution-comparison', className='nav-link')),
            dbc.NavItem(dcc.Link('Autocorrelation Analysis', href='/autocorr-analysis', className='nav-link')),
        ],
        brand='Prática em Ciência de Dados II',
        color='primary',
        dark=True,
        style={'marginBottom': "20px"}
    ),
    html.Div(id='page-content')
    
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/distribution-comparison':
        return page_2_layout
    elif pathname == '/autocorr-analysis':
        return page_3_layout
    elif pathname == '/exploratory-analysis':
        return extra_page_layout
    else:
        return html.H1("404 - Página não encontrada")
    

if __name__ == "__main__":
    app.run_server(debug=False)