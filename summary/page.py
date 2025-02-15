"""Módulo de visão geral financeira para aplicativo Streamlit.

Este módulo fornece uma interface interativa para análise financeira pessoal,
exibindo informações consolidadas sobre renda, gastos e saldo do usuário.
Integra-se com o sistema de autenticação e banco de dados através do módulo queries.

Componentes principais:
    - summary_page: Função principal que estrutura a página e lógica de exibição
    - formatar_valor: Função auxiliar para formatação condicional de valores

Funcionalidades:
    * Visualização de dados financeiros por período específico
    * Controle de privacidade para ocultar valores sensíveis
    * Atualização manual de dados em tempo real
    * Alertas automáticos sobre situação financeira
    * Detalhamento de gastos por categorias
"""

import streamlit as st
from datetime import datetime
from .queries import search_user_info


def summary_page():
    """Exibe e gerencia a página de visão geral financeira do usuário.

    Esta função cria a interface completa da página de resumo financeiro, incluindo:
    - Verificação de autenticação do usuário
    - Controles de seleção de período (mês/ano)
    - Sistema de ocultação de valores sensíveis
    - Atualização e cache de dados financeiros
    - Exibição de métricas e gráficos consolidados
    - Alertas contextuais sobre saúde financeira

    Processo:
        1. Verifica autenticação via session_state
        2. Configura layout da página e controles interativos
        3. Recupera/atualiza dados do banco de dados
        4. Calcula métricas e prepara visualizações
        5. Exibe resultados com formatação condicional

    Requer:
        - Sessão ativa com user_id válido em st.session_state
        - Módulo queries com função search_user_info operacional

    Side effects:
        - Modifica st.session_state.dados_financeiros para cache
        - Exibe diversos elementos na interface via Streamlit
        - Realiza consultas ao banco de dados através de search_user_info

    Mensagens:
        - Erro de autenticação se usuário não logado
        - Alerta positivo/negativo conforme saldo restante
    """

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não autenticado. Por favor, faça login.")
        return

    st.markdown(
        """
        <h1 style='text-align: center;'>💰 Visão Geral</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    mes_atual = datetime.now().month
    ano_atual = datetime.now().year

    col1, col2 = st.columns(2)
    with col1:
        mes = st.selectbox("Mês", range(1, 13), index=mes_atual - 1)
    with col2:
        ano = st.number_input("Ano", min_value=2000, max_value=2100, value=ano_atual)

    mostrar_valores = st.checkbox("👁️ Mostrar valores", value=False)

    if st.button("Atualizar Dados"):
        st.session_state.pop("dados_financeiros", None)
        dados = search_user_info(user_id, mes, ano)
        st.session_state.dados_financeiros = dados
    else:
        dados = st.session_state.get("dados_financeiros") or search_user_info(
            user_id, mes, ano
        )
        st.session_state.dados_financeiros = dados

    def formatar_valor(valor):
        """Formata valores financeiros com controle de visibilidade.

        Args:
            valor (float): Valor numérico a ser formatado

        Returns:
            str: Valor monetário formatado (R$ X.XX) ou máscara (***) conforme
                o estado da checkbox 'mostrar_valores'

        Exemplos:
            >>> formatar_valor(1500.5) # Com mostrar_valores=True
            'R$ 1500.50'
            >>> formatar_valor(1500.5) # Com mostrar_valores=False
            '***'
        """
        return f"R$ {valor:.2f}" if mostrar_valores else "***"

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

    st.markdown("---")
    if saldo_restante > 0:
        st.success("🎉 Você está dentro do orçamento!")
    elif saldo_restante < 0:
        st.error(
            "⚠️ Atenção! Você está gastando mais do que sua renda. Considere revisar seus gastos."
        )
