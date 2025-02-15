"""Módulo de gerenciamento de contas fixas para aplicação Streamlit.

Este módulo é responsável por interagir com as funcionalidades de contas fixas
dentro da aplicação, permitindo a recuperação, atualização e exclusão de contas fixas.

Componentes principais:
    - save_fixed_account: Função para salvar uma nova conta fixa ou atualizar uma existente
    - get_fixed_accounts: Função para recuperar as contas fixas do usuário
    - update_fixed_account: Função para atualizar uma conta fixa específica
    - delete_fixed_account: Função para excluir uma conta fixa

Módulos integrados:
    - streamlit: Para a construção da interface do usuário

Funcionalidades:
    - Visualização das contas fixas cadastradas
    - Criação, edição e exclusão de contas fixas conforme as entradas do usuário

Fluxo da aplicação:
    1. Importar funções necessárias para manipulação de contas fixas
    2. Interagir com a interface do Streamlit para gerenciar contas fixas do usuário
"""

import streamlit as st
from .queries import (
    save_fixed_account,
    get_fixed_accounts,
    update_fixed_account,
    delete_fixed_account,
)


def fixed_accounts_page():
    """Gerencia a interface de gerenciamento de contas fixas.

    Exibe e controla:
        - Formulário para criação de novas contas fixas
        - Lista de contas fixas cadastradas
        - Funcionalidades de edição e exclusão de contas fixas

    Fluxo:
        1. Exibe título e formulário para nova conta fixa
        2. Valida e salva a nova conta fixa
        3. Recupera e exibe contas fixas existentes

    Componentes:
        - save_fixed_account: Função para salvar uma nova conta fixa
        - get_fixed_accounts: Função para recuperar contas fixas existentes
        - display_fixed_accounts: Função para exibir contas cadastradas
    """
    user_id = st.session_state.get("user_id")

    st.markdown(
        """
        <h1 style='text-align: center;'>📄 Gerenciamento de contas fixas</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    with st.form("account_form"):
        st.subheader("Nova Conta Fixa")
        title = st.text_input("Título da Conta*")
        total_value = st.number_input("Valor Mensal (R$)*", min_value=0.01, step=0.01)

        if st.form_submit_button("📤 Salvar Conta"):
            if not all([title, total_value]):
                st.error("Campos obrigatórios marcados com *")
            else:
                try:
                    save_fixed_account(user_id, title, total_value)
                    st.success("Conta fixa salva com sucesso!")
                    st.session_state.pop("accounts", None)
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao salvar a conta fixa: {e}")

    if "accounts" not in st.session_state:
        st.session_state.accounts = get_fixed_accounts(user_id)
    accounts = st.session_state.accounts

    display_fixed_accounts(accounts)


def display_fixed_accounts(accounts):
    """Exibe as contas fixas cadastradas.

    Esta função renderiza a lista de contas fixas e permite a edição e exclusão
    de cada conta.

    Args:
        accounts (list): Lista de contas fixas a serem exibidas.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    st.divider()
    st.subheader("Contas Cadastradas")

    if not accounts:
        st.info("Nenhuma conta cadastrada ainda.")
        return

    for account in accounts:
        with st.container(border=True):
            editing = st.session_state.get(f"editing_{account[0]}", False)
            show_account_editor(account) if editing else show_account_info(account)


def show_account_info(account):
    """Exibe informações detalhadas de uma conta fixa.

    Esta função mostra o título e o valor mensal de uma conta fixa, além
    de permitir a edição e a exclusão da conta.

    Args:
        account (tuple): Tupla contendo informações da conta fixa.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    cols = st.columns([3, 2, 2, 1.5])

    cols[0].write(f"**{account[1]}**")
    cols[1].write(f"**Valor Mensal**\nR$ {account[2]:.2f}")

    if cols[3].button("✏️ Editar", key=f"edit_{account[0]}"):
        st.session_state[f"editing_{account[0]}"] = True
        st.rerun()

    if cols[3].button("🗑️", key=f"del_{account[0]}"):
        try:
            delete_fixed_account(account[0])
            st.success("Conta fixa deletada com sucesso!")
            st.session_state.pop("accounts", None)
            st.rerun()
        except Exception as e:
            st.error(f"Erro ao deletar a conta fixa: {e}")


def show_account_editor(account):
    """Renderiza um formulário para editar uma conta fixa.

    Esta função permite ao usuário modificar o título e o valor mensal
    de uma conta fixa existente.

    Args:
        account (tuple): Tupla contendo informações da conta fixa a ser editada.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    with st.form(key=f"edit_form_{account[0]}"):
        st.subheader("Editar Conta Fixa")

        new_title = st.text_input("Título*", value=account[1])
        new_value = st.number_input(
            "Valor Mensal (R$)*", value=float(account[2]), min_value=0.01, step=0.01
        )

        col1, col2, _ = st.columns([2, 2, 4])
        if col1.form_submit_button("💾 Salvar"):
            try:
                update_fixed_account(account[0], new_title, new_value)
                st.success("Conta fixa atualizada com sucesso!")
                st.session_state[f"editing_{account[0]}"] = False
                st.session_state.pop("accounts", None)
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao atualizar a conta fixa: {e}")

        if col2.form_submit_button("❌ Cancelar"):
            st.session_state[f"editing_{account[0]}"] = False
            st.rerun()
