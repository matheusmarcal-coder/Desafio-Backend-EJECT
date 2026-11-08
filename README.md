## 🛍️ NewStyle 
### Objetivo e funcionalidades principais do projeto: 
🚨???🚨🚨???🚨🚨???🚨🚨???🚨
## 🌐 Acesso
- API Base:
- Documentação Interativa (Swagger): 🚨???🚨🚨???🚨🚨???🚨🚨???🚨
  obs: "Documentação da API: Instruções para acessar o Swagger com
detalhes dos endpoints."
## Modelo Conceitual de Dados  🚨???🚨🚨???🚨
<img width="918" height="1666" alt="3 2 Modelo Conceitual - Desafio Backend 2026 2 - Matheus Marçal" src="https://github.com/user-attachments/assets/045a23e1-30ad-4641-a6b2-8476d0ba81ab" />

## ⚙️ Instalação e Execução 
### Passo a passo para configurar a instalação:
🚨NAO ESQUECER AS SEEDS🚨


## 🧰 Tecnologias Utilizadas
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
|`drf_yasg` -> Versão 1.21.18 | Geração de documentação interativa Swagger |
## 🏗️ Estrutura e Organização
🚨???🚨🚨???🚨🚨???🚨🚨???🚨
### 📖 Biblioteca (FAÇA PARA A SUA API)
🚨???🚨🚨???🚨🚨???🚨🚨???🚨 e veja se precisa disso mesmo
### 🏢 Institucional (FAÇA PARA A SUA API)
🚨???🚨🚨???🚨🚨???🚨🚨???🚨 e veja se precisa disso mesmo
## 🧩 Correspondência entre Endpoints e Mockups
### 📋 Tabela de Referência - Login, cadastro e recuperar senha 
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
## 🧱 Estrutura do Projeto
## 🧑‍💻 Autor
