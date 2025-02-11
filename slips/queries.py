from db.conn import execute_query, execute_update


def save_bill(user_id, title, total_value, due_date, is_installment, installments):

    execute_update(
        """
        INSERT INTO boletos 
            (usuario_id, titulo, valor_total, data_vencimento, parcelado, num_parcelas)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, title, total_value, due_date, is_installment, installments),
    )


def get_bills(user_id):

    return execute_query(
        """SELECT id, titulo, valor_total, data_vencimento, 
                  parcelado, num_parcelas, pago, data_pagamento 
           FROM boletos WHERE usuario_id = %s""",
        (user_id,),
    )


def update_bill(
    bill_id,
    title,
    total_value,
    due_date,
    is_installment,
    installments,
    paid,
    payment_date,
):

    execute_update(
        """
        UPDATE boletos SET
            titulo = %s,
            valor_total = %s,
            data_vencimento = %s,
            parcelado = %s,
            num_parcelas = %s,
            pago = %s,
            data_pagamento = %s
        WHERE id = %s
        """,
        (
            title,
            total_value,
            due_date,
            is_installment,
            installments,
            paid,
            payment_date,
            bill_id,
        ),
    )


def delete_bill(bill_id):

    execute_update("DELETE FROM boletos WHERE id = %s", (bill_id,))
