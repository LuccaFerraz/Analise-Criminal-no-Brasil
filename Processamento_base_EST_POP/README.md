# Estimativa Populacional

Para além de dados criminais, necessitou-se de informações demográficas dos municípios do Estado de São Paulo para contextualizar e encontrar motivações para as ocorrências. Por isso, agregou-se a base de estimativa Populacional do ***SEADE***. A partir de interpolações dos censos de 2000, 2010 e 2022, considerando-se o crescimento vegetativo e migratório, obteve-se os seguintes dados para os 645 municípios:

* Estimativa Populacional
* Número de Homens
* Número de Mulheres
* Razão do Sexo
* Idade Média
* Densidade Demográfica (Número de habitantes residentes em relação à área em Km^2)

Em contrapontos com as outras bases, nessa não foi necessário realizar grandes alterações, apenas padronizações de variáveis para serem agregadas às outras e mudanças em seus tipos.

Um exemplo da base:

| Ano | cod_ibge | Municipio  | populacao | homens  | mulheres | razao_sexo | id_media | dens_demog |
|-----|----------|------------|-----------|---------|----------|------------|----------|------------|
| 2000| 3500105  | Adamantina | 33484.0   | 16318.0 | 17166.0  | 105,2      | 33,7     | 81,3       |
| 2001| 3500105  | Adamantina | 33577.0   | 16360.0 | 17217.0  | 105,2      | 34,1     | 81,5       |
| 2002| 3500105  | Adamantina | 33636.0   | 16387.0 | 17249.0  | 105,3      | 34,5     | 81,6       |
| 2003| 3500105  | Adamantina | 33677.0   | 16400.0 | 17277.0  | 105,3      | 34,9     | 81,7       |
| 2004| 3500105  | Adamantina | 33715.0   | 16411.0 | 17304.0  | 105,4      | 35,3     | 81,8       |
| 2005| 3500105  | Adamantina | 33764.0   | 16426.0 | 17338.0  | 105,6      | 35,7     | 82         |
| 2006| 3500105  | Adamantina | 33784.0   | 16428.0 | 17356.0  | 105,6      | 36,1     | 82         |
| 2007| 3500105  | Adamantina | 33791.0   | 16417.0 | 17374.0  | 105,8      | 36,5     | 82         |
| 2008| 3500105  | Adamantina | 33781.0   | 16397.0 | 17384.0  | 106        | 36,9     | 82         |
| 2009| 3500105  | Adamantina | 33765.0   | 16372.0 | 17393.0  | 106,2      | 37,3     | 82         |
| 2010| 3500105  | Adamantina | 33794.0   | 16374.0 | 17420.0  | 106,4      | 37,7     | 82         |
| 2011| 3500105  | Adamantina | 33908.0   | 16420.0 | 17488.0  | 106,5      | 38       | 82,3       |
| 2012| 3500105  | Adamantina | 34001.0   | 16454.0 | 17547.0  | 106,6      | 38,2     | 82,5       |
| 2013| 3500105  | Adamantina | 34085.0   | 16488.0 | 17597.0  | 106,7      | 38,5     | 82,7       |
| 2014| 3500105  | Adamantina | 34185.0   | 16528.0 | 17657.0  | 106,8      | 38,8     | 83         |
| 2015| 3500105  | Adamantina | 34285.0   | 16565.0 | 17720.0  | 107        | 39,1     | 83,2       |
| 2016| 3500105  | Adamantina | 34366.0   | 16598.0 | 17768.0  | 107        | 39,4     | 83,4       |
| 2017| 3500105  | Adamantina | 34455.0   | 16630.0 | 17825.0  | 107,2      | 39,6     | 83,6       |
| 2018| 3500105  | Adamantina | 34551.0   | 16668.0 | 17883.0  | 107,3      | 39,9     | 83,9       |
| 2019| 3500105  | Adamantina | 34643.0   | 16703.0 | 17940.0  | 107,4      | 40,2     | 84,1       |
| 2020| 3500105  | Adamantina | 34717.0   | 16732.0 | 17985.0  | 107,5      | 40,5     | 84,3       |
| 2021| 3500105  | Adamantina | 34708.0   | 16716.0 | 17992.0  | 107,6      | 40,8     | 84,2       |
| 2022| 3500105  | Adamantina | 34681.0   | 16699.0 | 17982.0  | 107,7      | 41,1     | 84,2       |
| 2023| 3500105  | Adamantina | 34706.0   | 16701.0 | 18005.0  | 107,8      | 41,4     | 84,2       |


<div style="text-align: center;">
  <p><em>Exemplo para o município de Adamantina (2000-2023)</em></p>
</div>