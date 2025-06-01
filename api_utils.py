"""
Módulo de utilidades para acessar a API da Riot Games
-----------------------------------------------------
Este módulo fornece funções para interagir com a API da Riot Games,
facilitando a obtenção de dados de jogadores e partidas de League of Legends.
"""

# ===========================
# Dependências
# ===========================

import requests                     # Requisições HTTP para API Riot
import time                         # Controle de tempo para throttling de requisições
import os                           # Acesso a variáveis de ambiente e sistema de arquivos
from dotenv import load_dotenv      # Carrega variáveis de ambiente do arquivo .env
import streamlit as st              # Interface web para a aplicação

# ===========================
# Carrega as variáveis do .env
# ===========================

# Carrega as variáveis do arquivo .env com prioridade sobre variáveis de ambiente existentes
load_dotenv(override=True)

# Obtém a chave da API e o continente das variáveis de ambiente
API_KEY = os.getenv("RIOT_API_KEY")  # Chave de autenticação para a API da Riot
CONTINENT = os.getenv("CONTINENT")   # Região/continente (ex: americas, europe, asia)
HEADERS = {"X-Riot-Token": API_KEY}  # Cabeçalho HTTP com token de autenticação

# ========================================
# Funções auxiliares para acessar a API
# ========================================

# Decorator @st.cache_data armazena em cache o resultado da função para evitar chamadas repetidas à API
# show_spinner=False impede que o Streamlit mostre um indicador de carregamento
@st.cache_data(show_spinner=False)
def getPUUID(player_name, tag_line):
    """
    Obtém o PUUID (identificador único universal do jogador) usando nome e tagline do Riot ID.
    
    Parâmetros:
        player_name (str): Nome do jogador (ex: "FakerLeBlanc")
        tag_line (str): Tag do jogador (ex: "KR1")
        
    Retorna:
        dict: Objeto JSON com informações do jogador, incluindo o PUUID
    """
    url = f"https://{CONTINENT}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{player_name}/{tag_line}?api_key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

@st.cache_data(show_spinner=False)
def getMatches(puuid, quant):
    """
    Recupera os IDs das últimas partidas de um jogador usando seu PUUID.
    
    Parâmetros:
        puuid (str): Identificador único do jogador
        quant (int): Quantidade de partidas a serem recuperadas
        
    Retorna:
        list: Lista de IDs de partidas
    """
    url = f"https://{CONTINENT}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={quant}&api_key={API_KEY}"
    response = requests.get(url, headers=HEADERS)
    return response.json()

def getMatchDetails(match_id):
    """
    Obtém dados detalhados de uma partida específica.
    
    Implementa:
    - Controle de taxa de requisições (1 requisição por segundo)
    - Tratamento de erros HTTP
    
    Parâmetros:
        match_id (str): Identificador da partida
        
    Retorna:
        dict: Objeto JSON com todos os detalhes da partida ou dict vazio em caso de erro
    """
    url = f"https://{CONTINENT}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={API_KEY}"

    try:
        response = requests.get(url, headers=HEADERS)

        time.sleep(1)  # Pausa de 1 segundo para evitar atingir limites de taxa da API

        response.raise_for_status()  # Levanta exceção para códigos de erro HTTP (4xx, 5xx)

        return response.json()
    
    except requests.exceptions.RequestException as e:
        # Exibe mensagem de erro na interface e no console
        st.error(f"Erro ao buscar detalhes da partida {match_id}: {e}")

        print(f"Erro ao buscar detalhes da partida {match_id}: {e}")

        return {}  # Retorna dicionário vazio em caso de erro