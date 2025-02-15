"""Módulo de conexão e registro de log para a aplicação.

Este módulo é responsável por gerenciar a conexão com o banco de dados
e registrar eventos e erros ocorridos durante a execução da aplicação.

Componentes principais:
    - execute_query: Função para executar consultas SQL no banco de dados
    - get_connection: Função para estabelecer e retornar a conexão com o banco de dados
    - logging: Módulo para registrar logs de eventos e erros

Funcionalidades:
    - Estabelecer conexão com o banco de dados
    - Executar consultas SQL de leitura
    - Registrar mensagens de log para monitoramento e depuração

Fluxo da aplicação:
    1. Importar funções necessárias para manipulação de banco de dados
    2. Configurar e utilizar o sistema de logging
"""

from db.conn import execute_query, get_connection
import logging

# Configura o logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def execute_non_query(query, params=None):
    """Executa uma consulta que não espera resultados.

    Esta função executa comandos SQL que não retornam dados (como INSERT, UPDATE, DELETE)
    e gerencia transações, garantindo que as alterações sejam confirmadas ou revertidas
    em caso de erro.

    Fluxo:
        1. Estabelece conexão com o banco de dados
        2. Executa a consulta SQL fornecida
        3. Comita as alterações ou reverte em caso de erro

    Exceções:
        - Registra erros de execução e reverte a transação em caso de falha.

    Args:
        query (str): Consulta SQL a ser executada.
        params (tuple, optional): Parâmetros da consulta. Padrão é None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()
    except Exception as e:
        logger.error(f"Erro durante a execução da consulta: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def save_fixed_account(user_id, title, total_value):
    """Salva uma nova conta fixa no banco de dados.

    Esta função insere uma nova conta fixa associada a um usuário.

    Args:
        user_id (int): ID do usuário ao qual a conta está associada.
        title (str): Título da conta fixa.
        total_value (float): Valor total da conta fixa.

    Exemplo:
        >>> save_fixed_account(1, "Aluguel", 1200.00)
    """
    insert_query = """
        INSERT INTO contas_fixas (usuario_id, titulo, valor_total)
        VALUES (%s, %s, %s)
    """
    execute_non_query(insert_query, (user_id, title, total_value))


def update_fixed_account(account_id, title, total_value):
    """Atualiza os detalhes de uma conta fixa existente.

    Esta função modifica o título e o valor total de uma conta fixa existente.

    Args:
        account_id (int): ID da conta fixa a ser atualizada.
        title (str): Novo título da conta fixa.
        total_value (float): Novo valor total da conta fixa.

    Exemplo:
        >>> update_fixed_account(1, "Aluguel Atualizado", 1300.00)
    """
    update_query = """
        UPDATE contas_fixas SET
            titulo = %s,
            valor_total = %s
        WHERE id = %s
    """
    execute_non_query(update_query, (title, total_value, account_id))


def delete_fixed_account(account_id):
    """Exclui uma conta fixa do banco de dados.

    Esta função remove uma conta fixa com base no ID fornecido.

    Args:
        account_id (int): ID da conta fixa a ser excluída.

    Exemplo:
        >>> delete_fixed_account(1)
    """
    delete_query = "DELETE FROM contas_fixas WHERE id = %s"
    execute_non_query(delete_query, (account_id,))


def get_fixed_accounts(user_id):
    """Recupera as contas fixas associadas a um usuário.

    Esta função retorna uma lista de contas fixas de um usuário específico.

    Args:
        user_id (int): ID do usuário cujas contas fixas devem ser recuperadas.

    Returns:
        list: Lista de tuplas contendo ID, título e valor total das contas fixas.

    Exemplo:
        >>> accounts = get_fixed_accounts(1)
    """
    query = """
        SELECT id, titulo, valor_total
        FROM contas_fixas
        WHERE usuario_id = %s
    """
    return execute_query(query, (user_id,))
