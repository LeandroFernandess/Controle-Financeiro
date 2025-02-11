from db.conn import execute_query, execute_update


def get_existing_income(user_id):

    return execute_query(
        "SELECT valor, data_atualizacao FROM Renda WHERE user_id = %s;", (user_id,)
    )


def save_income(user_id, new_income):

    execute_update(
        """
        INSERT INTO Renda (user_id, valor)
        VALUES (%s, %s)
        ON CONFLICT (user_id) DO UPDATE
        SET valor = EXCLUDED.valor,
            data_atualizacao = CURRENT_TIMESTAMP AT TIME ZONE 'America/Sao_Paulo';
        """,
        (user_id, new_income),
    )
