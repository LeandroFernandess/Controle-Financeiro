from db.conn import execute_query, execute_update, get_connection
import logging

# Configura o logger
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def execute_non_query(query, params=None):
    """Executa uma consulta que não espera resultados."""
    conn = get_connection()  # Você deve implementar ou importar essa função
    cursor = conn.cursor()
    try:
        cursor.execute(query, params)
        conn.commit()  # Para operações DML
    except Exception as e:
        logger.error(f"Erro durante a execução da consulta: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def save_fixed_account(user_id, title, total_value):
    insert_query = """
        INSERT INTO contas_fixas (usuario_id, titulo, valor_total)
        VALUES (%s, %s, %s)
    """
    execute_non_query(insert_query, (user_id, title, total_value))


def update_fixed_account(account_id, title, total_value):
    update_query = """
        UPDATE contas_fixas SET
            titulo = %s,
            valor_total = %s
        WHERE id = %s
    """
    execute_non_query(update_query, (title, total_value, account_id))


def delete_fixed_account(account_id):
    delete_query = "DELETE FROM contas_fixas WHERE id = %s"
    execute_non_query(delete_query, (account_id,))


def get_fixed_accounts(user_id):
    query = """
        SELECT id, titulo, valor_total
        FROM contas_fixas
        WHERE usuario_id = %s
    """
    return execute_query(query, (user_id,))
