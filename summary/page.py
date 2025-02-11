import streamlit as st
from datetime import datetime
from .queries import search_user_info


def summary_page():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não autenticado. Por favor, faça login.")
        return

    # Centralizar o título com HTML e CSS
    st.markdown(
        """
        <h1 style='text-align: center;'>💰 Visão Geral</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    # Seletor de mês e ano
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", range(1, 13), index=mes_atual - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2000, max_value=2100, value=ano_atual)

    # Botão de alternância para mostrar/ocultar valores
    mostrar_valores = st.checkbox("👁️ Mostrar valores", value=False)

    # Adiciona o botão de atualizar
    if st.button("Atualizar Dados"):
        st.session_state.pop("dados_financeiros", None)
        dados = search_user_info(user_id, mes, ano)
        st.session_state.dados_financeiros = dados
    else:
        # Verifica se os dados já estão armazenados na sessão
        if "dados_financeiros" not in st.session_state:
            dados = search_user_info(user_id, mes, ano)
            st.session_state.dados_financeiros = dados
        else:
            dados = st.session_state.dados_financeiros

    # Função para formatar os valores (mostrar ou ocultar)
    def formatar_valor(valor):
        return f"R$ {valor:.2f}" if mostrar_valores else "***"

    # Exibir métricas principais com emojis
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Renda Mensal", formatar_valor(dados["renda_mensal"]))
    with col2:
        total_gastos = (
            dados["gastos_cartao"]
            + dados["gastos_boletos"]
            + dados["gastos_contas_fixas"]
        )
        st.metric("💸 Total de Gastos", formatar_valor(total_gastos))
    with col3:
        saldo_restante = dados["renda_mensal"] - total_gastos
        st.metric("💹 Saldo Restante", formatar_valor(saldo_restante))

    # Detalhamento dos gastos com emojis
    st.subheader("📉 Detalhamento dos Gastos")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("💳 **Cartão de Crédito**")
        st.write(formatar_valor(dados["gastos_cartao"]))
    with col2:
        st.write("📄 **Boletos**")
        st.write(formatar_valor(dados["gastos_boletos"]))
    with col3:
        st.write("🏠 **Contas Fixas**")
        st.write(formatar_valor(dados["gastos_contas_fixas"]))

    # Mensagem adicional com emojis
    st.markdown("---")
    if saldo_restante > 0:
        st.success("🎉 Você está dentro do orçamento!")
    else:
        st.error(
            "⚠️ Atenção! Você está gastando mais do que sua renda. Considere revisar seus gastos."
        )
