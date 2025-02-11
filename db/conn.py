import psycopg2
import os
from contextlib import contextmanager
from psycopg2 import OperationalError, IntegrityError
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection():

    try:
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
    except OperationalError as e:
        logger.error(f"Erro ao conectar ao banco de dados: {e}")
        raise


@contextmanager
def get_db_connection():

    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query, params=None):

    try:
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                    return cursor.fetchall()
            except Exception as e:
                conn.rollback()
                logger.error(f"Erro durante a consulta: {e}")
                raise
    except OperationalError as e:
        logger.error(f"Erro de conexão: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")


def execute_update(query, params=None):

    try:
        with get_db_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params or ())
                conn.commit()

            except Exception as e:
                conn.rollback()
                logger.error(f"Erro durante a transação: {e}")
                raise

    except OperationalError as e:
        logger.error(f"Erro de conexão: {e}")
    except IntegrityError as e:
        logger.error(f"Erro de integridade: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
