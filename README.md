# Sonhario - API
![Sonhario Logo](meta/cover.png)
A API em Django do aplicativo **Sonhario** -- um diário de hábitos do sono que usa dados passados para tentar melhorar a sua rotina. Projeto desenvolvido para fins de estudo.\
Confira também o [repositório do frontend](https://github.com/omarcosss/sonhario-front)

## Tecnologias Utilizadas
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Groq](https://groq.com/) para análise de dados
* [Render](https://groq.com/) para produção

## Como Começar

### Prerequisitos

* Python 3.x
* pip
* venv

### Instalação

1. Clone o repositório

   ```bash
   git clone https://github.com/bunny-sammy/sonhario-api.git
   cd sonhario-api
   ```

2. Crie e ative o ambiente virtual

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   # Ou no Windows
   .venv/Scripts/activate
   ```

3. Instale as dependências

   ```bash
   pip install -r requirements.txt
   ```

4. Aplique as migrações

   ```bash
   python manage.py migrate
   ```

5. Crie suas variáveis de ambiente
   ```bash
   cp .env.example .env
   # Ou no Windows
   copy .env.example .env
   ```

6. Inicie o servidor de desenvolvimento

   ```bash
   python manage.py runserver
   ```

## Documentação da API

Para entender o funcionamento da API e contribuir com o projeto, acesse a [documentação detalhada aqui](https://api-sonhario.onrender.com/docs/).