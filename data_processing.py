"""
Módulo de Processamento de Dados do League of Legends
----------------------------------------------------
Este módulo transforma dados brutos de partidas da API da Riot em um formato
estruturado e limpo para análise e modelagem preditiva.
"""

# ===========================
# Dependências
# ===========================

import pandas as pd         # Biblioteca para manipulação e análise de dados tabulares
import streamlit as st      # Framework para criação de aplicações web interativas

from api_utils import getMatchDetails  # Função para obter detalhes de partidas da API Riot

# ========================================
# Processamento dos dados das partidas
# ========================================

def processMatches(puuid, matches, progress_bar):
    """
    Processa os dados das partidas de um jogador específico.
    
    Fluxo de Funcionamento:
    1. Itera sobre cada ID de partida na lista fornecida
    2. Obtém os detalhes completos da partida da API
    3. Filtra para encontrar o jogador específico pelo PUUID
    4. Extrai métricas relevantes de desempenho (KDA, dano, ouro, etc.)
    5. Atualiza a barra de progresso visual para feedback ao usuário
    6. Retorna um DataFrame estruturado com todas as estatísticas
    
    Parâmetros:
        puuid (str): Identificador único do jogador a ser analisado
        matches (list): Lista de IDs de partidas a processar
        progress_bar (st.progress): Objeto de barra de progresso do Streamlit
        
    Retorna:
        pandas.DataFrame: Tabela com estatísticas de todas as partidas do jogador
    """
    # Lista vazia para armazenar os dados processados de cada partida
    data = []
    
    # Itera sobre cada partida, mantendo o índice para atualizar a barra de progresso
    for i, match_id in enumerate(matches):
        # Obtém os detalhes completos da partida através da API
        match = getMatchDetails(match_id)
        
        # Procura nos participantes da partida pelo jogador com o PUUID especificado
        # O método .get() com valor padrão {} evita erros se 'info' ou 'participants' não existirem
        for player in match.get('info', {}).get('participants', []):
            if player['puuid'] == puuid:
                # Quando encontra o jogador, extrai as estatísticas relevantes
                data.append({
                    'champion': player['championName'],                        # Nome do campeão usado
                    'win': player['win'],                                      # Resultado da partida (True/False)
                    'kills': player['kills'],                                  # Número de abates
                    'deaths': player['deaths'],                                # Número de mortes
                    'assists': player['assists'],                              # Número de assistências
                    'kda': (player['kills'] + player['assists']) / (player['deaths'] or 1),  # Cálculo do KDA (divisão por 1 evita divisão por zero)
                    'role': player['teamPosition'],                            # Posição/Lane jogada
                    'duration': match['info']['gameDuration'] / 60,            # Duração da partida em minutos
                    'gold': player.get('goldEarned', 0),                       # Ouro ganho na partida
                    'damage': player.get('totalDamageDealtToChampions', 0),    # Dano total causado a campeões
                    'farm': player.get('totalMinionsKilled', 0),               # Total de minions eliminados
                    'vision': player.get('visionScore', 0),                    # Pontuação de visão
                    'first_blood': int(player.get('firstBloodKill', False)),   # Se conseguiu o primeiro abate (1=sim, 0=não)
                })
                # Após encontrar e processar o jogador, não precisa continuar verificando outros
                break
                
        # Atualiza a barra de progresso com base na proporção de partidas processadas
        progress_bar.progress((i + 1) / len(matches))
        
    # Converte a lista de dicionários em um DataFrame pandas estruturado
    # Cada linha representa uma partida, cada coluna uma estatística
    return pd.DataFrame(data)