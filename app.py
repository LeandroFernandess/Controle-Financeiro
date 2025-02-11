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
    st.sidebar.title("Sistema do Usuário")
    menu = st.sidebar.selectbox("Menu", ["Login", "Cadastro", "Redefinir Senha"])

    if menu == "Login":
        login_page()
    elif menu == "Cadastro":
        create_user_page()
    elif menu == "Redefinir Senha":
        forgot_password_page()


def logged():
    """Exibe a página principal após o login do usuário."""

    # Sidebar para navegação dentro do dashboard
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

    # Adicione o botão "Sair" no rodapé da sidebar
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


# Controle do estado de login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    logged()
else:
    main()
