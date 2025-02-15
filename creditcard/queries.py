"""Módulo de interação com o banco de dados.

Este módulo é responsável por executar consultas e atualizações no banco de dados,
facilitando a interação com as tabelas de dados da aplicação.

Funcionalidades principais:
    - Execução de consultas SQL de leitura
    - Execução de comandos SQL de escrita (inserção, atualização, exclusão)

Dependências:
    - db.conn: Para obter as funções de conexão e execução de consultas (execute_query, execute_update)

Exceções:
    - Erros de execução de consultas
    - Erros de conexão com o banco de dados
"""

from db.conn import execute_query, execute_update


def save_credit_card(
    user_id, account_name, installments, installment_value, importance, due_date
):
    """Salva um novo cartão de crédito no banco de dados.

    Esta função insere um novo registro de cartão de crédito associado a um usuário.

    Args:
        user_id (int): ID do usuário ao qual o cartão está associado.
        account_name (str): Nome da conta do cartão de crédito.
        installments (int): Número de parcelas do cartão de crédito.
        installment_value (float): Valor de cada parcela.
        importance (str): Importância do cartão (descrição).
        due_date (datetime): Data de vencimento do cartão.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
        IntegrityError: Lança um erro se houver problemas de integridade.
    """
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
            due_date.strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )


def get_credit_cards(user_id):
    """Recupera os cartões de crédito associados a um usuário.

    Esta função executa uma consulta para obter todos os cartões de crédito
    registrados para um usuário específico.

    Args:
        user_id (int): ID do usuário cujos cartões de crédito devem ser recuperados.

    Returns:
        list: Lista de tuplas contendo as informações dos cartões de crédito.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
    """
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
    """Atualiza as informações de um cartão de crédito existente.

    Esta função modifica os detalhes de um cartão de crédito com base no ID fornecido.

    Args:
        card_id (int): ID do cartão de crédito a ser atualizado.
        account_name (str): Novo nome da conta do cartão de crédito.
        installments (int): Novo número de parcelas do cartão de crédito.
        installment_value (float): Novo valor de cada parcela.
        importance (str): Nova importância do cartão (descrição).
        due_date (datetime): Nova data de vencimento do cartão.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
        IntegrityError: Lança um erro se houver problemas de integridade.
    """
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
    """Exclui um cartão de crédito do banco de dados.

    Esta função remove um registro de cartão de crédito com base no ID fornecido.

    Args:
        card_id (int): ID do cartão de crédito a ser excluído.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
        IntegrityError: Lança um erro se houver problemas de integridade.
    """
    execute_update(
        "DELETE FROM cartoes_credito WHERE id = %s",
        (card_id,),
    )
