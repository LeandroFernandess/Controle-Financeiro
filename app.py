"""Aplicação principal para gestão financeira pessoal.

Este módulo constitui o ponto de entrada do sistema, responsável por:
- Configurar a aplicação Streamlit
- Gerenciar o estado de autenticação do usuário
- Coordenar a navegação entre diferentes módulos
- Controlar o ciclo de vida da sessão

Componentes principais:
    - main: Interface de autenticação (login/cadastro)
    - logged: Dashboard principal pós-login
    - Controle de estado via st.session_state

Módulos integrados:
    - auth: Gerenciamento de usuários e autenticação
    - creditcard: Gestão de cartões de crédito
    - slips: Controle de boletos
    - income: Gerenciamento de renda
    - fixedaccounts: Contas fixas recorrentes
    - summary: Visão geral consolidada

Fluxo da aplicação:
    1. Configuração inicial da página
    2. Verificação do estado de login
    3. Redirecionamento para interface adequada
    4. Gerenciamento de navegação e sessão
"""

import streamlit as st
from auth.page import *
from creditcard.page import *
from slips.page import *
from income.page import *
from fixedaccounts.page import *
from summary.page import *


st.set_page_config(
    page_title="Gestão financeira",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    """Gerencia a interface de autenticação e registro de usuários.

    Exibe e controla:
        - Menu lateral com opções de login/cadastro/redefinição de senha
        - Páginas correspondentes à seleção do usuário
        - Transições entre estados de autenticação

    Fluxo:
        1. Exibe menu lateral com opções de autenticação
        2. Carrega módulo correspondente à seleção
        3. Mantém estado até autenticação bem-sucedida

    Componentes:
        - login_page: Formulário de autenticação
        - create_user_page: Formulário de cadastro
        - forgot_password_page: Recuperação de credenciais
    """
    st.sidebar.title("Sistema do Usuário")
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro", "Redefinir Senha"])

    if menu == "Login":
        login_page()
    elif menu == "Cadastro":
        create_user_page()
    elif menu == "Redefinir Senha":
        forgot_password_page()


def logged():
    """Gerencia o dashboard principal pós-autenticação.

    Funcionalidades:
        - Exibe menu de navegação entre módulos
        - Controla logout do usuário
        - Gerencia carregamento dos módulos específicos
        - Mantém estado consistente da sessão

    Seções:
        - Resumo: Visão consolidada (summary_page)
        - Cartões de Crédito: Gestão de faturas (credit_card_page)
        - Boletos: Controle de pagamentos (slips_page)
        - Contas fixas: Despesas recorrentes (fixed_accounts_page)
        - Renda: Gerenciamento de receitas (income_page)

    Comportamentos:
        - Atualiza interface ao alterar seleção no menu
        - Reinicia estado ao efetuar logout
        - Mantém sessão ativa até logout explícito
    """

    st.sidebar.title("Opções de Navegação")
    dashboard_menu = st.sidebar.selectbox(
        "Selecione uma opção",
        [
            "Resumo",
            "Cartões de Crédito",
            "Boletos",
            "Contas fixas",
            "Renda",
        ],
    )

    if st.sidebar.button("Sair"):
        st.session_state["logged_in"] = False
        st.rerun()

    if dashboard_menu == "Resumo":
        summary_page()
    elif dashboard_menu == "Cartões de Crédito":
        credit_card_page()
    elif dashboard_menu == "Boletos":
        slips_page()
    elif dashboard_menu == "Contas fixas":
        fixed_accounts_page()
    elif dashboard_menu == "Renda":
        income_page()


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    logged()
else:
    main()
