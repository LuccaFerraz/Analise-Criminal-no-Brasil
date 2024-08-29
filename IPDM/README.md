# IPDM (Índice Paulista de Desenvolvimento Municipal)

Por que agregar essas informações ao conjunto de ocorrências da **SSP-SP**?

O objetivo do Índice Paulista de Desenvolvimento Municipal é "Comparar o esforço dos municípios paulistas para aumentar o desenvolvimento para sua população", como se define em sua documentação. Por isso, concluiu-se que entender a dinâmica de desenvolvimento da Riqueza, Longevidade e Escolaridade dos municípios do Estado de São Paulo seria benéfico para ter um panorama geral dos últimos anos e, possivelmente explicar as ocorrências criminais processadas da SSP-SP.

O IPDM é caracterizado pelas seguintes classes:

- Muito alto: 0.600 (+)
- Alto:  0.550 - 0.600
- Médio: 0.500 - 0.550
- Baixo: 0.500 (-) 

Os três domínios considerados no cálculo foram baseados nas seguintes variáveis:

### Riqueza
1. Consumo anual de energia elétrica, por ligação residencia.
2. Consumo anual de energia elétrica no comércio, na agricultura e nos serviços, por ligação. 
3. valor do rendimento de empregados formais e dos benefícios do INSS de aposentados e pensionistas.
4. Produto Interno Bruto Per capita 2022 (Estimativa para os outros anos) 

### Longevidade
1. Taxas de mortalidade infantil (por mil nascidos vivos)
2. Taxas de mortalidade perinatal (por mil nascidos vivos) 
3. Taxas de mortalidade 15 a 39 anos (por mil hab.) 
4. Taxas de mortalidade  60 a 69 anos (por mil hab.) 

### Escolaridade
1. Taxa de atendimento escolar na faixa etária de 0 a 3 anos (acesso à creche)
2. Proporção média de alunos do 5º ano com proficiência em Língua Portuguesa e Matemática (%)
3. Proporção média de  alunos do 9º ano com proficiência em Língua Portuguesa e Matemática (%)
3. Taxas de distorção idade-série no Ensino Médio (%)

## A Base
Originalmente, os dados do IPDM foram organizados em cinco anos: 2014, 2016, 2018, 2020 e 2022. Em cada ano, registrou-se 16 indicadores correspondentes aos âmbitos de Riqueza, Longevidade e Educação para cada município.

Como possivelmente essa base terá uma abordagem de Séries Temporais, optou-se por segmentar os dados por ano. Além disso, agregou-se as 80 informações de cada município em apenas uma linha, o que a princípio, eram 80 instâncias, uma referente a cada indicador em cada ano.

|   Unnamed: 0 |   cod_ibge | Municipio   | Valor            |   Ano | Tipo         | Valor_Estado   | Indicador1                                                      | Indicador2                                                                                 | Indicador3                                                                                  | Indicador4                                         | Indicador5             |
|-------------:|-----------:|:------------|:-----------------|------:|:-------------|:---------------|:----------------------------------------------------------------|:-------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------|:---------------------------------------------------|:-----------------------|
|            0 |    3500105 | Adamantina  | ,548             |  2014 | IPDM         | ,535           |                                                                 |                                                                                            |                                                                                             |                                                    |                        |
|         3225 |    3500105 | Adamantina  | 2,42000319030148 |  2014 | Riqueza      | 2,54           | Consumo anual de energia elétrica residencial (MWh) por ligação |                                                                                            |                                                                                             |                                                    |                        |
|         6450 |    3500105 | Adamantina  | 8,97541371158392 |  2014 | Riqueza      | 24,47          |                                                                 | Consumo anual de energia elétrica comercial, serviços e rural (MWh) por ligação            | Rendimento do trabalho formal mais benefícios previdenciários per capita (R$ de 2022)      | Produto Interno Bruto per capita (R$ de 2022)     |                        |
|        38700 |    3500105 | Adamantina  | 8,44444444444444 |  2014 | Escolaridade | 14,5           |                                                                 |                                                                                            |                                                                                             | Taxas de distorção idade-série no Ensino Médio (%) |                        |
|        41925 |    3500105 | Adamantina  | ,365             |  2014 | Riqueza      | ,457           |                                                                 |                                                                                            |                                                                                             |                                                    | Indicador Riqueza      |
|        41930 |    3500105 | Adamantina  | ,77              |  2014 | Longevidade  | ,698           |                                                                 |                                                                                            |                                                                                             |                                                    | Indicador Longevidade  |
|        41935 |    3500105 | Adamantina  | ,51              |  2014 | Escolaridade | ,449           |                                                                 |                                                                                            |                                                                                             |                                                    | Indicador Escolaridade |


<div style="text-align: center;">
  <p><em>Exemplo da base Original para o município de Adamantina (2014)</em></p>
</div>