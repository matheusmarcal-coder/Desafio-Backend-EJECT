## NewStyle - Back-End
### Objetivo e funcionalidades principais do projeto: 
> **NewStyle** é uma API RESTful desenvolvida com **Django REST Framework** para gerenciar um sistema de e-commerce voltado para a venda de
roupas de forma integrada e escalável.
##  Acesso
- Produção API: [NewStyle](https://desafiobackendejectdeploy.pythonanywhere.com/)
- Documentação Interativa (Swagger): [http://127.0.0.1:8000/api/docs/](https://desafiobackendejectdeploy.pythonanywhere.com/api/docs/?utm_source=chatgpt.com)
##  Modelo Conceitual de Dados 
<img width="2107" height="1204" alt="Desafio Backend EJECT - Modelo Conceitual de Dados_ New Style" src="https://github.com/user-attachments/assets/d97c45b2-2f3e-4d6f-9e83-011da6238d6a" />


## Sobre o Projeto
A NewStyle é um projeto de desenvolvimento de uma API RESTful para um sistema de e-commerce, contendo clientes, lojistas e produtos. Desse modo, segue as principais funcionalidades implementadas:
- Gerenciamento de usuários
  - Cadastro e autenticação de usuários, sendo diferenciados por papéis: lojistas e clientes. O sistema agrupa os papéis em grupos, com suas respectivas permissões para controlar as operações disponíveis dentro da API.
- Gerenciamento de produtos
  - Operações CRUD de produtos, categoria e variações, incluindo informações como: nome, preço, tamanho, cor, estoque e status do produto.
- Realização de pedido de produtos
  - Finalização do carrinho do cliente para a criação do pedido, contendo endereço e método de pagamento escolhidas pelo cliente
- Documentação da API
  - Documentação gerada pelo `drf_spectacular`
- Publicação na internet
  - API publicada no PythonAnywhere, apresentando interface navegável do DRF.

## Tecnologias Utilizadas
| Tecnologia | Descrição |
|---|---|
| **Python 3.15** | Linguagem principal |
| **Django 6.1.2** | Framework Backend |
| **Django REST Framework 3.18.3** | Criação e gerenciamento de APIs RESTful |
| **SQLite** | Sistema Gerenciador de Banco de dados relacional  
## Principais Dependências Utilizadas 
| Dependência | Descrição |
|---|---|
|`djangorestframework-simplejwt` -> Versão 5.5.1 | Autenticação via JWT (token)|
|`PyJWT` -> Versão: 2.15.1 | Codifica e valida tokens JWT |
|`drf_spectacular` -> Versão 0.30.0 | Geração de documentação interativa Swagger |
|`django-filter` -> Versão 26.2 | Filtragem de dados nos endpoints |

## Configuração e Instalação

### Pré-requisitos

- Python 3.12+

### 1. Clone o Repositório

```bash
git clone https://github.com/matheusmarcal-coder/Desafio-Backend-EJECT.git
cd Desafio-Backend-EJECT
```

### 2. Configuração do Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### 3. Instalação das Dependências

```bash
pip install -r requirements.txt
```

### 4. Variáveis de Ambiente

Copie o arquivo de exemplo e ajuste os valores se necessário:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

### 5. Migrações do Banco

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Criação do Superusuário

```bash
python manage.py createsuperuser
```

### 7. Execução do Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em `http://localhost:8000`.


| Rota        | Descrição                             |
|-------------|---------------------------------------|
| `/admin/`   | Painel administrativo do Django       |
| `/auth/login/`| Login da API navegável         |

### Passo a passo para configurar a instalação (você só pode executar esse passo após a etapa de migrações feitas na parte 5 de "Configuração e instalação"):
#### 1- Seed do lojista inicial:, você deve executar o comando `python manage.py seed_lojista_inicial`
#### 2- Seed das categorias disponíveis da NewStyle: você deve executar o comando `python manage.py loaddata categorias.json`



### Variáveis de Ambiente para Produção

```bash
DEBUG=False
ALLOWED_HOSTS=desafiobackendejectdeploy.pythonanywhere.com
SECRET_KEY=chave-super-secreta-para-producao
LOJISTA_EMAIL=email_lojista@gmail.com
LOJISTA_SENHA=senha_segura_lojista
```

Para gerar uma `SECRET_KEY` nova:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### Padrões de Código

- **PEP 8** para formatação Python
- **Docstrings** para funções e classes
- **Português** para nomes de domínio (models, campos, serializers, views), mantendo em inglês o que é sintaxe do framework (`Meta`, `ForeignKey`, `Serializer`...)


## Principais endpoints e suas devidas descrições de funcionalidade
### Mockup completo de base para o projeto: [Mockup NewStyle](https://www.figma.com/design/2x9GdF7zL0uiG6wDUVvAA8/Trainee-26.1---Back-end?node-id=0-1&p=f) 
### Autenticação, registro e redefinição de senha
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
|POST | `/auth/register/` | Cria um novo usuário por meio do registro de seus dados no sistema. |
|POST | `/auth/login/` | Realiza o login do usuário e retorna o token de acesso (JWT). |
| POST | 🚨`/auth/forgot-password/` | Envia o e-mail de redefinição de senha para o usuário que esqueceu a senha. | 
| POST | 🚨`/auth/reset-password/` | Confirma a redefinição da senha usando o token enviado por e-mail e define a nova senha. |

### Gerenciamento de categorias 
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| GET | `/categorias/` |  Mostra as categorias presentes dentro da loja. (Lojistas e clientes vizualizam). |
| POST | `/categorias/` |  Cria uma categroria. (apenas lojistas podem criar categorias). |  
| GET | `/categorias/{id}/` |  Mostra uma categoria específica dentro da loja. (Lojistas e clientes vizualizam). |
| PUT | `/categorias/{id}/` | Atualiza os dados de uma categoria específica. (apenas lojistas podem atualizar categorias).| 
| PATCH | `/categorias/{id}/` |  Permite atualizar paricalmente os dados de uma categoria específica. (apenas lojistas podem atualizar categorias).| 

### Gerenciamento de produtos 
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| **POST** | `/produtos/` | Cria produtos dentro da loja (apenas lojistas podem criar produtos). |
| **GET** | `/produtos/` |  Visualiza os produtos dentro da loja (clientes visualizam apenas produtos ativos ; lojistas visualizam produtos ativos e inativos).|
|**GET** | `/produtos/{id}/` | Vizualiza um produto específico. |
| **PUT** | `/produtos/{id}/` | Permite atualizar os dados dentro do produto (apenas lojistas).|
| **PATCH** | `/produtos/{id}/` | Permite atualizar parcialmente os dados do produto, assim como o status do produto (ativo/inativo ; apenas lojistas).|

### Gerenciamento de variações 
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| GET | `/variacoes/` |  Mostra as variações presentes dentro da loja, independente do produto. (Lojistas e clientes vizualizam). |
| POST | `/variacoes/` |  Cria uma variação associada a um produto dentro da loja. (apenas lojistas podem criar variações). |  
| GET | `/variacoes/{id}/` |  Mostra uma variação específica dentro da loja. (Lojistas e clientes vizualizam). |
| PUT | `/variacoes/{id}/` | Atualiza os dados de uma variação específica. (apenas lojistas podem atualizar variações).| 
| PATCH | `/variacoes/{id}/` |  Permite atualizar paricalmente os dados de uma variação específica, assim como o estoque de uma variação específica. (apenas lojistas podem atualizar variações).| 

### Gerenciamento de carrinho 
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| GET | `/carrinho/` |  Permite vizualiar o carrinho (apenas usuário autenticados, logo: clientes e lojistas). |
| GET | `/carrinho/itens/` |  Mostra os itens que estão dentro do carrinho.|
| POST | `/carrinho/itens/` |  Adciona uma variação de produto dentro do carrinho. |  
| GET | `/carrinho/itens/{id}/` |  Mostra um item específico do carrinho. |
| PUT | `/carrinho/itens/{id}/` | Atualiza os dados de um item específico do carrinho, como sua quantidade. | 
| PATCH | `/carrinho/itens/{id}/` |  Permite atualizar paricalmente os itens de um carrinho , assim como a quantidade da variação desejada.| 
| DELETE | `/carrinho/itens/{id}/` |  Permite remover algum item do carrinho.| 
| PATCH | `/carrinho/itens/finalizar/` | Finaliza o carrinho, iniciando a criação do pedido.| 

### Gerenciamento de clientes 
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| GET | `/clientes/` |  Permite vizualiar os clientes cadastrados (apenas lojistas) ; Quando este é um cliente, acessa apenas seus próprios dados. |
| GET | `/clientes/{id}/` | consulta os dados de um cliente específico (apenas lojistas). |

### Gerenciamento de pedidos
|Método HTTP | Endpoint da API | Descrição |
|---|---|---|
| GET | `/pedidos/` | Lista os pedidos disponíveis (lojista vizualiza pedidos ativos, enquanto o cliente vizualiza apenas o próprio pedido).|
| POST | `/pedidos/` |  Cria um novo pedido. |  
| GET | `/pedidos/{id}/` |  Permite consultar um pedido específico com seus dados. |
| PATCH | `/pedidos/{id}/` |  Permite atualizar paricalmente os dados de um pedido, assim como o seu status de entrega.| 




###  Filtros e Buscas 
A API NewStyle oferece diversos filtros para facilitar a busca e organização dos produtos. Abaixo estão os filtros disponíveis e como utilizá-los:
####  Filtros
| Parâmetro | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `category` | ID | Filtragem por categoria específica | `?category=1` |
| `min_price` | Decimal | Filtragem por preço maior ou igual ao número inserido | `min_price=70.00` |
| `max_price` | Decimal | Filtragem por preço menor ou igual ao número inserido | `max_price=90.00` |
####  Busca por Texto
| Parâmetro |	Descrição |	Campos Pesquisados | Exemplo |
|---|---|---|---|
| `search` | Busca textual | Título do produto | `search=cargo+azul` | 
####  Paginação
| Parâmetro |	Descrição | Exemplo |
|---|---|---|
| `page` | Número da página | `?page=2` | 

##  Autenticação e Permissões
- **Endpoints de autenticação (`/auth/`)** — responsáveis por login, 🚨 recuperação🚨  e atualização de tokens JWT.  
- **Endpoints de usuários (`/clientes/`)** — permitem gerenciar contas e definir permissões específicas para cada usuário.
##  Estrutura do Projeto
```
Desafio-Backend-EJECT/
├── NewStyle/                       # App da API: models, serializers, views e rotas
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py                # Configuração de endpoints
│   └── views.py
├── setup/                     # Configurações do Django
│   ├── settings.py
│   └── urls.py
├── .env.example               # Modelo das variáveis de ambiente
├── requirements.txt           # Dependências Python
├── manage.py                  # Utilitário Django
└── README.md                  # Este arquivo
```
## Autor

### **Matheus Marçal**
#### Trainee Backend | Estudante do Bacharelado em Ciências e Tecnologia 
#### [GitHub](https://github.com/matheusmarcal-coder)
