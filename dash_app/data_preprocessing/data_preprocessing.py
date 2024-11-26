import pandas as pd
import geopandas as gpd
from libpysal import weights
from esda import Moran, Moran_Local, G_Local
import os   
import unidecode
from typing import Tuple, Union
from libpysal.weights import W

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

def acessar_dataframe(ano: str, colunas: list) -> gpd.GeoDataFrame:
    
    caminho = f"Base_final/{ano}/{ano}.shp"
    
    try:
        df = gpd.read_file(caminho)
        if colunas:
            df = df[colunas]
    except Exception as e:
        raise ValueError(f"Erro ao acessar o arquivo {caminho}: {e}")
    
    return df

def spatial_weights(df: pd.DataFrame,
                    spatial_weights: str,
                    variavel_interesse: str,
                    spatial_lag: bool =True) -> Tuple[pd.DataFrame, pd.Series, weights.W]:
    """
    Computes spatial weights matrices and spatially lagged variables for spatial autocorrelation analysis.

    Args:
        df (pd.DataFrame): DataFrame containing the data, including 'NRGIme', 'cod_ibge', and 'Municipio' columns.
        spatial_weights (str): Type of spatial weights to compute. Options are:
            - 'Regiao Imediata': Block weights based on immediate regions.
            - 'Distancia Centroides': Distance-based weights using centroids of municipalities.
            - 'Distancia Centroides (Apenas Região Imediata)': Distance-based weights using centroids,
              but only considering municipalities within the same immediate region.
        variavel_interesse (str): Name of the variable of interest in `df` to compute spatial lag for.
        spatial_lag (bool, optional): If True, computes the spatially lagged variable. If False,
            returns the original variable. Default is True.

    Returns:
        Tuple:
            - autocorr (pd.DataFrame): DataFrame with the spatially lagged variable added.
            - y (pd.Series): The spatially lagged variable or the original variable, depending on `spatial_lag`.
            - w (libpysal.weights.W): The spatial weights matrix.

    Raises:
        ValueError: If `spatial_weights` is not one of the recognized options.
    """
    
    autocorr  = df.copy()
    
    if spatial_weights == 'Regiao Imediata':
        w = weights.block_weights(autocorr['NRGIme'])
        w.transform = 'r' 
        autocorr[f"{variavel_interesse}_lag"] = weights.spatial_lag.lag_spatial(w, autocorr[variavel_interesse])
        y = autocorr[f"{variavel_interesse}_lag"]
        
    elif spatial_weights == 'Distancia Centroides':
        # Load centroids data
        centroides = pd.read_csv(r"Shapefiles_auxiliares/centroides_mun.csv")
        centroides['Municipio'] = centroides['Municipio'].apply(lambda x: unidecode.unidecode(x))
        centroides.rename(columns={'Cod_ibge': 'cod_ibge'}, inplace=True)
        df_temp = autocorr.merge(centroides, on=['cod_ibge', 'Municipio'], how='inner')
        
        coords = df_temp[['coord_centroide_x', 'coord_centroide_y']].values
        w = weights.DistanceBand.from_array(coords, binary=False, alpha=-1, threshold=100000)
        w.transform = 'r' 
        autocorr[f"{variavel_interesse}_lag"] = weights.spatial_lag.lag_spatial(w, df[variavel_interesse])
        y = autocorr[f"{variavel_interesse}_lag"]
    
    elif spatial_weights == 'Distancia Centroides (Apenas Região Imediata)':
        # Load centroids data
        centroides = pd.read_csv(r"Shapefiles_auxiliares/centroides_mun.csv")
        centroides['Municipio'] = centroides['Municipio'].apply(lambda x: unidecode.unidecode(x))
        centroides.rename(columns={'Cod_ibge': 'cod_ibge'}, inplace=True)
        df_temp = autocorr.merge(centroides, on=['cod_ibge', 'Municipio'], how='inner')

        coords = df_temp[['coord_centroide_x', 'coord_centroide_y']].values  
        threshold = 100000
        w = weights.DistanceBand.from_array(coords, threshold=threshold, binary=False, alpha=-1)

        regioes = df_temp['NRGIme'].values 

        for i in range(len(regioes)):
            neighbors_i = w.neighbors[i]
            weights_i = w.weights[i]
            new_neighbors_i = []
            new_weights_i = []
            for idx, j in enumerate(neighbors_i):
                if regioes[i] == regioes[j]:
                    new_neighbors_i.append(j)
                    new_weights_i.append(weights_i[idx])
            w.neighbors[i] = new_neighbors_i
            w.weights[i] = new_weights_i

        w.transform = 'r'
        autocorr[f"{variavel_interesse}_lag"] = weights.spatial_lag.lag_spatial(w, df_temp[variavel_interesse])
        y = autocorr[f"{variavel_interesse}_lag"]

    if spatial_lag == False:
        y = autocorr[f"{variavel_interesse}"]

    return autocorr, y, w
    
def autocorr_stats(y: pd.Series,
                   w: W, 
                   autocorr_df: pd.DataFrame,
                   metric: str) -> Union[Tuple[float, pd.DataFrame], pd.DataFrame]:
    
    if metric == 'Global Morans I':
        
        global_moransI =Moran(y, w)
        return global_moransI, autocorr_df
    
    elif metric == 'Local Morans I':
        
        quadrant_colors = {
        1: 'rgb(23, 28, 66)',    # HH - Alto-Alto
        2: 'rgb(72, 202, 228)',   # LL - Baixo-Baixo
        3: 'rgb(224, 30, 55)',  # LH - Baixo-Alto
        4: 'rgb(120, 14, 40)', # HL - Alto-Baixo
        }
        
        nonsignificant_color = 'lightgray'
        autocorr_df['color'] = autocorr_df.apply(
            lambda row: quadrant_colors.get(row['quadrant'], nonsignificant_color) if row['Significância_lisa'] < 0.05 else nonsignificant_color,
            axis=1
        )

        autocorr_df['quadrant'] = autocorr_df.apply(
            lambda row: 0 if row['color'] == 'lightgray' else row['quadrant'],
            axis=1
        )
        
        lisa = Moran_Local(y, w)
        autocorr_df['LISA'] = lisa.Is
        autocorr_df['Significância_lisa'] = lisa.p_sim
        autocorr_df['quadrant'] = lisa.q

        return autocorr_df
    
    elif metric == 'G_local':
        gi_star = G_Local(y, w, star=True)
        autocorr_df['Gi*'] = gi_star.Zs
        autocorr_df['Significância_Gi*'] = gi_star.p_sim
        
        # Categoriza cada região como Hotspot, Coldspot ou Não Significativo
        def categorize(row):
            if row['Gi*'] > 1.96 and row['Significância_Gi*'] < 0.05:
                return 'Hotspot'
            elif row['Gi*'] < -1.96 and row['Significância_Gi*'] < 0.05:
                return 'Coldspot'
            else:
                return 'Não significativo'
        autocorr_df['category'] = autocorr_df.apply(categorize, axis=1)
        return autocorr_df
    else:
        raise ValueError(f"Métrica '{metric}' não reconhecida. Escolha entre 'Global Morans I', 'Local Morans I' ou 'G_local'.")
    