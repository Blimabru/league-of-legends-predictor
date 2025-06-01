"""
Módulo de Machine Learning para Previsão de Vitórias no League of Legends
------------------------------------------------------------------------
Este módulo implementa o modelo de aprendizado de máquina (Random Forest)
para prever a probabilidade de vitória com base nas estatísticas do jogador,
campeões utilizados e posições jogadas.
"""

# ===========================
# Dependências
# ===========================

import pandas as pd                                      # Manipulação e análise de dados
import numpy as np                                       # Computação numérica e arrays
from sklearn.ensemble import RandomForestClassifier      # Modelo de classificação baseado em árvores de decisão
from sklearn.model_selection import train_test_split     # Divisão dos dados em conjuntos de treino e teste

# ====================================
# Dicionário de Lanes
# ====================================

# Mapeamento das posições (roles) da API para nomes mais amigáveis na interface
# Isso torna a exibição das previsões mais compreensível para o usuário final
ROLE_MAPPING = {
    "UTILITY": "Suporte",    # Posição de suporte (normalmente bot lane com campeões de utilidade)
    "BOTTOM": "ADC",         # Posição de carry de dano físico (atiradores na bot lane)
    "TOP": "TOP",            # Posição de topo (normalmente tanques ou lutadores)
    "JUNGLE": "Jungle",      # Posição na selva (farm neutro e ganks nas lanes)
    "MIDDLE": "MID"          # Posição no meio (normalmente magos ou assassinos)
}

# ====================================
# Treinamento do modelo de Machine Learning
# ====================================

def trainModel(df):
    """
    Prepara os dados e treina um modelo de Random Forest para prever vitórias.
    
    O processo envolve:
    1. Transformação de variáveis categóricas (campeão, lane) em formato numérico
    2. Separação entre variáveis preditoras e variável alvo (vitória/derrota)
    3. Divisão em conjuntos de treino e teste para validação
    4. Treinamento do modelo Random Forest com os dados de treino
    
    Parâmetros:
        df (pandas.DataFrame): DataFrame com estatísticas das partidas do jogador
        
    Retorna:
        tuple: (modelo, x_train, x_test, y_train, y_test, df_encoded)
    """
    # Converte variáveis categóricas em colunas numéricas binárias (0/1)
    # Exemplo: 'champion=Yasuo' se torna coluna 'champion_Yasuo' com valor 1
    df_encoded = pd.get_dummies(df, columns=['champion', 'role'])
    
    # Separa variáveis independentes (X) e a variável dependente (y)
    x = df_encoded.drop('win', axis=1)   # Features que influenciam o resultado
    y = df_encoded['win']                # Target: True para vitória, False para derrota
    
    # Divide os dados em conjuntos de treino (80%) e teste (20%)
    # random_state=42 garante reprodutibilidade dos resultados
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )
    
    # Cria e treina o modelo Random Forest
    # Random Forest usa múltiplas árvores de decisão e combina seus resultados
    # para melhorar a precisão e evitar overfitting
    model = RandomForestClassifier(random_state=42)  # Inicializa o modelo
    model.fit(x_train, y_train)                      # Treina com os dados de treino
    
    # Retorna todos os elementos necessários para avaliação e previsão
    return model, x_train, x_test, y_train, y_test, df_encoded

# ==============================================
# Previsão de chances de vitória com campeões usados
# ==============================================

def predictByMostPlayed(model, x, df):
    """
    Prevê a probabilidade de vitória para as combinações mais relevantes
    de campeão e lane para o jogador analisado.
    
    Funcionamento:
    1. Identifica os campeões mais jogados e lanes mais frequentes
    2. Para cada combinação, cria um exemplo hipotético para previsão
    3. Usa o modelo treinado para calcular a probabilidade de vitória
    
    Parâmetros:
        model: Modelo Random Forest treinado
        x (DataFrame): Features de treino (para manter estrutura consistente)
        df (DataFrame): DataFrame original com dados das partidas
        
    Retorna:
        list: Lista de tuplas (campeão, lane, probabilidade_vitória)
    """
    # Obtém os 3 campeões mais jogados pelo usuário (por frequência)
    top_champions = df['champion'].value_counts().head(3).index
    
    # Obtém as 2 lanes/posições mais jogadas pelo usuário
    top_roles = df['role'].value_counts().head(2).index
    
    # Calcula estatísticas médias para usar na previsão
    kda_average = df['kda'].mean()         # Relação média de Kills/Deaths/Assists
    time_average = df['duration'].mean()   # Duração média das partidas em minutos
    
    # Lista para armazenar resultados das previsões
    predictions = []
    
    # Testa cada combinação de campeão e lane populares
    for champ in top_champions:
        for role in top_roles:
            # Cria um exemplo vazio com a mesma estrutura das features de treino
            # Inicializa com zeros todas as colunas (especialmente one-hot)
            entry = pd.DataFrame(np.zeros((1, x.shape[1])), columns=x.columns)
            
            # Define valores para as features numéricas
            entry['kda'] = kda_average          # Usa o KDA médio do jogador
            entry['duration'] = time_average    # Usa a duração média das partidas
            
            # Ativa o flag para o campeão específico (codificação one-hot)
            # Só ativa se a coluna existir (o campeão estava nos dados de treino)
            if f'champion_{champ}' in entry.columns:
                entry[f'champion_{champ}'] = 1  # 1 significa "este campeão está sendo usado"
                
            # Ativa o flag para a lane específica (codificação one-hot)
            if f'role_{role}' in entry.columns:
                entry[f'role_{role}'] = 1       # 1 significa "jogando nesta lane"
                
            # Calcula a probabilidade de vitória usando o modelo treinado
            # predict_proba retorna [prob_derrota, prob_vitória]
            # Multiplica por 100 para converter em porcentagem
            prob = model.predict_proba(entry)[0][1] * 100
            
            # Converte o código interno da lane para nome amigável ao usuário
            role_name = ROLE_MAPPING.get(role, role)
            
            # Adiciona o resultado à lista de previsões
            predictions.append((champ, role_name, prob))
            
    # Retorna todas as combinações com suas probabilidades
    return predictions