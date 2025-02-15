"""Módulo de interação com o banco de dados para aplicativo.

Este módulo é responsável por gerenciar a conexão com o banco de dados,
executar consultas e atualizações, e garantir a integridade das transações.
Integra-se com o sistema de autenticação e outras funcionalidades da aplicação.

Componentes principais:
    - execute_query: Função para executar consultas SQL de leitura
    - execute_update: Função para executar comandos SQL de escrita
    - get_connection: Função para estabelecer e retornar a conexão com o banco de dados

Funcionalidades:
    * Execução de consultas SQL para recuperação de dados
    * Execução de comandos SQL para atualização de registros
    * Gerenciamento seguro de conexões com o banco de dados
    * Tratamento de exceções e registro de erros durante operações de banco de dados
"""

from db.conn import execute_query, execute_update, get_connection


def get_user_by_email(email):
    """Recupera um usuário a partir do e-mail fornecido.

    Esta função executa uma consulta para obter o ID e a senha do usuário
    associado ao e-mail fornecido.

    Args:
        email (str): O e-mail do usuário a ser pesquisado.

    Returns:
        tuple: Tupla contendo o ID do usuário e a senha, se encontrado; caso contrário, None.

    Example:
        >>> user = get_user_by_email("usuario@exemplo.com")
    """
    return execute_query("SELECT id, senha FROM usuarios WHERE email = %s;", (email,))


def check_existing_email(email):
    """Verifica se um e-mail já está cadastrado no sistema.

    Esta função executa uma consulta para verificar a existência do e-mail
    fornecido na tabela de usuários.

    Args:
        email (str): O e-mail a ser verificado.

    Returns:
        list: Lista contendo o e-mail se encontrado; caso contrário, uma lista vazia.

    Example:
        >>> exists = check_existing_email("usuario@exemplo.com")
    """
    return execute_query("SELECT email FROM usuarios WHERE email = %s", (email,))


def check_existing_phone(phone):
    """Verifica se um telefone já está cadastrado no sistema.

    Esta função executa uma consulta para verificar a existência do telefone
    fornecido na tabela de usuários.

    Args:
        phone (str): O telefone a ser verificado.

    Returns:
        list: Lista contendo o telefone se encontrado; caso contrário, uma lista vazia.

    Example:
        >>> exists = check_existing_phone("+5511999999999")
    """
    return execute_query("SELECT telefone FROM usuarios WHERE telefone = %s", (phone,))


def create_user(name, surname, email, password_hash, phone):
    """Cria um novo usuário no banco de dados.

    Esta função insere um novo registro de usuário com as informações fornecidas.

    Args:
        name (str): Nome do usuário.
        surname (str): Sobrenome do usuário.
        email (str): E-mail do usuário.
        password_hash (str): Hash da senha do usuário.
        phone (str): Telefone do usuário.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
        IntegrityError: Lança um erro se houver problemas de integridade.

    Example:
        >>> create_user("Nome", "Sobrenome", "usuario@exemplo.com", "hashed_password", "+5511999999999")
    """
    execute_update(
        """
        INSERT INTO usuarios (nome, sobrenome, email, senha, telefone)
        VALUES (%s, %s, %s, %s, %s);
        """,
        (name, surname, email, password_hash, phone),
    )


def get_password_by_phone(phone):
    """Recupera a senha de um usuário a partir do telefone fornecido.

    Esta função executa uma consulta para obter a senha associada ao telefone
    do usuário.

    Args:
        phone (str): O telefone do usuário a ser pesquisado.

    Returns:
        tuple: Tupla contendo a senha se encontrada; caso contrário, None.

    Example:
        >>> password = get_password_by_phone("+5511999999999")
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT senha FROM usuarios WHERE telefone = %s;", (phone,))
        return cursor.fetchone()


def update_password_by_phone(phone, new_password_hash):
    """Atualiza a senha de um usuário com base no telefone fornecido.

    Esta função modifica a senha do usuário associado ao telefone fornecido.

    Args:
        phone (str): O telefone do usuário cuja senha deve ser atualizada.
        new_password_hash (str): O novo hash da senha a ser definido.

    Raises:
        OperationalError: Lança um erro se houver problemas de conexão.
    """
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE usuarios SET senha = %s WHERE telefone = %s;",
            (new_password_hash, phone),
        )
    conn.commit()
