"""Módulo de páginas da aplicação.

Este módulo contém as páginas da aplicação Streamlit, incluindo:
- Página de login
- Página de cadastro de usuário
- Página de recuperação de senha

Dependências:
- streamlit: Para criação da interface gráfica
- db_queries: Para interação com o banco de dados
- authentication: Para autenticação de usuários
- random: Para geração de tokens
- re: Para validação de e-mails
"""

import streamlit as st
from .authentication import *
from .queries import (
    get_user_by_email,
    check_existing_email,
    check_existing_phone,
    create_user,
    get_password_by_phone,
    update_password_by_phone,
)
import random
import re


def is_valid_email(email):
    """Valida se um e-mail está no formato correto.

    Args:
        email (str): O endereço de e-mail a ser validado

    Returns:
        bool: True se o e-mail for válido, False caso contrário

    Example:
        >>> is_valid_email("teste@exemplo.com")
        True
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def login_page():
    """Exibe a página de login e processa a autenticação do usuário.

    Exemplo:
        >>> login_page()
    """
    st.title("Login")
    mail = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")

    if st.button("Login"):
        result = get_user_by_email(mail)

        if result:
            user_id = result[0][0]
            senha_hex = result[0][1]

            # Verificação do prefixo
            if not senha_hex.startswith("\\x"):
                st.error("Formato de senha inválido no banco de dados!")
                return

            try:
                # Remove o prefixo escapado "\\x" e converte para bytes
                hashed_password = bytes.fromhex(senha_hex[2:])
                if check_password(password, hashed_password):
                    st.success("Login realizado com sucesso!")
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_id
                    st.rerun()
                else:
                    st.error("Senha incorreta.")
            except ValueError as e:
                st.error(f"Erro ao processar a senha: {e}")
        else:
            st.error("Usuário não encontrado.")


def create_user_page():
    """Exibe e gerencia a interface de cadastro de novos usuários.

    Exemplo:
        >>> create_user_page()
    """
    st.title("Cadastro de Usuário")
    name = st.text_input("Nome")
    surname = st.text_input("Sobrenome")
    mail = st.text_input("E-mail")
    password = st.text_input("Senha", type="password")
    phone = st.text_input("Telefone", placeholder="Exemplo: +5531123456789")

    if st.button("Cadastrar"):
        if not all([name, surname, mail, password]):
            st.error("Todos os campos são obrigatórios.")
            return

        if not is_valid_email(mail):
            st.error("Por favor, insira um e-mail válido.")
            return

        # Validação do telefone
        phone_regex = re.compile(r"^\+\d{1,3}\d{10}$")
        if phone and not phone_regex.match(phone):
            st.error("Por favor, insira um telefone válido no formato +CCXXXXXXXXXX.")
            return

        existing_email = check_existing_email(mail)
        existing_phone = check_existing_phone(phone) if phone else None

        try:
            if existing_email:
                st.error("Este e-mail já está cadastrado.")
                return

            if existing_phone:
                st.error("Este telefone já está cadastrado.")
                return

            pw_hash = hash_password(password)
            create_user(name, surname, mail, pw_hash, phone)
            st.success("Usuário cadastrado com sucesso!")

        except Exception as e:
            st.error(f"Erro ao cadastrar usuário: {e}")


def forgot_password_page():
    """Exibe a página para recuperação de senha e envia um token SMS para o telefone do usuário.

    Exemplo:
        >>> forgot_password_page()
    """
    st.title("Recuperar Senha")
    phone = st.text_input("Telefone")

    if st.button("Enviar Token"):
        result = get_password_by_phone(phone)

        if result:
            # Gerar um token aleatório
            token = str(random.randint(100000, 999999))
            message = f"Seu token de recuperação de senha é: {token}"
            send_sms(phone, message)

            # Salvar o token na sessão para validação posterior
            st.session_state["token"] = token
            st.session_state["telefone"] = phone

            st.success(
                "Token enviado com sucesso! Insira o token para redefinir sua senha."
            )
            st.session_state["awaiting_token"] = True
        else:
            st.error("Telefone não encontrado.")

    if st.session_state.get("awaiting_token"):
        token_input = st.text_input("Insira o token recebido")
        new_pw = st.text_input("Nova Senha", type="password")
        confirm_pw = st.text_input("Confirmar Nova Senha", type="password")

        if st.button("Redefinir Senha"):
            if token_input == st.session_state["token"]:
                if new_pw == confirm_pw:
                    pw_hash = hash_password(new_pw)
                    update_password_by_phone(st.session_state["telefone"], pw_hash)
                    st.success("Senha redefinida com sucesso!")
                    st.session_state["awaiting_token"] = False
                    del st.session_state["token"]
                    del st.session_state["telefone"]
                else:
                    st.error("As senhas não coincidem.")
            else:
                st.error("Token inválido.")
