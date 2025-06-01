# 🔮 League of Legends Predictor

## 🔍 Visão Geral

O **League of Legends Predictor** é uma aplicação web interativa que utiliza técnicas de mineração de dados e machine learning para analisar o histórico de partidas de jogadores de League of Legends e prever chances de vitória com base em diversos fatores como campeões utilizados, posições jogadas e estatísticas de desempenho.

### 🎯 Objetivo Principal

Fornecer insights sobre o desempenho dos jogadores e prever probabilidades de vitória em diferentes cenários, ajudando os usuários a entender melhor suas tendências de jogo e áreas de melhoria potencial.

### 🔑 Funcionalidades Principais

- Análise detalhada do histórico de partidas do jogador
- Visualização de estatísticas gerais e taxa de vitória por campeão
- Avaliação de performance em diferentes posições (lanes)
- Previsão de chances de vitória com diferentes combinações de campeão e lane
- Apresentação do processo de mineração de dados de forma educativa
- Interface web interativa e responsiva

## 🏗️ Arquitetura do Sistema

O projeto segue uma arquitetura modular organizada em camadas:

```
League of Legends Predictor/
├── main.py                # Aplicação principal e interface
├── api_utils.py           # Comunicação com a API da Riot
├── data_processing.py     # Processamento dos dados brutos
├── model.py               # Implementação do modelo de ML
├── visualization.py       # Visualização de dados e resultados
├── credits.py             # Componente de créditos
├── requirements.txt       # Dependências do projeto
├── .env.template          # Template para configuração
└── README.md              # Documentação básica
```

### 📊 Fluxo de Dados

1. **Coleta de Dados**: Consulta à API da Riot Games para obter dados do jogador e partidas
2. **Processamento**: Transformação dos dados brutos em formato estruturado
3. **Modelagem**: Aplicação de técnicas de machine learning para previsão
4. **Visualização**: Apresentação interativa dos resultados e insights

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.8 ou superior
- Conta de desenvolvedor Riot Games com chave de API válida
- Conexão com internet para acessar a API

### Passos para Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/Blimabru/league-of-legends-predictor.git
   cd league-of-legends-predictor
   ```

2. **Crie um ambiente virtual**:
   #### No Linux/macOS
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

   #### No Windows
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**:
   ```bash
   # Copie o template de ambiente
   cp .env.template .env
   
   # Edite o arquivo .env inserindo sua chave de API
   # RIOT_API_KEY=RGAPI-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   # CONTINENT=americas (ou europe, asia, etc.)
   ```

5. **Execute a aplicação**:
   ```bash
   streamlit run main.py
   ```

## 💻 Uso da Aplicação

### Página Inicial

Ao iniciar a aplicação, você verá a interface principal com:
- Título e descrição do projeto
- Campos para inserir o Riot ID e Tagline do jogador
- Controle deslizante para selecionar o número de partidas a analisar
- Botão "Analisar Jogador" para iniciar o processo

### Analisando um Jogador

1. Insira o Riot ID no formato correto:
   - **Nome**: Parte principal do ID (ex: "PFM Misto Quente")
   - **Tagline**: Código após o "#" (ex: "PQP")

2. Ajuste o número de partidas a serem analisadas (10-100)
   - Mais partidas fornecem análises mais precisas, mas aumentam o tempo de processamento

3. Clique em "Analisar Jogador"
   - Uma barra de progresso indicará o status do processamento
   - Aguarde enquanto os dados são coletados e analisados

4. Explore as diferentes abas de resultados:
   - **📈 Estatísticas Gerais**: Visão geral do desempenho
   - **🔢 Avaliação do Modelo**: Métricas do modelo de machine learning
   - **🏆 Taxa de Vitória por Campeão**: Análise por campeão jogado
   - **📊 Distribuição de Lanes**: Análise por posições jogadas
   - **🔄 Processo de Mineração**: Detalhes do processamento de dados
   - **🔮 Previsão de Chances de Vitória**: Previsões para diferentes combinações

## 📋 Detalhes Técnicos dos Módulos

### 1. main.py - Módulo Principal

Este módulo implementa a interface do usuário e orquestra todo o fluxo da aplicação:


#### Fluxo principal

```python
if st.button("🔍 Analisar Jogador"):
    # 1. Buscar PUUID do jogador
    account = getPUUID(player_name, tag_line)
    puuid = account.get('puuid')
    
    # 2. Buscar histórico de partidas
    matches = getMatches(puuid, quant_matches)
    
    # 3. Processar dados das partidas
    df = processMatches(puuid, matches, progress_bar)
    
    # 4. Treinar modelo de machine learning
    model, x_train, x_test, y_train, y_test, df_encoded = trainModel(df)
    
    # 5. Exibir visualizações
    # Cada aba mostra uma visualização diferente
```

### 2. api_utils.py - Comunicação com API

Responsável por todas as interações com a API da Riot Games:

- `getPUUID()`: Obtém o identificador único do jogador
- `getMatches()`: Recupera lista de IDs de partidas recentes
- `getMatchDetails()`: Obtém dados detalhados de uma partida específica

Implementa:
- Cache de dados para evitar chamadas repetidas
- Controle de taxa de requisições (1 por segundo)
- Tratamento de erros de API

### 3. data_processing.py - Processamento de Dados

Transforma dados brutos da API em formato estruturado para análise:

- `processMatches()`: Função principal que itera sobre partidas e extrai estatísticas relevantes
- Cálculo de métricas derivadas como KDA e taxas de vitória
- Tratamento de valores ausentes e normalização

### 4. model.py - Machine Learning

Implementa o modelo preditivo usando Random Forest:

- `trainModel()`: Prepara dados e treina o modelo
  - One-hot encoding para variáveis categóricas
  - Split treino/teste (80%/20%)
  - Treinamento do modelo Random Forest

- `predictByMostPlayed()`: Gera previsões para combinações de campeão/lane
  - Identifica os campeões e lanes mais utilizados
  - Cria exemplos hipotéticos para previsão
  - Calcula probabilidades de vitória

### 5. visualization.py - Visualizações

Implementa todas as visualizações interativas:

- `show_general_stats()`: Estatísticas gerais do jogador
- `show_model_eval()`: Matriz de confusão e métricas do modelo
- `show_winrate_by_champion()`: Gráfico de taxa de vitória por campeão
- `show_role_distribution()`: Distribuição de posições jogadas
- `show_mining_process()`: Detalhes do processo de mineração
- `show_lane_predictions()`: Previsões por lane

### 6. credits.py - Componente de Créditos

Implementa o botão flutuante de créditos e sua funcionalidade:

- `show_credits_button()`: Cria botão flutuante com CSS personalizado
- `display_credits_if_active()`: Gerencia o estado de exibição dos créditos

## 🧠 Modelo de Machine Learning

### Algoritmo: Random Forest Classifier

O projeto utiliza o algoritmo Random Forest por diversas vantagens:

- **Robustez**: Lida bem com diferentes tipos de dados e outliers
- **Interpretabilidade**: Fornece medidas de importância das features
- **Performance**: Bom equilíbrio entre precisão e velocidade
- **Resistência ao overfitting**: Usa múltiplas árvores de decisão para generalizar melhor

### Features Utilizadas

- **Campeão**: One-hot encoding (uma coluna para cada campeão jogado)
- **Posição**: One-hot encoding (TOP, JUNGLE, MID, ADC, SUPORTE)
- **KDA**: Relação numérica (Kills + Assists) / Deaths
- **Duração**: Tempo de partida em minutos

### Fluxo de Treinamento

1. **Preparação dos dados**:
   - One-hot encoding para variáveis categóricas
   - Normalização para variáveis numéricas

2. **Divisão dos dados**:
   - 80% para treinamento
   - 20% para teste e validação

3. **Treinamento do modelo**:
   - Instanciação do RandomForestClassifier
   - Ajuste aos dados de treino

4. **Avaliação**:
   - Matriz de confusão
   - Métricas de precisão, recall e F1-score

### Previsões

O modelo gera previsões para as combinações mais relevantes de campeão e lane, calculando a probabilidade de vitória para cada cenário.

## ⚠️ Limitações e Considerações

### Limitações da API

- **Quota de requisições**: A API em modo de desenvolvimento da Riot tem limites de requisições (20 por segundo, 100 por 2 minutos), precisando ser renovada a cada 24 horas.
- **Histórico limitado**: Acesso apenas às partidas mais recentes
- **Tempo de resposta**: Análise de muitas partidas pode ser lenta

### Limitações do Modelo

- **Quantidade de dados**: Precisão limitada com poucas partidas (<20)
- **Viés de seleção**: Análise apenas das partidas mais recentes pode não representar o histórico completo
- **Generalização**: O modelo é treinado para um jogador específico, não generaliza para outros jogadores

### Considerações Técnicas

- **Throttling**: Implementado controle de taxa de 1 requisição/segundo para evitar limitações da API
- **Cache**: Resultados são armazenados em cache para melhorar performance
- **Dimensionalidade**: One-hot encoding pode criar muitas dimensões com muitos campeões diferentes

## 🛠️ Manutenção e Extensão

### Adicionando Novas Features

Para adicionar novas características ao modelo:

1. Modifique data_processing.py para extrair as novas métricas das partidas
2. Atualize model.py para incluir as novas features no treinamento
3. Se necessário, crie novas visualizações em visualization.py

### Atualizando para Novas Versões da API

A API da Riot Games pode mudar ocasionalmente. Se isso acontecer:

1. Verifique as mudanças na documentação oficial
2. Atualize as funções em api_utils.py para se adequar às novas endpoints ou parâmetros
3. Ajuste o processamento de dados conforme necessário

## 📝 FAQ - Perguntas Frequentes

### Gerais

**P: É necessário ter uma conta no League of Legends para usar?**  
R: Não para usar a aplicação, mas você precisa analisar contas existentes.

**P: Posso analisar qualquer jogador?**  
R: Sim, desde que você tenha o Riot ID e Tagline corretos.

**P: O aplicativo funciona para todas as regiões?**  
R: Sim, mas você precisa configurar a variável CONTINENT corretamente (.env).

### Técnicas

**P: Qual é a precisão média do modelo?**  
R: Geralmente entre 65-80%, dependendo do número de partidas analisadas.

**P: Por que escolher Random Forest e não outra técnica?**  
R: Random Forest oferece bom equilíbrio entre interpretabilidade, performance e resistência a overfitting.

**P: Posso treinar o modelo com mais partidas?**  
R: Sim, até 100 partidas, limitado pela API da Riot e performance.

**P: Como os dados são armazenados?**  
R: Os dados são processados em memória e não são persistidos entre sessões.

## 🔄 Diagrama de Fluxo Completo

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│  Interface  │────▶│ API da Riot │ ───▶│ Processamento │
│  (main.py)  │     │ (api_utils)  │     │    de Dados   │
└─────────────┘     └──────────────┘     │(data_process) │
       ▲                                 └───────┬───────┘
       │                                         │
       │                                         ▼
┌─────────────┐     ┌──────────────┐     ┌───────────────┐
│Visualização │◀───│   Modelo     │◀─── │  Treinamento  │
│(visualiza-  │     │  Treinado    │     │   do Modelo   │
│  tion.py)   │     │  (model.py)  │     │   (model.py)  │
└─────────────┘     └──────────────┘     └───────────────┘
```

## 📜 Requisitos e Dependências


### Interface e API
```
streamlit>=1.32.0      # Framework para criação de aplicações web interativas
requests>=2.31.0       # Biblioteca para requisições HTTP à API da Riot Games
python-dotenv>=1.0.1   # Gerenciamento de variáveis de ambiente (.env)
```

### Análise e Processamento de Dados
```
pandas>=2.2.2          # Manipulação e análise de dados tabulares
numpy>=1.26.4          # Operações numéricas e manipulação de arrays
```

### Visualização de Dados
```
matplotlib>=3.8.4      # Criação de gráficos estáticos
seaborn>=0.13.2        # Visualizações estatísticas baseadas em matplotlib
plotly>=5.22.0         # Gráficos interativos para dashboard
```

### Machine Learning
```
scikit-learn>=1.4.2    # Algoritmos de aprendizado de máquina (Random Forest)
```

---

## 📞 Suporte e Contato

Para questões, sugestões ou contribuições, visite o repositório GitHub:
[https://github.com/Blimabru/league-of-legends-predictor](https://github.com/Blimabru/league-of-legends-predictor)

---

*Nota: Este aplicativo não é afiliado à Riot Games e utiliza a API pública oficial para fins educacionais e analíticos.*