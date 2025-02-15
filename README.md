# Controle Financeiro 💰

Um sistema de gerenciamento financeiro desenvolvido com Python e Streamlit. O projeto permite acompanhar receitas, despesas, contas fixas, faturas de cartão de crédito e resumos financeiros de forma intuitiva.

## Tecnologias Utilizadas 🛠️

- **Python**: Linguagem principal do projeto.
- **Streamlit**: Framework para criação da interface interativa.
- **PostGres**: Banco de dados utilizado para armazenar as transações financeiras.

## Estrutura do Projeto 📂

A estrutura do projeto está organizada da seguinte forma:

```
controlefinanceiro/
├── auth/
│   ├── authentication.py  # Gerenciamento de autenticação
│   ├── page.py  # Interface de login
│   ├── queries.py  # Consultas relacionadas a autenticação
│   ├── __init__.py
├── creditcard/
│   ├── page.py  # Interface para faturas do cartão
│   ├── queries.py  # Consultas relacionadas ao cartão de crédito
│   ├── __init__.py
├── db/
│   ├── conn.py  # Conexão com o banco de dados
│   ├── __init__.py
├── fixedaccounts/
│   ├── page.py  # Interface para contas fixas
│   ├── queries.py  # Consultas relacionadas a contas fixas
│   ├── __init__.py
├── income/
│   ├── page.py  # Interface para receitas
│   ├── queries.py  # Consultas relacionadas a receitas
│   ├── __init__.py
├── slips/
│   ├── page.py  # Interface para recibos
│   ├── queries.py  # Consultas relacionadas a recibos
│   ├── __init__.py
├── summary/
│   ├── page.py  # Interface do resumo financeiro
│   ├── queries.py  # Consultas para gerar o resumo financeiro
│   ├── __init__.py
├── venv/  # Ambiente virtual
├── .gitignore  # Arquivo para ignorar arquivos desnecessários no Git
├── app.py  # Arquivo principal para execução do Streamlit
├── requirements.txt  # Dependências do projeto
```

### Principais Pastas e Arquivos

- **auth/**: Gerenciamento de autenticação e login.
- **creditcard/**: Gerenciamento de faturas de cartão de crédito.
- **db/**: Configuração e conexão com o banco de dados.
- **fixedaccounts/**: Controle de contas fixas recorrentes.
- **income/**: Controle de receitas e entradas financeiras.
- **slips/**: Controle de recibos e comprovantes de pagamento.
- **summary/**: Página de resumo financeiro com estatísticas.
- **app.py**: Arquivo principal para executar a aplicação.
- **requirements.txt**: Arquivo com as bibliotecas necessárias para rodar o projeto.

## Funcionalidades 🚀

- Autenticação de usuários via Firebase.
- Cadastro e gerenciamento de receitas e despesas.
- Controle de contas fixas e variáveis.
- Monitoramento de faturas de cartão de crédito.
- Geração de resumo financeiro.
- Interface interativa e responsiva com Streamlit.

## Como Executar o Projeto 🔧

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/controlefinanceiro.git
   ```
2. **Entre no diretório do projeto:**
   ```bash
   cd controlefinanceiro
   ```
3. **Crie e ative o ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows
   venv\Scripts\activate
   # No Unix ou MacOS
   source venv/bin/activate
   ```
4. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Execute o aplicativo Streamlit:**
   ```bash
   streamlit run app.py
   ```
6. **Acesse no navegador:**
   Abra o navegador e acesse `http://localhost:8501/`.

## Configuração do Firebase 🔐

Para autenticação, é necessário configurar o Firebase:

1. Crie um arquivo `.env` na raiz do projeto.
2. Adicione as credenciais do Firebase:
   ```
  DB_NAME= Nome do BD
  DB_USER= Usuário do BD
  DB_PASSWORD= Senha do BD
  DB_HOST= Link do BD
  DB_PORT= Porta do DB
  TWILIO_ACCOUNT_SID= Conta do Twilio
  TWILIO_AUTH_TOKEN= Token de autenticação do Twilio
  TWILIO_PHONE_NUMBER= Número de telefone gerado pelo Twilio
   ```

## Contribuindo 🤝

Contribuições são bem-vindas! Se você encontrar algum problema ou tiver sugestões, abra uma *issue* ou envie um *pull request*.

## Contato 💬

Caso tenha dúvidas ou sugestões, entre em contato:

- **Nome**: Leandro Fernandes
- **Email**: leandrofernandes1600@email.com
- **GitHub**: https://github.com/se](https://github.com/LeandroFernandess/Controle-Financeiro
- **Links utilizados**:
  - BD --> https://cloud.tembo.io/orgs/org_2rrdBUpzp1gEfGfFusn5XPWcHnR/instances
  - API para autenticação e recuperação de senha --> https://www.twilio.com/login?iss=https%3A%2F%2Flogin.twilio.com%2F
---

*Documentação atualizada em: `14/02/2025`.* 🚀

