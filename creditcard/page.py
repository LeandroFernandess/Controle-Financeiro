"""Módulo de gerenciamento de cartões de crédito utilizando Streamlit.

Este módulo fornece uma interface web para o gerenciamento de cartões de crédito,
permitindo a criação, visualização, atualização e exclusão de cartões para usuários logados.

Funcionalidades principais:
    - Criação de novos cartões de crédito
    - Visualização de cartões de crédito existentes
    - Atualização de informações dos cartões
    - Exclusão de cartões de crédito

Dependências:
    - streamlit: Para criação da interface web
    - datetime: Para manipulação de datas
    - .queries: Para operações de banco de dados (save_credit_card, get_credit_cards, update_credit_card, delete_credit_card)

Exceções:
    - Erros de validação para campos obrigatórios
    - Erros de sessão para usuários não logados
"""

import streamlit as st
from datetime import datetime
from .queries import (
    save_credit_card,
    get_credit_cards,
    update_credit_card,
    delete_credit_card,
)


def credit_card_page():
    """Gerencia a interface de gerenciamento de cartões de crédito.

    Exibe e controla:
        - Formulário para criação de novos lançamentos de cartões de crédito
        - Lista de lançamentos cadastrados
        - Funcionalidades de edição e exclusão de lançamentos

    Fluxo:
        1. Exibe título e formulário para novo lançamento
        2. Valida e salva o novo lançamento
        3. Recupera e exibe lançamentos existentes

    Componentes:
        - save_credit_card: Função para salvar um novo cartão de crédito
        - get_credit_cards: Função para recuperar lançamentos existentes
        - display_credit_cards: Função para exibir lançamentos cadastrados
    """
    user_id = st.session_state.get("user_id")

    st.markdown(
        """
        <h1 style='text-align: center;'>💳 Gerenciamento do cartão de crédito</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    with st.form("cartao_form"):
        st.subheader("Novo Lançamento")
        account_name = st.text_input("Nome da conta*")
        installments = st.number_input(
            "Número de Parcelas*", min_value=1, step=1, value=1
        )
        installment_value = st.number_input(
            "Valor de Cada Parcela (R$)*", min_value=0.01, step=0.01
        )
        importance = st.selectbox(
            "Importância*",
            ["Imprevisto", "Consumo próprio", "Necessário", "Lazer", "Outros"],
        )
        due_date = st.date_input("Data de Vencimento*", value=datetime.today())
        due_date = datetime.combine(due_date, datetime.min.time())

        submitted = st.form_submit_button("💳 Salvar Lançamento")

        if submitted:
            if not all([account_name, installments, installment_value]):
                st.error("Campos obrigatórios marcados com *")
            else:
                save_credit_card(
                    user_id,
                    account_name,
                    installments,
                    installment_value,
                    importance,
                    due_date,
                )
                st.session_state.pop("credit_cards", None)
                st.rerun()

    if "credit_cards" not in st.session_state:
        st.session_state.credit_cards = get_credit_cards(user_id)
    credit_cards = st.session_state.credit_cards

    display_credit_cards(credit_cards, user_id)


def display_credit_cards(credit_cards, user_id):
    """Exibe os lançamentos de cartões de crédito cadastrados.

    Esta função renderiza a lista de lançamentos de cartões de crédito
    e permite a edição e a exclusão de cada lançamento.

    Args:
        credit_cards (list): Lista de lançamentos de cartões de crédito a serem exibidos.
        user_id (int): ID do usuário associado aos lançamentos.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    st.divider()
    st.subheader("Lançamentos Cadastrados")

    if not credit_cards:
        st.info("Nenhum lançamento cadastrado ainda.")
        return

    for card in credit_cards:
        with st.container(border=True):
            editing = st.session_state.get(f"editing_{card[0]}", False)

            if editing:
                show_edit_form(card, user_id)
            else:
                show_card_info(card)


def show_card_info(card):
    """Exibe informações detalhadas de um lançamento de cartão de crédito.

    Esta função mostra o nome da conta, parcelas, valores totais,
    data de vencimento e permite a edição ou exclusão do lançamento.

    Args:
        card (tuple): Tupla contendo informações do lançamento do cartão de crédito.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    cols = st.columns([3, 2, 2, 2, 1.5])

    # Coluna 1: Nome e Data
    cols[0].write(f"**{card[1]}**")
    cols[0].caption(f"Criado em: {card[6].strftime('%d/%m/%Y')}")

    # Coluna 2: Parcelas
    cols[1].write(f"**Parcelas**\n{card[2]}x de R$ {card[3]:.2f}")

    # Coluna 3: Valores totais
    total = card[2] * card[3]
    cols[2].write(f"**Total**\nR$ {total:.2f}")

    # Coluna 4: Vencimento e Importância
    cols[3].write(f"**Vence na data {card[5].strftime('%d/%m/%Y')}**")
    cols[3].caption(f"Prioridade: {card[4]}")

    # Coluna 5: Ações
    action_col = cols[4]
    if action_col.button("✏️ Editar", key=f"edit_{card[0]}"):
        st.session_state[f"editing_{card[0]}"] = True
        st.rerun()

    if action_col.button("🗑️", key=f"del_{card[0]}"):
        delete_credit_card(card[0])
        st.session_state.pop("credit_cards", None)
        st.rerun()


def show_edit_form(card, user_id):
    """Renderiza um formulário para editar um lançamento de cartão de crédito.

    Esta função permite que o usuário modifique o nome da conta, número de parcelas,
    valor de cada parcela, importância e data de vencimento de um lançamento existente.

    Args:
        card (tuple): Tupla contendo informações do lançamento do cartão de crédito a ser editado.
        user_id (int): ID do usuário associado ao lançamento.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
    """
    with st.form(key=f"edit_form_{card[0]}"):
        st.subheader("Editar Lançamento")

        new_name = st.text_input("Nome do Cartão*", value=card[1])
        new_installments = st.number_input("Parcelas*", value=card[2], min_value=1)
        new_value = st.number_input(
            "Valor Parcela*", value=float(card[3]), min_value=0.01
        )
        new_importance = st.selectbox(
            "Importância*",
            ["Imprevisto", "Consumo próprio", "Necessário", "Lazer", "Outros"],
            index=[
                "Imprevisto",
                "Consumo próprio",
                "Necessário",
                "Lazer",
                "Outros",
            ].index(card[4]),
        )

        new_due_date = st.date_input("Data Vencimento*", value=card[5])
        new_due_date = datetime.combine(new_due_date, datetime.min.time())

        col1, col2, col3 = st.columns([2, 2, 4])
        if col1.form_submit_button("💾 Salvar"):
            update_credit_card(
                card_id=card[0],
                account_name=new_name,
                installments=new_installments,
                installment_value=new_value,
                importance=new_importance,
                due_date=new_due_date,
            )
            st.session_state[f"editing_{card[0]}"] = False
            st.session_state.pop("credit_cards", None)
            st.rerun()

        if col2.form_submit_button("❌ Cancelar"):
            st.session_state[f"editing_{card[0]}"] = False
            st.rerun()
