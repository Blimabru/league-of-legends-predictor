"""
Módulo Principal do Preditor de Vitórias no League of Legends
------------------------------------------------------------
Este aplicativo usa a API da Riot Games para coletar dados de jogadores,
processa esses dados com técnicas de mineração de dados e machine learning,
e exibe visualizações e previsões interativas no navegador através do Streamlit.
"""

# ===========================
# Dependências
# ===========================

import streamlit as st          # Interface Web para aplicação

# Importa funções para acessar a API da Riot (PUUID, histórico de partidas)
from api_utils import getPUUID, getMatches

# Importa função para processar os dados das partidas em DataFrame
from data_processing import processMatches

# Importa funções de machine learning: treinamento, predição e mapeamento de roles
from model import trainModel, predictByMostPlayed, ROLE_MAPPING

# Importa funções para visualização dos resultados e gráficos
from visualization import (
    show_general_stats,        # Estatísticas gerais do jogador
    show_model_eval,           # Métricas de avaliação do modelo
    show_winrate_by_champion,  # Taxa de vitória por campeão
    show_role_distribution,    # Distribuição de lanes jogadas
    show_mining_process,       # Processo de mineração de dados
    show_lane_predictions      # Previsões por lane
)

# Importa módulo de créditos
from credits import display_credits_if_active

# ===========================
# Configuração da página
# ===========================

# Define o título da página, largura (wide permite usar toda a janela do navegador)
st.set_page_config(page_title="Análise de LoL", layout="wide")

# ===========================
# Exibe o botão e conteúdo de créditos
# ===========================
display_credits_if_active()

# ===========================
# Título e descrição
# ===========================

# Título principal do aplicativo
st.title("🔮 Previsão de Vitórias no League of Legends")
st.markdown("<br>", unsafe_allow_html=True)  # Espaço em branco

# Expander com explicação resumida do funcionamento do aplicativo
with st.expander("Este aplicativo utiliza mineração de dados para analisar estatísticas de jogadores e prever chances de vitória com base no histórico de partidas."):
    st.markdown("""
    - **Mineração de Dados**: Coleta informações de partidas jogadas, como campeões usados, taxa de vitórias, KDA, e Lanes jogadas.
    - **Machine Learning**: Treina um modelo de Random Forest para prever a probabilidade de vitória com base nos dados coletados.
    """)

st.markdown("<br><br>", unsafe_allow_html=True)  # Espaço adicional

# ===========================
# Entrada de dados do usuário
# ===========================

# Layout de três colunas para entrada do Riot ID (format: name#tag)
colRiotId, colHashtag, colTagLine = st.columns([2, 0.1, 1])

with colRiotId:
    # Campo para o nome do jogador
    player_name = st.text_input("Riot ID", "PFM Misto Quente", help="Insira o Riot ID do jogador.")

with colHashtag:
    # Símbolo '#' entre nome e tagline (apenas visual)
    st.markdown("<h1 style='text-align: center;'>#</h1>", unsafe_allow_html=True)

with colTagLine:
    # Campo para a tagline do jogador
    tag_line = st.text_input("Tagline", "PQP", help="Insira a Tagline do jogador.")

# Controle deslizante para selecionar o número de partidas a analisar
quant_matches = st.slider(
    "Número de partidas a analisar",
    min_value=10,         # Mínimo de 10 partidas
    max_value=100,        # Máximo de 100 partidas
    value=20,             # Valor padrão: 20 partidas
    help="Escolha o número de partidas que deseja analisar. Mais partidas podem levar mais tempo."
)

# =============================
# Fluxo principal da aplicação
# =============================

# Botão que inicia o processo de análise quando clicado
if st.button("🔍 Analisar Jogador"):
    # Elementos de UI para feedback visual do progresso
    progress_bar = st.progress(0)  # Barra de progresso iniciando em 0%
    status_text = st.empty()       # Espaço para texto de status atualizável

    # ETAPA 1: Buscar o PUUID do jogador na API da Riot
    status_text.text("🔍 Procurando jogador...")
    account = getPUUID(player_name, tag_line)  # Busca informações da conta
    puuid = account.get('puuid')               # Extrai o PUUID (identificador único)
    progress_bar.progress(0.15)                # Atualiza progresso para 15%

    # Verifica se o jogador foi encontrado
    if not puuid:
        # Exibe mensagem de erro se o jogador não for encontrado
        st.error(f"Erro ao buscar jogador: {account.get('message', 'Jogador não encontrado.')}")
    else:
        # ETAPA 2: Buscar histórico de partidas
        status_text.text("⬇️ Baixando histórico de partidas...")
        matches = getMatches(puuid, quant_matches)  # Obtém IDs das partidas recentes
        progress_bar.progress(0.3)                  # Atualiza progresso para 30%

        # ETAPA 3: Processar os dados das partidas
        status_text.text("🎲 Montando DataFrame...")
        # Processa os detalhes de cada partida e cria um DataFrame
        df = processMatches(puuid, matches, progress_bar)
        progress_bar.progress(0.45)  # Atualiza progresso para 45%

        # ETAPA 4: Preparar os dados para machine learning
        status_text.text("🔢 Realizando One-Hot Encoding")
        progress_bar.progress(0.7)   # Atualiza progresso para 70%

        # ETAPA 5: Treinar o modelo de machine learning
        status_text.text("🔢 Aplicando algoritmo Random Forest...")
        # Treina o modelo e obtém os conjuntos de dados e o DataFrame codificado
        model, x_train, x_test, y_train, y_test, df_encoded = trainModel(df)
        progress_bar.progress(1.0)   # Completa a barra de progresso (100%)
        status_text.text("Concluído!")

        # ETAPA 6: Criar abas para exibir diferentes visualizações
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📈 Estatísticas Gerais",
            "🔢 Avaliação do Modelo",
            "🏆 Taxa de Vitória por Campeão",
            "📊 Distribuição de Lanes",
            "🔄 Processo de Mineração",
            "🔮 Previsão de Chances de Vitória por Lane",
        ])

        # Preenche cada aba com a visualização correspondente
        with tab1:
            # Exibe estatísticas gerais do jogador
            show_general_stats(df)
        with tab2:
            # Exibe métricas de avaliação do modelo (precisão, recall, etc.)
            show_model_eval(model, x_test, y_test)
        with tab3:
            # Exibe gráfico de taxa de vitória por campeão jogado
            show_winrate_by_champion(df)
        with tab4:
            # Exibe gráfico de distribuição de lanes/posições jogadas
            show_role_distribution(df)
        with tab5:
            # Exibe detalhes do processo de mineração e transformação de dados
            show_mining_process(df, df_encoded, model, x_train, y_train, x_test, y_test)
        with tab6:
            # Exibe previsões de chance de vitória por lane/posição
            show_lane_predictions(model, x_train, df)