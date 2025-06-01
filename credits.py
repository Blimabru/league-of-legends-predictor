"""
Módulo de Créditos do League of Legends Predictor
-------------------------------------------------
Este módulo implementa a funcionalidade de exibição de créditos
e links para repositório do projeto.
"""

import streamlit as st

def show_credits_button():
    """
    Mostra o botão flutuante de créditos no canto inferior direito da tela.
    
    Retorna:
        bool: True se o botão foi clicado, False caso contrário
    """
    # CSS personalizado para o botão flutuante
    credit_btn_css = """
        <style>
        .stButton > button.credit-btn {
            position: fixed;         /* Fixa o botão na tela */
            bottom: 30px;            /* Posição a partir do fundo */
            right: 30px;             /* Posição a partir da direita */
            z-index: 9999;           /* Garante que fique por cima de outros elementos */
            background: #24292f;     /* Cor de fundo (GitHub escuro) */
            color: #fff;             /* Cor do texto */
            border: none;            /* Remove borda */
            border-radius: 50%;      /* Torna o botão circular */
            width: 56px;             /* Largura */
            height: 56px;            /* Altura */
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);  /* Sombra suave */
            font-size: 28px;         /* Tamanho do ícone */
            display: flex;           /* Layout flexbox */
            align-items: center;     /* Centraliza verticalmente */
            justify-content: center; /* Centraliza horizontalmente */
            transition: background 0.2s;  /* Efeito suave ao passar o mouse */
            padding: 0;              /* Remove padding interno */
        }
        .stButton > button.credit-btn:hover {
            background: #444950;     /* Cor ao passar o mouse */
            color: #fff;             /* Cor do texto ao passar o mouse */
        }
        </style>
    """
    
    # Aplica o CSS personalizado
    st.markdown(credit_btn_css, unsafe_allow_html=True)
    
    # Cria layout de duas colunas para posicionar o botão no lado direito
    col1, col2 = st.columns([0.95, 0.05])
    with col2:
        # Botão que alterna a visibilidade dos créditos
        return st.button("ⓘ", key="credit_btn", help="Créditos do Projeto", use_container_width=False)

def display_credits_if_active():
    """
    Exibe o conteúdo de créditos se estiver ativo no estado da sessão.
    """
    # Inicializa o estado se necessário
    if "show_credits" not in st.session_state:
        st.session_state["show_credits"] = False
    
    # Verifica se o botão foi clicado
    if show_credits_button():
        st.session_state["show_credits"] = not st.session_state["show_credits"]
    
    # Exibe créditos se estiverem ativos
    if st.session_state["show_credits"]:
        with st.expander("Créditos", expanded=True):
            # Conteúdo HTML formatado para os créditos
            st.markdown("""
            <div style="text-align:center;">
                <h3>Créditos</h3>
                <p>
                    Veja o código fonte no GitHub:<br>
                    <a href="https://github.com/Blimabru/league-of-legends-predictor" target="_blank" style="display:inline-block; margin-top:16px; text-decoration:none;">
                        <span style="display:flex; align-items:center; gap:8px; background:#24292f; color:#fff; padding:8px 18px; border-radius:8px; font-size:18px; font-family:Arial; font-weight:bold;">
                            <svg height="24" width="24" viewBox="0 0 16 16" fill="white" style="vertical-align:middle;">
                                <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38
                                0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52
                                -.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2
                                -3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64
                                -.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08
                                2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01
                                1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>
                            </svg>
                            GitHub
                        </span>
                    </a>
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Botão para fechar o expander de créditos
            if st.button("Fechar créditos", key="close_credits_btn"):
                st.session_state["show_credits"] = False
                st.rerun()  # Força a reexecução do app para atualizar a UI