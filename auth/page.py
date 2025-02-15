"""Módulo de gerenciamento de usuários para aplicativo Streamlit.

Este módulo fornece funcionalidades relacionadas ao gerenciamento de usuários,
incluindo autenticação, registro e recuperação de senhas. Integra-se com o
banco de dados através do módulo queries.

Componentes principais:
    - get_user_by_email: Função para recuperar um usuário a partir do e-mail
    - check_existing_email: Função para verificar se um e-mail já está cadastrado
    - check_existing_phone: Função para verificar se um telefone já está cadastrado
    - create_user: Função para criar um novo usuário
    - get_password_by_phone: Função para recuperar a senha de um usuário pelo telefone
    - update_password_by_phone: Função para atualizar a senha de um usuário

Funcionalidades:
    * Autenticação de usuários com e-mail e senha
    * Registro de novos usuários com validação de dados
    * Recuperação de senha via token enviado por SMS
    * Verificação de dados existentes (e-mail e telefone) para evitar duplicações
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
    """Verifica se o e-mail fornecido está no formato válido.

    Esta função utiliza uma expressão regular para validar a estrutura do e-mail.

    Args:
        email (str): O e-mail a ser validado.

    Returns:
        bool: Retorna True se o e-mail for válido, False caso contrário.

    Example:
        >>> is_valid_email("usuario@exemplo.com")
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def login_page():
    """Gerencia a interface de login do usuário.

    Esta função exibe um formulário para o usuário inserir suas credenciais
    e realiza a autenticação. Se as credenciais forem válidas, o usuário é
    autenticado e o estado da sessão é atualizado.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
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
    """Gerencia a interface de cadastro de usuário.

    Esta função exibe um formulário para o usuário inserir informações
    necessárias para criar uma nova conta. Valida os dados inseridos
    antes de salvá-los no banco de dados.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
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
    """Gerencia a interface de recuperação de senha.

    Esta função permite ao usuário solicitar um token de recuperação
    via SMS e redefinir a senha utilizando o token recebido.

    Returns:
        None: A função não retorna valor, mas atualiza a interface do Streamlit.
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
