"""Módulo de gerenciamento de renda para aplicação Streamlit.

Este módulo é responsável por interagir com a funcionalidade de renda mensal
dentro da aplicação, permitindo a recuperação e atualização de informações de renda.

Componentes principais:
    - get_existing_income: Função para recuperar a renda atual do usuário
    - save_income: Função para salvar ou atualizar a renda do usuário

Módulos integrados:
    - streamlit: Para a construção da interface do usuário
    - pytz: Para manipulação de fusos horários

Funcionalidades:
    - Visualização da renda mensal atual
    - Atualização da renda mensal conforme as entradas do usuário

Fluxo da aplicação:
    1. Importar funções necessárias para manipulação de renda
    2. Interagir com a interface do Streamlit para gerenciar a renda do usuário
"""

import streamlit as st
import pytz
from .queries import (
    get_existing_income,
    save_income,
)


def income_page():
    """Renderiza a página de gerenciamento de renda mensal.

    Esta função exibe uma interface para o usuário gerenciar sua renda mensal.
    O usuário deve estar logado para acessar esta página. A função permite
    visualizar a renda atual e atualizar o valor da renda.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.

    Raises:
        Erros de sessão: Exibe mensagem de erro se o usuário não estiver logado.
        Exceções ao salvar: Mostra mensagem de erro se ocorrer um problema ao salvar a renda.

    Example:
        >>> income_page()
    """

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
