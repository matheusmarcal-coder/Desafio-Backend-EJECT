## 🛍️ NewStyle - Back-End
### Objetivo e funcionalidades principais do projeto: 
> **NewStyle** é uma API RESTful desenvolvida com **Django REST Framework** para gerenciar um sistema de e-commerce voltado para a venda de
roupas de forma integrada e escalável.
## 🌐 Acesso
- API Base: [API](https://desafiobackendejectdeploy.pythonanywhere.com/)
- (⚠️OBRIGATÓRIO⚠️)Documentação Interativa (Swagger): 🚨???🚨🚨???🚨🚨???🚨🚨???🚨
  obs: "Documentação da API: Instruções para acessar o Swagger com
detalhes dos endpoints."
## 🗂️ Modelo Conceitual de Dados  🚨???🚨🚨???🚨(⚠️OBRIGATÓRIO⚠️)
<img width="2107" height="1204" alt="Desafio Backend EJECT - Modelo Conceitual de Dados_ New Style" src="https://github.com/user-attachments/assets/d0d5233b-33fe-418a-83a4-ebba3512adca" />

## 📋 Sobre o Projeto
A NewStyle é um projeto de desenvolvimento de uma API RESTful para um sistema de e-commerce, contendo clientes, lojistas e produtos. Desse modo, segue as principais funcionalidades implementadas:
- Gerenciamento de usuários
  - Cadastro e autenticação de usuários, sendo diferenciados por papéis: lojistas e clientes. O sistema agrupa os papéis em grupos, com suas respectivas permissões para controlar as operações disponíveis dentro da API.
- Gerenciamento de produtos
  - Operações CRUD de produtos, categoria e variações, incluindo informações como: nome, preço, tamanho, cor, estoque e status do produto. 
- Publicação na internet
  - API publicada no PythonAnywhere, apresentando interface navegável do DRF.

## 🧰 Tecnologias Utilizadas
| Tecnologia | Descrição |
|---|---|
| **Python 3.15** | Linguagem principal |
| **Django 6.1.2** | Framework Backend |
| **Django REST Framework 3.18.3** | Criação e gerenciamento de APIs RESTful |
| **SQLite** | Sistema Gerenciador de Banco de dados relacional  
## (⚠️OBRIGATÓRIO⚠️)Principais Dependências Utilizadas 
| Dependência | Descrição |
|---|---|
|`djangorestframework-simplejwt` -> Versão 5.5.1 | Autenticação via JWT (token)|
|`PyJWT` -> Versão: 2.15.1 | Codifica e valida tokens JWT |
|`drf_yasg` -> Versão 1.21.18 | Geração de documentação interativa Swagger |

## (⚠️OBRIGATÓRIO⚠️) ⚙️ Configuração e Instalação

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

### Passo a passo para configurar a instalação:
🚨NAO ESQUECER AS SEEDS🚨

### Variáveis de Ambiente para Produção

```bash
DEBUG=False
ALLOWED_HOSTS=['desafiobackendejectdeploy.pythonanywhere.com']
SECRET_KEY='django-insecure-*zbc9)!(x*-(+3o6iq)68d+e6s9*tz#-d-m*$%g3o0tsex4tpo'
```

Para gerar uma `SECRET_KEY` nova:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
### Padrões de Código

- **PEP 8** para formatação Python
- **Docstrings** para funções e classes
- **Português** para nomes de domínio (models, campos, serializers, views), mantendo em inglês o que é sintaxe do framework (`Meta`, `ForeignKey`, `Serializer`...)


## 🧩 Correspondência entre Endpoints e Mockups
### 📋 Tabela de Referência - Login, cadastro e recuperar senha 
  ### Mockup completo: [Mockup NewStyle](https://www.figma.com/design/2x9GdF7zL0uiG6wDUVvAA8/Trainee-26.1---Back-end?node-id=0-1&p=f)
|Tela/Componente| Imagem | Descrição | Endpoint da API | Método HTTP |
|---|---|---|---|---|
| **Criar usuário** | <img width="523" height="426" alt="FIGMA_CADASTRO" src="https://github.com/user-attachments/assets/30171fa6-3ce8-40dc-862f-f4df4addf79b" /> | Cria um novo usuário por meio do registro de seus dados no sistema. | `/auth/register` | POST |
|**Login (obter token JWT)**| <img width="435" height="403" alt="FIGMA_LOGIN" src="https://github.com/user-attachments/assets/846e1d56-61bc-4642-b889-9b9b95d8198b" /> | Realiza o login do usuário e retorna o token de acesso (JWT). | `/auth/login` | POST |
| **🚨Recuperar senha (etapa 1)**| <img width="334" height="267" alt="FIGMA_RECUPERACAO_SENHA" src="https://github.com/user-attachments/assets/23a8acbd-5a4a-443c-ac3d-93026528e00b" /> | Envia o e-mail de redefinição de senha para o usuário que esqueceu a senha. | `/auth/forgot-password` | POST
|**🚨Recuperar senha (etapa 2)**| FOTO???? | Confirma a redefinição da senha usando o token enviado por e-mail e define a nova senha. | `/auth/reset-password` | POST



### 📋 Tabela de Referência - Inicio🚨???🚨 (COMPARAR COM SUA API USANDO FOTOS DO FIGMA)
### 📋 Tabela de Referência - Loja (COMPARAR COM SUA API USANDO FOTOS DO FIGMA)
### 📋 Tabela de Referência - Sobre Nós🚨???🚨 (COMPARAR COM SUA API USANDO FOTOS DO FIGMA)
## 🔍 Filtros e Buscas - API Theka (FAÇA PARA A SUA API)
### 📋 Filtros Disponíveis
A API NewStyle oferece diversos filtros para facilitar a busca e organização dos produtos. Abaixo estão os filtros disponíveis e como utilizá-los:
#### 🎯 Filtros Básicos
| Parâmetro | Tipo | Descrição | Exemplo |
|---|---|---|---|
| `category` | ID | Filtragem por categoria específica | `?category=1` |
| `min_price` | Decimal | Filtragem por preço maior ou igual ao número inserido | `min_price=70.00` |
| `max_price` | Decimal | Filtragem por preço menor ou igual ao número inserido | `max_price=90.00` |
#### 🔍 Busca por Texto
| Parâmetro |	Descrição |	Campos Pesquisados | Exemplo |
|---|---|---|---|
| `search` | Busca textual | Título do produto | `search=cargo+azul` | 
#### 📊 Ordenação
| Parâmetro |	Descrição |	Campos Disponíveis | Exemplo |
|---|---|---|---|
| 🚨???🚨 | 🚨???🚨 |🚨???🚨 | 🚨???🚨 | 
#### 📄 Paginação
| Parâmetro |	Descrição | Exemplo |
|---|---|---|
| `page` | Número da página | `?page=2` | 

## 🔐 Autenticação e Permissões
- **Endpoints de autenticação (`/auth/`)** — responsáveis por login, 🚨 recuperação🚨  e atualização de tokens JWT.  
- **Endpoints de usuários (`/users/`)** — permitem gerenciar contas e definir permissões específicas para cada usuário.
## 🧱 Estrutura do Projeto
```
Nome do Projeto/
├── api/                       # App da API: models, serializers, views e rotas
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
├── 🚨.env.example               # Modelo das variáveis de ambiente🚨
├── 🚨Dockerfile🚨
├── 🚨docker-compose.yml🚨
├── 🚨ruff.toml                  # Configuração do Ruff🚨
├── requirements.txt           # Dependências Python
├── manage.py                  # Utilitário Django
└── README.md                  # Este arquivo
```
## 🧑‍💻 Autor

### **Matheus Marçal**
### Trainee Backend | Estudante do Bacharelado em Ciências e Tecnologia 
### [GitHub](https://github.com/matheusmarcal-coder)
