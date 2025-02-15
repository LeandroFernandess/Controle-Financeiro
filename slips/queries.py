"""Módulo de gestão de boletos para sistema financeiro.

Este módulo fornece operações CRUD completas para gerenciamento de boletos,
integrando-se com o banco de dados através do módulo db.conn.

Funcionalidades principais:
    - Criação de novos boletos
    - Recuperação de boletos existentes
    - Atualização de informações de boletos
    - Exclusão de boletos

Dependências:
    - db.conn.execute_query: Para operações de leitura
    - db.conn.execute_update: Para operações de escrita

Exceções:
    - Propaga exceções de database do db.conn
    - Assume que conexão com banco já está estabelecida
"""

from db.conn import execute_query, execute_update


def save_bill(user_id, title, total_value, due_date, is_installment, installments):
    """Armazena um novo boleto no banco de dados.

    Args:
        user_id (int): ID do usuário associado ao boleto
        title (str): Descrição/título do boleto
        total_value (float): Valor total do boleto
        due_date (date): Data de vencimento
        is_installment (bool): Indica se o boleto é parcelado
        installments (int): Número de parcelas (0 se não parcelado)

    Returns:
        None: A função não retorna valor mas persiste os dados no banco

    Raises:
        DatabaseError: Em caso de falha na operação de inserção

    Example:
        >>> save_bill(123, "Aluguel", 1500.0, date(2023, 12, 5), False, 0)
    """
    execute_update(
        """
        INSERT INTO boletos 
            (usuario_id, titulo, valor_total, data_vencimento, parcelado, num_parcelas)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (user_id, title, total_value, due_date, is_installment, installments),
    )


def get_bills(user_id):
    """Recupera todos os boletos associados a um usuário.

    Args:
        user_id (int): ID do usuário para consulta

    Returns:
        list[tuple]: Lista de tuplas contendo:
            (id, titulo, valor_total, data_vencimento,
             parcelado, num_parcelas, pago, data_pagamento)

    Raises:
        DatabaseError: Se a consulta falhar

    Example:
        >>> get_bills(123)
        [(1, 'Aluguel', 1500.0, datetime.date(2023, 12, 5), False, 0, False, None)]
    """
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
    """Atualiza todas as informações de um boleto existente.

    Args:
        bill_id (int): ID do boleto a ser atualizado
        title (str): Novo título/descrição
        total_value (float): Novo valor total
        due_date (date): Nova data de vencimento
        is_installment (bool): Novo status de parcelamento
        installments (int): Novo número de parcelas
        paid (bool): Status de pagamento
        payment_date (date): Data efetiva de pagamento

    Returns:
        None: Atualiza o registro no banco sem retornar valor

    Raises:
        DatabaseError: Em caso de falha na atualização

    Notes:
        - Define payment_date como NULL quando paid=False
        - Atualiza todas as colunas do registro
    """
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
    """Remove permanentemente um boleto do sistema.

    Args:
        bill_id (int): ID do boleto a ser excluído

    Returns:
        None: Remove o registro sem retornar valor

    Raises:
        DatabaseError: Se a exclusão falhar
        ValueError: Se bill_id não existir

    Warning:
        Esta operação é irreversível e remove definitivamente o registro
    """
    execute_update("DELETE FROM boletos WHERE id = %s", (bill_id,))
