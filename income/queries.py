"""Módulo de conexão e manipulação de dados no banco de dados.

Este módulo é responsável por executar consultas e atualizações no banco de dados,
facilitando a interação com as tabelas de dados da aplicação.

Componentes principais:
    - execute_query: Função para executar consultas SQL de leitura
    - execute_update: Função para executar comandos SQL de escrita

Módulos integrados:
    - db.conn: Conexão com o banco de dados e gerenciamento de transações

Funcionalidades:
    - Realizar operações CRUD básicas
    - Suporte a transações seguras
    - Manutenção da integridade dos dados

Fluxo da aplicação:
    1. Conectar ao banco de dados
    2. Executar consultas e atualizações conforme necessário
    3. Retornar resultados ou confirmar mudanças
"""

from db.conn import execute_query, execute_update


def get_existing_income(user_id):
    """Recupera a renda existente de um usuário no banco de dados.

    Esta função executa uma consulta para obter o valor e a data de atualização
    da renda associada a um usuário específico.

    Args:
        user_id (int): ID do usuário cuja renda deve ser recuperada.

    Returns:
        list: Uma lista de tuplas contendo o valor da renda e a data de atualização.

    Example:
        >>> incomes = get_existing_income(123)
    """
    return execute_query(
        "SELECT valor, data_atualizacao FROM Renda WHERE user_id = %s;", (user_id,)
    )


def save_income(user_id, new_income):
    """Armazena ou atualiza a renda de um usuário no banco de dados.

    Esta função insere um novo registro de renda ou atualiza um registro existente
    com base no ID do usuário. Se um registro já existir, seu valor é atualizado
    e a data de atualização é definida para o timestamp atual.

    Args:
        user_id (int): ID do usuário ao qual a renda está associada.
        new_income (float): Novo valor da renda a ser salvo.

    Returns:
        None: A função não retorna valor, mas persiste os dados no banco de dados.

    Example:
        >>> save_income(123, 4500.00)
    """
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
