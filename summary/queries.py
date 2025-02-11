from db.conn import execute_query
from datetime import datetime


def table_is_empty(table_name):
    """Verifica se uma tabela está vazia."""
    query = f"SELECT COUNT(*) FROM {table_name}"
    result = execute_query(query)
    return result[0][0] == 0


def search_user_info(usuario_id, mes=None, ano=None):
    # Define o mês e ano atual se não forem fornecidos
    if mes is None:
        mes = datetime.now().month
    if ano is None:
        ano = datetime.now().year

    # Verificar se as tabelas possuem dados
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

    # Buscar renda do usuário
    renda_query = "SELECT valor FROM Renda WHERE user_id = %s"
    renda = execute_query(renda_query, (usuario_id,))
    renda_mensal = renda[0][0] if renda else 0

    # Buscar gastos com cartão de crédito no mês e ano especificados
    if not table_is_empty("cartoes_credito"):
        cartao_query = """
            SELECT SUM(valor_parcela) 
            FROM cartoes_credito 
            WHERE usuario_id = %s 
              AND EXTRACT(MONTH FROM dia_vencimento) = %s
              AND EXTRACT(YEAR FROM dia_vencimento) = %s
        """
        gastos_cartao = execute_query(cartao_query, (usuario_id, mes, ano))
        gastos_cartao = (
            gastos_cartao[0][0] if gastos_cartao and gastos_cartao[0][0] else 0
        )
    else:
        gastos_cartao = 0

    # Buscar boletos do mês e ano especificados
    if not table_is_empty("boletos"):
        boletos_query = """
            SELECT SUM(valor_total) 
            FROM boletos 
            WHERE usuario_id = %s 
              AND EXTRACT(MONTH FROM data_pagamento) = %s
              AND EXTRACT(YEAR FROM data_pagamento) = %s
        """
        gastos_boletos = execute_query(boletos_query, (usuario_id, mes, ano))
        gastos_boletos = (
            gastos_boletos[0][0] if gastos_boletos and gastos_boletos[0][0] else 0
        )
    else:
        gastos_boletos = 0

    # Buscar contas fixas do mês e ano especificados
    if not table_is_empty("contas_fixas"):
        contas_fixas_query = """
            SELECT SUM(valor_total) 
            FROM contas_fixas 
            WHERE usuario_id = %s
        """
        gastos_contas_fixas = execute_query(contas_fixas_query, (usuario_id,))
        gastos_contas_fixas = (
            gastos_contas_fixas[0][0]
            if gastos_contas_fixas and gastos_contas_fixas[0][0]
            else 0
        )
    else:
        gastos_contas_fixas = 0

    return {
        "renda_mensal": renda_mensal,
        "gastos_cartao": gastos_cartao,
        "gastos_boletos": gastos_boletos,
        "gastos_contas_fixas": gastos_contas_fixas,
    }
