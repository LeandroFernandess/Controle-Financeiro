"""Módulo de gerenciamento de segurança e comunicação para aplicativo.

Este módulo fornece funcionalidades para hash de senhas e envio de mensagens SMS.
Integra-se com o Twilio para envio de SMS e utiliza bcrypt para segurança de senhas.

Componentes principais:
    - bcrypt: Biblioteca para hashing de senhas
    - os: Para acesso a variáveis de ambiente
    - dotenv: Para carregar variáveis de ambiente de um arquivo .env
    - Client: Classe do Twilio para gerenciamento de envio de mensagens SMS

Funcionalidades:
    * Hash seguro de senhas utilizando bcrypt
    * Carregamento de credenciais e configuração do ambiente
    * Envio de mensagens SMS via API do Twilio
"""

import bcrypt
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def hash_password(password):
    """Gera um hash da senha fornecida.

    Esta função utiliza o algoritmo bcrypt para gerar um hash seguro da
    senha, que pode ser armazenado no banco de dados.

    Args:
        password (str): A senha a ser hasheada.

    Returns:
        bytes: O hash gerado da senha.

    Example:
        >>> hashed_password = hash_password("minha_senha")
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed):
    """Verifica se a senha fornecida corresponde ao hash armazenado.

    Esta função compara a senha em texto claro com o hash armazenado
    para determinar se elas correspondem.

    Args:
        password (str): A senha em texto claro a ser verificada.
        hashed (bytes): O hash armazenado da senha.

    Returns:
        bool: Retorna True se a senha corresponder ao hash, False caso contrário.

    Example:
        >>> is_valid = check_password("minha_senha", hashed_password)
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def send_sms(to_phone, message):
    """Envia uma mensagem SMS para o número de telefone especificado.

    Esta função utiliza a API do Twilio para enviar mensagens SMS.
    As credenciais do Twilio devem estar configuradas nas variáveis de ambiente.

    Args:
        to_phone (str): O número de telefone do destinatário, incluindo o código do país.
        message (str): O corpo da mensagem a ser enviada.

    Raises:
        EnvironmentError: Lança um erro se as credenciais do Twilio não estiverem configuradas.

    Example:
        >>> send_sms("+5511999999999", "Olá, esta é uma mensagem de teste!")
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_phone]):
        raise EnvironmentError("Credenciais do Twilio não configuradas no ambiente")

    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=from_phone, to=to_phone)
