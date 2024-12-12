# Predição de criminalidade

Este notebook foi desenvolvido para abordar um problema de predição de padrões criminais no Estado de São Paulo. Ele organiza o trabalho em etapas que abrangem desde a formulação do problema até a implementação e validação de alguns modelos.

## Etapas do trabalho

### 1. Introdução ao problema

Uma primeira vista ao problema subentende que a etapa final, destinada aos modelos de predição, visa aplicar métodos de regressão a fim de obter estimadores para o índice de criminalidade para cada município. A forma com a qual é constituído o índice, porém, introduz alguns vieses a análise, o que dificultava a predição:

- **Pesos arbitrários:** pesos atribuídos aos diferentes crimes eram arbitrários e falhavam na tentativa de quantificar a gravidade de diferentes ocorrências: um homicídio não deve ser comparado a um número "n" de furtos, são equivalências que não fazem sentido.
- **Falta de representatividade:** crimes hediondos ocorrem predominantemente em grandes cidades, afetando a análise espacial.

Para contornar essas limitações, optou-se por prever o número total de roubos, uma métrica mais uniforme e confiável.

### 2. Filtragem e processamento dos dados

#### Sistema de coordenadas cartográficas

Para garantir precisão em análises espaciais, as coordenadas geográficas dos municípios foram convertidas para a projeção UTM (Zona 23S), minimizando distorções em distâncias e áreas.

#### Análise de autocorrelação espacial

Foi explorada a dependência espacial dos dados de roubos, utilizando técnicas como krigagem e variogramas.

### 3. Modelagem preditiva

A modelagem foi conduzida em algumas frentes principais:

#### Modelos "baseline" clássicos, para efeito de comparação

#### Modelos estatísticos para prever a criminalidade

- **Spatial Lag Model (SLM):** considera a dependência espacial na variável dependente, utilizando a matriz de pesos espaciais baseada nos 10 vizinhos mais próximos.
- **Spatial Error Model (SEM):** captura a dependência espacial nos erros do modelo, indicando a presença de fatores omitidos correlacionados espacialmente.


#### Modelos baseados em aprendizado profundo para modelar a estrutura espacial dos dados

- **Graph Neural Networks (GNNs):** utilizadas para modelar a estrutura espacial dos dados, representando municípios como nós em um grafo com atributos socioeconômicos.
  - **Graph Autoencoder (GAE):** modelo que mapeia grafos para espaços latentes, minimizando a loss entre as matrizes de adjacências real e reconstruída.
  - **NAGAE (Attention-Enhanced GAE):** extensão do GAE com mecanismos de atenção, ajustando dinamicamente a relevância das conexões entre nós e melhorando a modelagem em grafos heterogêneos.

Para mitigar problemas de multicolinearidade entre variáveis explicativas, foi utilizado o fator de inflação da variância (VIF).

### 4. Validação e resultados

As técnicas aplicadas foram validadas utilizando métodos robustos como validação cruzada, explorando o desempenho dos modelos na predição do número total de roubos. Resultados preliminares mostram que a combinação de modelos estatísticos e aprendizado profundo proporciona insights complementares e eficientes.

---
