"""Módulo de conexão e gerenciamento de banco de dados PostgreSQL.

Este módulo é responsável por gerenciar a conexão com o banco de dados,
executar consultas e atualizações, e garantir a integridade das transações.

Funcionalidades principais:
    - Estabelecimento de conexão com o banco de dados
    - Execução de consultas SQL e atualizações
    - Gerenciamento de transações com rollback em caso de erro

Dependências:
    - psycopg2: Para interação com o banco de dados PostgreSQL
    - os: Para acessar variáveis de ambiente
    - contextlib: Para gerenciamento de contexto
    - logging: Para registro de erros e eventos

Exceções:
    - Erros de conexão com o banco de dados
    - Erros de integridade durante as transações
    - Erros inesperados durante a execução de consultas
"""

import psycopg2
import os
from contextlib import contextmanager
from psycopg2 import OperationalError, IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_connection():
    """Estabelece uma conexão com o banco de dados PostgreSQL.

    Esta função utiliza as variáveis de ambiente para obter as credenciais
    necessárias e tenta conectar ao banco de dados. Em caso de falha, um erro
    é registrado.

    Returns:
        connection: Objeto de conexão ao banco de dados.

    Raises:
        OperationalError: Lança um erro se a conexão falhar.
    """
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
    """Context manager para gerenciar a conexão com o banco de dados.

    Esta função cria um gerenciador de contexto que garante que a conexão
    ao banco de dados será fechada após seu uso.

    Yields:
        connection: Objeto de conexão ao banco de dados.

    Example:
        >>> with get_db_connection() as conn:
        >>>     # Operações com o banco de dados
    """
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()


def execute_query(query, params=None):
    """Executa uma consulta SQL e retorna os resultados.

    Esta função executa uma consulta SQL que pode retornar dados e
    utiliza um gerenciador de contexto para a conexão com o banco de dados.

    Args:
        query (str): Consulta SQL a ser executada.
        params (tuple, optional): Parâmetros da consulta. Padrão é None.

    Returns:
        list: Lista de tuplas contendo os resultados da consulta.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
    """
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
    """Executa uma atualização SQL e comita as alterações.

    Esta função executa comandos SQL que não retornam dados (como INSERT,
    UPDATE e DELETE) e gerencia transações no banco de dados.

    Args:
        query (str): Consulta SQL a ser executada.
        params (tuple, optional): Parâmetros da consulta. Padrão é None.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
        IntegrityError: Lança um erro se houver problemas de integridade.
    """
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
