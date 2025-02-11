"""Módulo de autenticação e comunicação com serviços externos.

Este módulo fornece funcionalidades para:
- Hash e verificação de senhas usando bcrypt
- Envio de SMS via Twilio

Dependências:
- bcrypt: Para hash de senhas
- python-dotenv: Para gerenciamento de variáveis de ambiente
- twilio: Para integração com a API de SMS

Variáveis de Ambiente Requeridas:
- TWILIO_ACCOUNT_SID: SID da conta Twilio
- TWILIO_AUTH_TOKEN: Token de autenticação Twilio
- TWILIO_PHONE_NUMBER: Número de telefone Twilio
"""

import bcrypt
import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()


def hash_password(password):
    """Gera um hash seguro para uma senha usando bcrypt.

    Args:
        password (str): Senha em texto puro a ser hasheada

    Returns:
        bytes: Hash da senha no formato bytes

    Example:
        >>> hash_password("senha_secreta")
        b'$2b$12$...'
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def check_password(password, hashed):
    """Verifica se uma senha corresponde a um hash bcrypt.

    Args:
        password (str): Senha em texto puro para verificação
        hashed (bytes): Hash bcrypt armazenado

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário

    Example:
        >>> stored_hash = hash_password("senha_correta")
        >>> check_password("senha_correta", stored_hash)
        True
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed)


def send_sms(to_phone, message):
    """Envia uma mensagem SMS usando a API Twilio.

    Args:
        to_phone (str): Número de telefone do destinatário no formato E.164
        message (str): Conteúdo da mensagem SMS

    Raises:
        EnvironmentError: Se variáveis de ambiente do Twilio não estiverem configuradas

    Example:
        >>> send_sms("+5511999999999", "Seu código de verificação é 1234")
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_phone = os.getenv("TWILIO_PHONE_NUMBER")

    if not all([account_sid, auth_token, from_phone]):
        raise EnvironmentError("Credenciais do Twilio não configuradas no ambiente")

    client = Client(account_sid, auth_token)
    client.messages.create(body=message, from_=from_phone, to=to_phone)
