import streamlit as st
from .queries import (
    save_fixed_account,
    get_fixed_accounts,
    update_fixed_account,
    delete_fixed_account,
)


def fixed_accounts_page():
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
