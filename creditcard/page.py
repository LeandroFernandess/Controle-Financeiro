import streamlit as st
from datetime import datetime
from .queries import (
    save_credit_card,
    get_credit_cards,
    update_credit_card,
    delete_credit_card,
)


def credit_card_page():

    user_id = st.session_state.get("user_id")  # Obtém o user_id da sessão

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
        # Na função credit_card_page
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

    # Verifica se os lançamentos já estão armazenados na sessão
    if "credit_cards" not in st.session_state:
        st.session_state.credit_cards = get_credit_cards(user_id)
    credit_cards = st.session_state.credit_cards

    # Passa o user_id para a função display_credit_cards
    display_credit_cards(credit_cards, user_id)


def display_credit_cards(credit_cards, user_id):

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

        # Na função show_edit_form
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
