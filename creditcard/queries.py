from db.conn import execute_query, execute_update


def save_credit_card(
    user_id, account_name, installments, installment_value, importance, due_date
):
    execute_update(
        """
        INSERT INTO cartoes_credito 
            (usuario_id, nome_conta, num_parcelas, valor_parcela, importancia,
             dia_vencimento, data_criacao)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """,
        (
            user_id,
            account_name,
            installments,
            installment_value,
            importance,
            due_date.strftime("%Y-%m-%d %H:%M:%S"),  # Formato adequado para TIMESTAMP
        ),
    )


def get_credit_cards(user_id):

    return execute_query(
        """SELECT id, nome_conta, num_parcelas, valor_parcela, 
                  importancia, dia_vencimento, data_criacao 
           FROM cartoes_credito 
           WHERE usuario_id = %s""",
        (user_id,),
    )


def update_credit_card(
    card_id, account_name, installments, installment_value, importance, due_date
):

    execute_update(
        """
        UPDATE cartoes_credito SET
            nome_conta = %s,
            num_parcelas = %s,
            valor_parcela = %s,
            importancia = %s,
            dia_vencimento = %s
        WHERE id = %s
        """,
        (
            account_name,
            installments,
            installment_value,
            importance,
            due_date.strftime("%Y-%m-%d"),
            card_id,
        ),
    )


def delete_credit_card(card_id):

    execute_update(
        "DELETE FROM cartoes_credito WHERE id = %s",
        (card_id,),
    )
