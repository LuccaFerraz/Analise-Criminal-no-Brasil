from scipy.stats import mannwhitneyu
from scipy.stats import kruskal
import scikit_posthocs as sp
import pandas as pd
import numpy as np

def kruskal_stats(variavel_groupby, variavel_interesse, df):
    df_analysis = df[[variavel_groupby, variavel_interesse]].copy()

    groups = [grupo[variavel_interesse].values for nome, grupo in df_analysis.groupby(variavel_groupby)]

    stat, p = kruskal(*groups)
    
    n_total = len(df_analysis)
    k = len(groups) 
    epsilon_squared = (stat - k + 1) / (n_total - k)
    
    return stat, p, epsilon_squared
    
def post_hoc_dull_stats(variavel_groupby, variavel_interesse, df):
    df_analysis = df[[variavel_groupby, variavel_interesse]].copy()
    
    post_hoc = sp.posthoc_dunn(df_analysis, val_col=variavel_interesse,
                               group_col=variavel_groupby, p_adjust='fdr_bh')
    
    pares_significantes = (post_hoc < 0.05)
    significancia_dos_estados = pares_significantes.sum(axis=1)
    
    return significancia_dos_estados.sort_values(ascending=False)
    
def calculate_effect_size(group1, group2):
    n1 = len(group1)
    n2 = len(group2)
    u_statistic, _ = mannwhitneyu(group1, group2, alternative='two-sided')
    u_max = n1 * n2
    effect_size = 1 - (2 * u_statistic) / u_max
    return abs(effect_size)

def effect_size_matrix(variavel_groupby, variavel_interesse, df):
    
    df_analysis = df[[variavel_groupby, variavel_interesse]].copy()
    group_dict = {
    name: grupo[variavel_interesse].values
    for name, grupo in df_analysis.groupby(variavel_groupby)
    }

    group_names = list(group_dict.keys())
    n_groups = len(group_names)

    effect_size_array = np.zeros((n_groups, n_groups))

    for i in range(n_groups):
        group1 = group_names[i]
        data1 = group_dict[group1]

        for j in range(i, n_groups):
            group2 = group_names[j]
            data2 = group_dict[group2]
            effect_size = calculate_effect_size(data1, data2)
            effect_size_array[i, j] = effect_size
            effect_size_array[j, i] = effect_size

    # Converter a matriz NumPy em DataFrame
    effect_size_matrix = pd.DataFrame(
        effect_size_array,
        index=group_names,
        columns=group_names
    )
    
    return effect_size_matrix