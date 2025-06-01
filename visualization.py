"""
Módulo de Visualização de Dados do League of Legends Predictor
-------------------------------------------------------------
Este módulo implementa funções para criar visualizações interativas
dos dados processados e resultados do modelo de machine learning,
utilizando Streamlit e Plotly para gráficos interativos.
"""

# ===========================
# Dependências
# ===========================
import streamlit as st           # Framework para criação de aplicações web interativas
import plotly.express as px      # Biblioteca para gráficos interativos e responsivos
import pandas as pd              # Manipulação e análise de dados tabulares
from sklearn.metrics import confusion_matrix, classification_report  # Métricas para avaliação de modelos ML

from model import ROLE_MAPPING, predictByMostPlayed  # Importa mapeamento de roles e função de predição

# ====================================
# Funções de Visualização
# ====================================

def show_general_stats(df):
    """
    Exibe estatísticas gerais do jogador analisado.
    
    Apresenta:
    - Total de partidas analisadas
    - Taxa de vitórias global
    - Gráfico de pizza com proporção de vitórias e derrotas
    
    Parâmetros:
        df (pandas.DataFrame): DataFrame com estatísticas das partidas
    """
    # Adiciona subtítulo na interface
    st.subheader("📈 Estatísticas Gerais")
    
    # Exibe métricas básicas como texto
    st.write(f"**Total de partidas analisadas:** {len(df)}")
    st.write(f"**Taxa de vitórias:** {df['win'].mean() * 100:.0f}%")
    
    # Calcula quantidades absolutas de vitórias e derrotas
    victories = df['win'].sum()                # Soma de True (1) na coluna 'win'
    defeats = len(df) - victories              # Total de partidas menos vitórias
    
    # Cria gráfico de pizza usando plotly express
    fig = px.pie(
        names=['Vitórias', 'Derrotas'],        # Nomes das fatias
        values=[victories, defeats],            # Valores para cada fatia
        color=['Vitórias', 'Derrotas'],         # Cores diferentes para cada categoria
        color_discrete_map={'Vitórias': '#4CAF50', 'Derrotas': '#F44336'},  # Verde para vitórias, vermelho para derrotas
        title='Proporção de Vitórias e Derrotas'  # Título do gráfico
    )
    
    # Personaliza o estilo do texto no gráfico
    fig.update_traces(
        textinfo='percent+label',               # Mostra porcentagem e rótulo em cada fatia
        textfont=dict(size=16, family="Arial", color="black"),  # Fonte do texto
        insidetextfont=dict(size=16, family="Arial", color="black"),  # Fonte dentro das fatias
        textfont_weight='bold'                  # Texto em negrito
        )
    
    # Exibe o gráfico interativo na interface Streamlit
    st.plotly_chart(fig)

def show_model_eval(model, x_test, y_test):
    """
    Visualiza a avaliação do desempenho do modelo de machine learning.
    
    Apresenta:
    - Matriz de confusão: visualização de verdadeiros/falsos positivos/negativos
    - Relatório de classificação: precisão, recall, f1-score
    
    Parâmetros:
        model: Modelo Random Forest treinado
        x_test: Features do conjunto de teste
        y_test: Target do conjunto de teste (win/loss)
    """
    # Adiciona subtítulo na interface
    st.subheader("📊 Avaliação do Modelo")
    
    # Faz previsões com o modelo no conjunto de teste
    y_pred = model.predict(x_test)
    
    # Calcula a matriz de confusão (compara valores reais vs. preditos)
    # [0,0]: Verdadeiros Negativos, [0,1]: Falsos Positivos
    # [1,0]: Falsos Negativos, [1,1]: Verdadeiros Positivos
    cm = confusion_matrix(y_test, y_pred)
    
    # Cria visualização da matriz de confusão com plotly
    fig_cm = px.imshow(
        cm,                                    # Matriz de confusão calculada
        labels=dict(x="Predito", y="Real", color="Qtd"),  # Rótulos dos eixos
        x=["Derrota", "Vitória"],              # Rótulos do eixo x (colunas)
        y=["Derrota", "Vitória"],              # Rótulos do eixo y (linhas)
        color_continuous_scale="Blues",        # Escala de cores (azuis)
        text_auto=True,                        # Mostra valores automaticamente
        title="Matriz de Confusão"             # Título do gráfico
    )
    
    # Personaliza o estilo dos eixos e texto
    fig_cm.update_xaxes(tickfont=dict(size=16, family="Arial", color="black"))
    fig_cm.update_yaxes(tickfont=dict(size=16, family="Arial", color="black"))
    fig_cm.update_traces(textfont=dict(size=18, family="Arial", color="black"))
    
    # Exibe o gráfico na interface
    st.plotly_chart(fig_cm)
    
    # Adiciona título para o relatório de classificação
    st.write("**Relatório de Classificação:**")
    
    # Gera relatório detalhado de métricas de classificação
    # output_dict=True retorna o relatório como dicionário para manipulação
    report = classification_report(y_test, y_pred, output_dict=True)
    
    # Converte o relatório para DataFrame para melhor visualização
    report_df = pd.DataFrame(report).transpose()
    
    # Exibe o relatório como tabela interativa no Streamlit
    st.dataframe(report_df)

def show_winrate_by_champion(df):
    """
    Exibe a taxa de vitória por campeão utilizado pelo jogador.
    
    Apresenta um gráfico de barras dos 10 campeões com maior taxa de vitória.
    
    Parâmetros:
        df (pandas.DataFrame): DataFrame com estatísticas das partidas
    """
    # Adiciona subtítulo na interface
    st.subheader("🏆 Taxa de Vitória por Campeão")
    
    # Calcula a taxa de vitória para cada campeão
    # 1. Agrupa por campeão
    # 2. Calcula a média da coluna 'win' (True=1, False=0)
    # 3. Converte para porcentagem multiplicando por 100
    # 4. Ordena em ordem crescente (para mostrar os piores primeiro)
    win_rate = df.groupby('champion')['win'].mean().sort_values(ascending=True) * 100
    
    # Cria gráfico de barras para os 10 campeões com maior taxa de vitória
    fig_bar = px.bar(
        win_rate.head(10),                     # Seleciona os 10 primeiros (pior desempenho)
        x=win_rate.head(10).index,             # Nomes dos campeões no eixo X
        y=win_rate.head(10).values,            # Taxa de vitória no eixo Y
        labels={'x': 'Campeão', 'y': 'Taxa de Vitória (%)'},  # Rótulos dos eixos
        title="Top 10 Campeões - Maior Taxa de Vitória"       # Título do gráfico
    )
    
    # Exibe o gráfico na interface
    st.plotly_chart(fig_bar)

def show_role_distribution(df):
    """
    Visualiza a distribuição de lanes (posições) jogadas pelo usuário.
    
    Apresenta um gráfico de pizza mostrando a proporção de partidas
    em cada lane/posição do mapa.
    
    Parâmetros:
        df (pandas.DataFrame): DataFrame com estatísticas das partidas
    """
    # Adiciona subtítulo na interface
    st.subheader("📊 Distribuição de Lanes")
    
    # Calcula a contagem de partidas por lane/role
    role_distribution = df['role'].value_counts()
    
    # Cria gráfico de pizza usando plotly express
    fig_roles = px.pie(
        # Converte códigos de role (ex: "UTILITY") para nomes amigáveis (ex: "Suporte")
        names=role_distribution.index.map(ROLE_MAPPING),  
        values=role_distribution.values,        # Número de partidas em cada lane
        color=role_distribution.index.map(ROLE_MAPPING),  # Cores diferentes por lane
        color_discrete_sequence=px.colors.qualitative.Pastel,  # Paleta de cores pastel
        title="Distribuição de Lanes"           # Título do gráfico
    )
    
    # Personaliza o estilo do texto no gráfico
    fig_roles.update_traces(
        textinfo='percent+label',               # Mostra porcentagem e rótulo
        textfont=dict(size=16, family="Arial", color="black"),  # Fonte do texto
        insidetextfont=dict(size=16, family="Arial", color="black"),  # Fonte dentro das fatias
        textfont_weight='bold'                  # Texto em negrito
    )
    
    # Exibe o gráfico na interface
    st.plotly_chart(fig_roles)

def show_mining_process(df, df_encoded, model, x_train, y_train, x_test, y_test):
    """
    Apresenta detalhes do processo de mineração de dados e machine learning.
    
    Exibe:
    - DataFrame original antes do processamento
    - DataFrame codificado após one-hot encoding
    - Importância das variáveis para o modelo
    - Informações sobre divisão treino/teste
    
    Organizado em abas para melhor navegação.
    
    Parâmetros:
        df: DataFrame original
        df_encoded: DataFrame após one-hot encoding
        model: Modelo treinado
        x_train, y_train: Dados de treino
        x_test, y_test: Dados de teste
    """
    # Adiciona subtítulo na interface
    st.subheader("🔄 Processo de Mineração")
    
    # Cria abas para organizar as diferentes visualizações
    subtab1, subtab2, subtab3, subtab4 = st.tabs([
        "DataFrame Original",    # Dados brutos
        "DataFrame Codificado",  # Dados após processamento
        "Variáveis",             # Importância das features
        "Dados de Treino/Teste"  # Informações de particionamento
    ])
    
    # Aba 1: DataFrame Original
    with subtab1:
        st.write("**DataFrame Original:**")
        st.write("1. **Coleta de Dados:** Os dados são coletados diretamente da API da Riot Games.")
        st.write("2. **Processamento:** As informações das partidas são organizadas em um DataFrame.")
        st.dataframe(df)  # Exibe o DataFrame original
    
    # Aba 2: DataFrame após One-Hot Encoding
    with subtab2:
        st.write("**DataFrame Codificado:**")
        st.write("3. **Conversão de Dados:** Variáveis categóricas, como campeões e roles, são convertidas em valores numéricos - Utiliza **One-Hot Encoding**.")
        st.dataframe(df_encoded)  # Exibe o DataFrame codificado
    
    # Aba 3: Importância das Variáveis
    with subtab3:
        st.write("### Importância das variáveis para o modelo:")
        # Extrai a importância de cada feature do modelo Random Forest
        importances = model.feature_importances_  # Array de importâncias
        feature_names = x_train.columns           # Nomes das features
        
        # Cria DataFrame com features e suas importâncias
        importances_df = pd.DataFrame({'feature': feature_names, 'importance': importances})
        
        # Exibe as features ordenadas por importância (mais importantes primeiro)
        st.dataframe(importances_df.sort_values('importance', ascending=False))
    
    # Aba 4: Informações sobre Dados de Treino e Teste
    with subtab4:
        st.write("### **Dados de Treino e Teste**")
        # Explica como os dados são divididos
        st.markdown("""
        Após o processamento e conversão dos dados, eles são divididos em dois conjuntos:
        - **Dados de Treino:** Usados para treinar o modelo de Machine Learning. Este conjunto representa aproximadamente 80% dos dados disponíveis.
        - **Dados de Teste:** Usados para avaliar o desempenho do modelo. Este conjunto representa aproximadamente 20% dos dados disponíveis.
        """)
        
        # Exibe dimensões dos conjuntos de treino
        st.write("#### **Dimensões dos Dados de Treino:**")
        st.write(f"- **x_train:** {x_train.shape} (Características usadas para treinar o modelo)")
        st.write(f"- **y_train:** {y_train.shape} (Rótulos correspondentes às vitórias ou derrotas)")
        
        # Exibe dimensões dos conjuntos de teste
        st.write("#### **Dimensões dos Dados de Teste:**")
        st.write(f"- **x_test:** {x_test.shape} (Características usadas para avaliar o modelo)")
        st.write(f"- **y_test:** {y_test.shape} (Rótulos correspondentes às vitórias ou derrotas)")
        
        # Explica como funciona o processo de treinamento/teste
        st.markdown("""
        **Como funciona:**
        - O conjunto de treino (**x_train**, **y_train**) é usado para ajustar os parâmetros do modelo de Random Forest.
        - O conjunto de teste (**x_test**, **y_test**) é usado para verificar se o modelo consegue generalizar bem para dados que ele nunca viu antes.
        - As dimensões indicam o número de amostras e características presentes em cada conjunto.
        """)

def show_lane_predictions(model, x_train, df):
    """
    Visualiza as previsões de chance de vitória para cada lane.
    
    Cria uma interface com abas, uma para cada lane jogada pelo usuário,
    mostrando as chances de vitória previstas para diferentes campeões
    naquela lane específica.
    
    Parâmetros:
        model: Modelo Random Forest treinado
        x_train: Features de treino (para estrutura do modelo)
        df: DataFrame original com estatísticas das partidas
    """
    # Adiciona subtítulo na interface
    st.subheader("🤖 Previsão de Chances de Vitória por Lane")
    
    # Obtém previsões para campeões mais jogados em diferentes lanes
    results = predictByMostPlayed(model, x_train, df)
    
    # Obtém lista de lanes únicas jogadas pelo usuário
    lanes = df['role'].unique()
    
    # Cria uma aba para cada lane/posição
    # Converte códigos de role para nomes amigáveis usando ROLE_MAPPING
    lane_tabs = st.tabs([ROLE_MAPPING.get(lane, lane) for lane in lanes])
    
    # Itera sobre cada lane para preencher o conteúdo das abas
    for i, lane in enumerate(lanes):
        with lane_tabs[i]:
            # Adiciona subtítulo específico para a lane
            st.subheader(f"Previsões para a Lane: {ROLE_MAPPING.get(lane, lane)}")
            
            # Filtra resultados apenas para a lane atual
            lane_results = [r for r in results if r[1] == ROLE_MAPPING.get(lane, lane)]
            
            # Verifica se existem previsões para esta lane
            if lane_results:
                # Converte resultados para DataFrame para visualização
                lane_df = pd.DataFrame(lane_results, columns=["Campeão", "Role", "Chance de Vitória (%)"])
                
                # Cria gráfico de pizza para visualizar chances de vitória
                fig_lane = px.pie(
                    lane_df,
                    names="Campeão",                  # Nomes dos campeões
                    values="Chance de Vitória (%)",   # Valores das chances de vitória
                    title=f"Chances de Vitória - {ROLE_MAPPING.get(lane, lane)}",  # Título
                    color_discrete_sequence=px.colors.qualitative.Pastel  # Paleta de cores
                )
                
                # Personaliza o estilo do texto no gráfico
                fig_lane.update_traces(
                    textinfo='percent+label',               # Mostra porcentagem e rótulo
                    textfont=dict(size=18, family="Arial", color="black"),  # Estilo do texto
                    insidetextfont=dict(size=18, family="Arial", color="black")  # Estilo dentro das fatias
                )
                
                # Exibe o gráfico na interface
                st.plotly_chart(fig_lane)
            else:
                # Mensagem caso não haja previsões para esta lane
                st.write("Nenhuma previsão disponível para esta lane.")