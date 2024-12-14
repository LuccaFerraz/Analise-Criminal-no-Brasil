import geopandas as gpd
import os
import json

def carregar_shapefiles(diretorio_base='Shapefiles_auxiliares', shapefile_name=None):
    """_summary_

    Args:
        diretorio_base (str, optional): Diretório dos shapefiles
        shapefile (_type_, optional): Nome do shapefile desejado: {BR_UF_2022}, {LimiteMunicipal},
        {Regiao Geografica Imediata}, {Regiao Geografica Intermediaria}
    """
    shapefiles = {}

    for raiz, dirs, arquivos in os.walk(diretorio_base):
        for arquivo in arquivos:
            if arquivo.endswith('.shp'):
                caminho_shapefile = os.path.join(raiz, arquivo)
                
                nome_shapefile = arquivo.replace('.shp', '')
                shapefiles[nome_shapefile] = gpd.read_file(caminho_shapefile)

    if shapefile_name:
        if shapefile_name in shapefiles:
            return shapefiles[shapefile_name]
        else:
            raise ValueError(f"Shapefile '{shapefile_name}' não encontrado no diretório {diretorio_base}. "
                             f"Shapefiles disponíveis: {list(shapefiles.keys())}")
    else:
        return shapefiles
    
def shp_to_json(shapefile: gpd.GeoDataFrame):
    shapefile['geometry'] = shapefile['geometry'].simplify(0.01)
    shapefile['const'] = 1
    geojson = json.loads(shapefile.to_json())
    
    return shapefile, geojson