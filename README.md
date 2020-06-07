# Error Central - API
Em projetos modernos é cada vez mais comum o uso de arquiteturas baseadas em serviços ou microsserviços. Nestes ambientes complexos, erros podem surgir em diferentes camadas da aplicação (backend, frontend, mobile, desktop) e mesmo em serviços distintos. Desta forma, é muito importante que os desenvolvedores possam centralizar todos os registros de erros em um local, de onde podem monitorar e tomar decisões mais acertadas.
Com base no que foi descrito acima, o projeto Error Central é um sistema para a centralização de logs de aplicações variadas. A API conta com endpoints que permitem operações de CRUD nos logs.
## Documentação
[DOCS](https://documenter.getpostman.com/view/6653675/SztK2kAs)
## Ferramentas utilizadas
- Python
- Django
- Django REST Framework
- Djoser
- PostgreSQL
- Django Filters
## Como utilizar
### Criando ambiente virtual
1 - Abra um terminal na raiz do projeto
2 - Instale virtualenv usando ``pip install virtualenv``
3 - Crie um ambiente virtual usando ``virtualenv nome_da_virtualenv``
4 - Para ativá-lo, utilize um dos dois comandos abaixo:  
- `souce nome_da_virtualenv/bin/activate`  (Linux ou macOS)
-  `nome_da_virtualenvScriptsactivate`  (Windows)

5 - Instale as dependências usando ``pip install -r requirements.txt``
### Configurando banco de dados
1 - O banco de dados utilizado é o PostgreSQL. Caso não tenha instalado, poderá baixá-lo [aqui](https://www.postgresql.org/download/).

2 - Após instalado, execute os seguintes comando para criar o banco de dados:


``` SQL
-- Criar usuário errorcentral
CREATE USER errorcentral WITH PASSWORD 'errorcentral';  
ALTER USER errorcentral WITH SUPERUSER;

-- Criar banco de dados
CREATE DATABASE errorcentral WITH OWNER = errorcentral
ENCODING = 'UTF8'
TABLESPACE = pg_default
CONNECTION  LIMIT  =  -1;

-- Criar schema
CREATE SCHEMA core AUTHORIZATION  core; 
GRANT ALL ON SCHEMA core TO core WITH GRANT OPTION;
```
4 - Em um terminal, na pasta do projeto, use o seguinte comando para criar as tabelas: ``python manage.py migrate``
## Iniciando o servidor
Após criar o banco de dados, rode o comando ``python manage.py runserver``. Pronto!
## Autenticação
1 - Toda requisição para a API deve ser autenticada por um Token. Para isso, crie um usuário com o comando ``python manage.py createsuperuser``
2 - Faça uma requisição POST para o endpoint http://localhost:8000/auth/token/login/ com o body:
```
{
	"username": "username_do_usuario",
	"password": "senha_do_usuario"
}
```
A resposta será um token parecido com este:
```
{
	"token": "828ac2ed6f79fe2270d0a57d4632e5af032c89c1"
}
```
3 - Copie o token devolvido e adicione um header Authorize para todas as requisições que você for fazer para a api, prefixado pela palavra "Token " (Considere o espaço após a palavra Token). Ficando da seguinte forma:
```
{
	"Authorize": "Bearer 828ac2ed6f79fe2270d0a57d4632e5af032c89c1"
}
```
4 - Usuário autenticado! Caso queira fazer logout, utilize o endpoint http://127.0.0.1:8000/auth/token/logout/.

