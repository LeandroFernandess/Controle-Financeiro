"""Módulo de operações financeiras em banco de dados.

Este módulo fornece funcionalidades para:
- Verificar estado de tabelas no banco de dados
- Recuperar informações financeiras consolidadas de usuários

Componentes principais:
    - table_is_empty: Verifica se tabela está vazia
    - search_user_info: Obtém dados financeiros consolidados

Dependências:
    - db.conn.execute_query: Função para execução de queries SQL
    - datetime: Para manipulação de datas

Exceções:
    - Assume que execute_query trata erros de conexão/database
    - As funções retornam valores padrão (0) em caso de dados ausentes
"""

from db.conn import execute_query
from datetime import datetime


def table_is_empty(table_name):
    """Verifica se uma tabela específica está vazia no banco de dados.

    Args:
        table_name (str): Nome da tabela a ser verificada

    Returns:
        bool: True se a tabela estiver vazia, False caso contrário

    Raises:
        DatabaseError: Se ocorrer erro na query (propagado de execute_query)

    Exemplo:
        >>> table_is_empty("usuarios")
        True
    """
    query = f"SELECT COUNT(*) FROM {table_name}"
    result = execute_query(query)
    return result[0][0] == 0


def search_user_info(usuario_id, mes=None, ano=None):
    """Obtém informações financeiras consolidadas de um usuário para período específico.

    Coleta e calcula:
        - Renda mensal
        - Gastos com cartão de crédito
        - Gastos com boletos
        - Gastos com contas fixas

    Parâmetros:
        usuario_id (int): ID do usuário para consulta
        mes (int, opcional): Mês de referência (1-12). Padrão: mês atual
        ano (int, opcional): Ano de referência. Padrão: ano atual

    Retorna:
        dict: Dicionário com estrutura:
            {
                "renda_mensal": float,
                "gastos_cartao": float,
                "gastos_boletos": float,
                "gastos_contas_fixas": float
            }

    Lógica:
        1. Verifica se tabelas relevantes estão vazias
        2. Busca renda do usuário na tabela Renda
        3. Calcula gastos por categoria (cartões, boletos, contas fixas)
        4. Retorna valores consolidados

    Notas:
        - Retorna valores zerados se todas tabelas estiverem vazias
        - Usa data atual como fallback para mês/ano não informados
        - Valores nulos no banco são convertidos para 0

    Exemplo:
        >>> search_user_info(123, mes=5, ano=2023)
        {'renda_mensal': 5000.0, 'gastos_cartao': 1200.0, ...}
    """
    if mes is None:
        mes = datetime.now().month
    if ano is None:
        ano = datetime.now().year

    if (
        table_is_empty("Renda")
        and table_is_empty("cartoes_credito")
        and table_is_empty("boletos")
        and table_is_empty("contas_fixas")
    ):
        return {
            "renda_mensal": 0,
            "gastos_cartao": 0,
            "gastos_boletos": 0,
            "gastos_contas_fixas": 0,
        }

    renda_query = "SELECT valor FROM Renda WHERE user_id = %s"
    renda = execute_query(renda_query, (usuario_id,))
    renda_mensal = renda[0][0] if renda else 0

    gastos_cartao = 0
    if not table_is_empty("cartoes_credito"):
        cartao_query = """
            SELECT SUM(valor_parcela) 
            FROM cartoes_credito 
            WHERE usuario_id = %s 
              AND EXTRACT(MONTH FROM dia_vencimento) = %s
              AND EXTRACT(YEAR FROM dia_vencimento) = %s
        """
        result = execute_query(cartao_query, (usuario_id, mes, ano))
        gastos_cartao = result[0][0] if result and result[0][0] else 0

    gastos_boletos = 0
    if not table_is_empty("boletos"):
        boletos_query = """
            SELECT SUM(valor_total) 
            FROM boletos 
            WHERE usuario_id = %s 
              AND EXTRACT(MONTH FROM data_pagamento) = %s
              AND EXTRACT(YEAR FROM data_pagamento) = %s
        """
        result = execute_query(boletos_query, (usuario_id, mes, ano))
        gastos_boletos = result[0][0] if result and result[0][0] else 0

    gastos_contas_fixas = 0
    if not table_is_empty("contas_fixas"):
        contas_fixas_query = """
            SELECT SUM(valor_total) 
            FROM contas_fixas 
            WHERE usuario_id = %s
        """
        result = execute_query(contas_fixas_query, (usuario_id,))
        gastos_contas_fixas = result[0][0] if result and result[0][0] else 0

    return {
        "renda_mensal": renda_mensal,
        "gastos_cartao": gastos_cartao,
        "gastos_boletos": gastos_boletos,
        "gastos_contas_fixas": gastos_contas_fixas,
    }
