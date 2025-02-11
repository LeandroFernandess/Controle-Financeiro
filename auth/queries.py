"""Módulo de conexão e manipulação de banco de dados PostgreSQL.

Este módulo fornece funcionalidades para:
- Estabelecimento de conexão com o banco de dados
- Execução de consultas e atualizações
- Gerenciamento de exceções de banco de dados

Dependências:
- psycopg2: Para interação com o banco de dados PostgreSQL
- os: Para acesso a variáveis de ambiente
- contextlib: Para gerenciamento de contexto
- logging: Para registro de logs de operações e erros

Funções principais:
- get_connection: Estabelece uma conexão com o banco de dados
- get_db_connection: Context manager para gerenciar a conexão ao banco de dados
- execute_query: Executa uma consulta SQL e retorna os resultados
- execute_update: Executa uma atualização SQL no banco de dados
"""

from db.conn import execute_query, execute_update, get_connection
import psycopg2


def get_user_by_email(email):
    """Busca um usuário pelo e-mail.

    Args:
        email (str): E-mail do usuário.

    Returns:
        tuple: Tupla contendo o ID e a senha do usuário, ou None se não encontrado.

    Exemplo:
        >>> user_data = get_user_by_email("usuario@exemplo.com")
    """
    return execute_query("SELECT id, senha FROM usuarios WHERE email = %s;", (email,))


def check_existing_email(email):
    """Verifica se um e-mail já está cadastrado.

    Args:
        email (str): E-mail a ser verificado.

    Returns:
        bool: True se o e-mail já existe, False caso contrário.

    Exemplo:
        >>> email_exists = check_existing_email("usuario@exemplo.com")
    """
    return execute_query("SELECT email FROM usuarios WHERE email = %s", (email,))


def check_existing_phone(phone):
    """Verifica se um telefone já está cadastrado.

    Args:
        phone (str): Telefone a ser verificado.

    Returns:
        bool: True se o telefone já existe, False caso contrário.

    Exemplo:
        >>> phone_exists = check_existing_phone("+5531123456789")
    """
    return execute_query("SELECT telefone FROM usuarios WHERE telefone = %s", (phone,))


def create_user(name, surname, email, password_hash, phone):
    """Cria um novo usuário no banco de dados.

    Args:
        name (str): Nome do usuário.
        surname (str): Sobrenome do usuário.
        email (str): E-mail do usuário.
        password_hash (str): Hash da senha do usuário.
        phone (str): Telefone do usuário.

    Returns:
        None

    Exemplo:
        >>> create_user("João", "Silva", "joao@exemplo.com", "hash_senha", "+5531123456789")
    """
    execute_update(
        """
        INSERT INTO usuarios (nome, sobrenome, email, senha, telefone)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (name, surname, email, password_hash, phone),
    )


def get_password_by_phone(phone):
    """Busca a senha de um usuário pelo telefone.

    Args:
        phone (str): Telefone do usuário.

    Returns:
        str: Senha do usuário, ou None se não encontrado.

    Exemplo:
        >>> password = get_password_by_phone("+5531123456789")
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT senha FROM usuarios WHERE telefone = %s;", (phone,))
        return cursor.fetchone()


def update_password_by_phone(phone, new_password_hash):
    """Atualiza a senha de um usuário pelo telefone.

    Args:
        phone (str): Telefone do usuário.
        new_password_hash (str): Hash da nova senha.

    Returns:
        None

    Exemplo:
        >>> update_password_by_phone("+5531123456789", "novo_hash_senha")
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE usuarios SET senha = %s WHERE telefone = %s;",
            (new_password_hash, phone),
        )
    conn.commit()
