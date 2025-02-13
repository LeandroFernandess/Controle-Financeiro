import streamlit as st
from datetime import datetime, timedelta
from .queries import save_bill, get_bills, update_bill, delete_bill


def slips_page():

    user_id = st.session_state.get("user_id")

    if not user_id:
        st.error("Usuário não logado!")
        return

    st.markdown(
        """
        <h1 style='text-align: center;'> 🧾 Gerenciamento de Boletos</h1>
        <hr>
        """,
        unsafe_allow_html=True,
    )

    # Estado do parcelamento
    if "installment" not in st.session_state:
        st.session_state.installment = False

    # Botões de controle
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💰 Parcelado", use_container_width=True):
            st.session_state.installment = True
    with col2:
        if st.button("💵 À Vista", use_container_width=True):
            st.session_state.installment = False

    # Formulário principal
    with st.form("bill_form"):
        st.subheader("Novo Boleto")
        title = st.text_input("Título do Boleto*")
        total_value = st.number_input("Valor Total (R$)*", min_value=0.01, step=0.01)

        due_date = st.date_input(
            "Data de Vencimento*",
            format="DD/MM/YYYY",
            min_value=datetime.today().date(),
            value=datetime.today().date() + timedelta(days=5),
        )

        installments = None
        if st.session_state.installment:
            installments = st.number_input(
                "Número de Parcelas*", min_value=2, step=1, key="installments_input"
            )

        if st.form_submit_button("📤 Salvar Boleto"):
            if not all([title, total_value, due_date]):
                st.error("Campos obrigatórios marcados com *")
            else:
                if st.session_state.installment and not installments:
                    st.error("Informe o número de parcelas!")
                else:
                    save_bill(
                        user_id,
                        title,
                        total_value,
                        due_date,
                        st.session_state.installment,
                        installments,
                    )
                    st.session_state.installment = False
                    st.session_state.pop("bills", None)
                    st.rerun()

    # Inicializa a variável bills com um valor padrão
    bills = []

    # Verifica se os dados já estão armazenados na sessão
    if "bills" not in st.session_state:
        st.session_state.bills = get_bills(user_id)
    bills = st.session_state.bills

    display_bills(bills)


def display_bills(bills):

    st.divider()
    st.subheader("Boletos Cadastrados")

    if not bills:
        st.info("Nenhum boleto cadastrado ainda.")
        return

    for bill in bills:
        with st.container(border=True):
            if st.session_state.get(f"editing_{bill[0]}", False):
                show_edit_form(bill)
            else:
                show_bill_info(bill)


def show_bill_info(bill):

    cols = st.columns([3, 2, 2, 2, 2, 1.5])

    # Coluna 1: Informações básicas
    cols[0].write(f"**{bill[1]}**")
    cols[0].caption(f"Vencimento: {bill[3].strftime('%d/%m/%Y')}")

    # Converta bill[3] para datetime.date antes da comparação
    if not bill[6] and bill[3].date() < datetime.today().date():
        cols[0].error("⚠️ Vencido!")

    # Coluna 2: Valores
    cols[1].write(f"**Valor Total**\nR$ {bill[2]:.2f}")

    # Coluna 3: Parcelamento
    if bill[4]:
        installment_value = bill[2] / bill[5]
        cols[2].write(f"**Parcelado em**\n{bill[5]}x de R$ {installment_value:.2f}")
    else:
        cols[2].write("**Pagamento**\nÀ vista")

    # Coluna 4: Status
    status = "✅ Pago" if bill[6] else "❌ Pendente"
    cols[3].write(f"**Status**\n{status}")

    # Coluna 5: Dias restantes
    days_remaining = (
        bill[3] - datetime.today()
    ).days  # Pode deixar bill[3] como datetime
    status_text = (
        f"{days_remaining} dias"
        if days_remaining >= 0
        else f"Atraso: {abs(days_remaining)} dias"
    )
    cols[4].write(f"**Situação**\n{status_text}")

    # Coluna 6: Ações
    action_col = cols[5]
    if bill[6]:
        if action_col.button("🗑️", key=f"del_{bill[0]}"):
            delete_bill(bill[0])
            st.session_state.pop("bills", None)
            st.rerun()
    else:
        if action_col.button("✏️ Editar", key=f"edit_{bill[0]}"):
            st.session_state[f"editing_{bill[0]}"] = True
            st.rerun()


def show_edit_form(bill):
    with st.form(key=f"edit_form_{bill[0]}"):
        st.subheader("Editar Boleto")

        # Converter para objeto date se necessário
        existing_due_date = bill[3].date() if isinstance(bill[3], datetime) else bill[3]
        current_date = datetime.today().date()

        new_title = st.text_input("Título*", value=bill[1])
        new_total = st.number_input(
            "Valor Total (R$)*", value=float(bill[2]), min_value=0.01, step=0.01
        )

        # Ajustar min_value para permitir a data original
        new_due_date = st.date_input(
            "Data de Vencimento*",
            value=existing_due_date,
            format="DD/MM/YYYY",
            min_value=min(existing_due_date, current_date),
            max_value=current_date + timedelta(days=365 * 10),  # 10 anos à frente
        )

        new_installment = st.toggle("Parcelado", value=bill[4])

        new_installments = bill[5]
        if new_installment:
            new_installments = st.number_input(
                "Número de Parcelas*",
                value=bill[5] if bill[5] else 2,
                min_value=2,
                step=1,
            )

        new_paid = st.toggle("Marcar como pago", value=bill[6])

        payment_date = st.date_input(
            "Data de Pagamento",
            format="DD/MM/YYYY",
            value=bill[7].date() if len(bill) > 7 and bill[7] else current_date,
            max_value=current_date,
        )

        col1, col2, _ = st.columns([2, 2, 4])
        if col1.form_submit_button("💾 Salvar"):
            update_bill(
                bill[0],
                new_title,
                new_total,
                new_due_date,
                new_installment,
                new_installments,
                new_paid,
                payment_date,
            )
            st.session_state[f"editing_{bill[0]}"] = False
            st.session_state.pop("bills", None)
            st.rerun()

        if col2.form_submit_button("❌ Cancelar"):
            st.session_state[f"editing_{bill[0]}"] = False
            st.rerun()
