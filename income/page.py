import streamlit as st
import pytz
from .queries import (
    get_existing_income,
    save_income,
)


def income_page():

    if not st.session_state.get("logged_in"):
        st.error("⚠️ Por favor, faça login para acessar esta página.")
        return

    user_id = st.session_state.get("user_id")

    st.markdown(
        """
        <h1 style='text-align: center;'>💵 Gerenciamento de Renda Mensal</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    # Verifica se os dados da renda já estão armazenados na sessão
    if "existing_income" not in st.session_state:
        existing_income = get_existing_income(user_id)
        st.session_state.existing_income = existing_income
    else:
        existing_income = st.session_state.existing_income

    with st.form("income_form"):
        if existing_income:
            current_value = float(existing_income[0][0])
            last_update = (
                existing_income[0][1]
                .astimezone(pytz.timezone("America/Sao_Paulo"))
                .strftime("%d/%m/%Y %H:%M")
            )

            st.markdown(
                f"**Renda Atual:** R$ {current_value:,.2f}  \n"
                f"*Última atualização: {last_update}*"
            )

            new_income = st.number_input(
                "Nova Renda Mensal",
                value=current_value,
                min_value=0.0,
                step=100.0,
                format="%.2f",
            )
        else:
            new_income = st.number_input(
                "Insira sua Renda Mensal", min_value=0.0, step=100.0, format="%.2f"
            )

        submitted = st.form_submit_button("💾 Salvar Renda")

        if submitted:
            try:
                save_income(user_id, new_income)
                st.success("✅ Renda atualizada com sucesso!")
                st.session_state.existing_income = get_existing_income(user_id)
                st.rerun()
            except Exception as e:
                st.error(f"❌ Erro ao salvar renda: {e}")
