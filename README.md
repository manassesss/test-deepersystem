---

Este projeto implementa um sistema CRUD (Create, Read, Update, Delete) utilizando as melhores práticas do ecossistema Python (SOLID e Clean Code) no backend e VueJS 3 (Composition API) com PrimeVue no frontend. O sistema importa dados de um arquivo JSON para uma coleção de usuários no MongoDB e disponibiliza uma API REST para a aplicação frontend.

---

## Tabela de Conteúdos

- [Descrição do Projeto](#descrição-do-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Configuração do Backend](#configuração-do-backend)
- [Configuração do Frontend](#configuração-do-frontend)
- [Execução do Projeto](#execução-do-projeto)
- [Documentação da API (Swagger)](#documentação-da-api-swagger)
- [Rodando com Docker Compose](#rodando-com-docker-compose)
- [Funcionalidades](#funcionalidades)
- [Detalhes Técnicos](#detalhes-técnicos)
- [Dependências e Versões](#dependências-e-versões)
- [Considerações Finais](#considerações-finais)

---

## Descrição do Projeto

Este projeto é composto por duas partes:

1. **Backend:** 
   - Desenvolvido com Flask e MongoDB.
   - Utiliza uma estrutura modular baseada em princípios SOLID.
   - Possui um script (`parser.py`) para importar dados do arquivo `udata.json` para a coleção `users` do MongoDB.
   - Exibe uma API REST com endpoints para criação, listagem, atualização e exclusão de usuários.
   - Configuração via arquivo `.env` (utilizando `python-dotenv`) para facilitar o gerenciamento de variáveis de ambiente.
   - Documentação da API disponível via Swagger.

2. **Frontend:**
   - Desenvolvido com VueJS 3 (Composition API) e utiliza PrimeVue para os componentes da interface.
   - Contém duas páginas principais:
     - **Página Principal:** Exibe uma tabela com os usuários e ações para criar, editar e deletar.
     - **Página de Detalhes do Usuário:** Exibe as informações individuais e permite a edição e exclusão de um usuário.
   - Utiliza o Vite para o build e desenvolvimento.

---

## Estrutura do Projeto

```plaintext
project/
├── backend/
│   ├── app.py              # Entry point da API Flask
│   ├── config.py           # Configurações (uso do .env com python-dotenv)
│   ├── models.py           # Definição dos dataclasses User e UserPreferences
│   ├── parser.py           # Script para importar os dados do udata.json
│   ├── requirements.txt    # Dependências do backend com versões fixas
│   └── services/
│         └── user_service.py  # Lógica de negócio e acesso ao MongoDB
├── frontend/
│   ├── package.json        # Dependências e scripts do Node.js
│   ├── vite.config.js      # Configuração do Vite
│   ├── public/             # Arquivos estáticos
│   └── src/
│       ├── main.js         # Inicialização da aplicação VueJS
│       ├── App.vue         # Componente raiz do Vue
│       ├── router.js       # Configuração das rotas
│       └── components/
│           ├── UsersTable.vue   # Tabela de usuários e ações (CRUD)
│           ├── UserDetail.vue   # Página individual do usuário
│           └── UserForm.vue     # Formulário reutilizável para criação/edição (modal)
├── docker-compose.yml      # Arquivo para orquestrar os containers com Docker Compose
├── udata.json              # Arquivo JSON com os dados a serem importados
└── README.md               # Este arquivo
```

---

## Requisitos

- **Python 3.8+**
- **Node.js 14+**
- **Docker** e **Docker Compose**
- **MongoDB** (se for executado localmente sem Docker)

---

## Configuração do Backend

### 1. Instalação das Dependências

Navegue para a pasta `backend`:

```bash
cd backend
```

Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate      # Para Linux/Mac
venv\Scripts\activate         # Para Windows
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

### 2. Configuração das Variáveis de Ambiente

Crie um arquivo `.env` na pasta `backend` com o seguinte conteúdo:

```dotenv
MONGO_URI=mongodb://localhost:27017/mydatabase
```

O arquivo `config.py` utiliza a biblioteca `python-dotenv` para carregar as variáveis definidas nesse arquivo.

### 3. Importação dos Dados

Utilize o script `parser.py` para importar os dados do arquivo `udata.json` para a coleção `users` do MongoDB:

```bash
python parser.py
```

### 4. Execução do Servidor Flask

Inicie a API:

```bash
python app.py
```

O servidor estará disponível em: `http://localhost:5000`

---

## Configuração do Frontend

### 1. Instalação das Dependências

Navegue para a pasta `frontend`:

```bash
cd ../frontend
```

Instale as dependências do Node.js:

```bash
npm install
```

### 2. Execução do Servidor de Desenvolvimento

Inicie o servidor de desenvolvimento com:

```bash
npm run dev
```

O frontend estará disponível em: `http://localhost:3000` (ou conforme indicado no terminal).

---

## Execução do Projeto

1. **Backend:**
   - Configure o ambiente (virtualenv e .env).
   - Importe os dados com `parser.py`.
   - Inicie o servidor Flask.

2. **Frontend:**
   - Instale as dependências do Node.js.
   - Inicie o servidor de desenvolvimento com Vite.

A API e o frontend estão integrados via CORS, permitindo a comunicação entre as duas partes.

---

## Documentação da API (Swagger)

A documentação da API está disponível via Swagger, utilizando a biblioteca [Flasgger](https://github.com/flasgger/flasgger). Essa interface permite visualizar e testar os endpoints diretamente pelo navegador.

**Como acessar:**

Após iniciar o servidor Flask, acesse a URL:

```
http://localhost:5000/apidocs
```

Essa página exibirá a documentação interativa da API, permitindo testes e visualização dos parâmetros de cada endpoint.

---

## Rodando com Docker Compose

Para facilitar o ambiente de desenvolvimento e deploy, disponibilizamos um arquivo `docker-compose.yml` que orquestra os containers necessários:

1. **Pré-requisitos:**  
   Certifique-se de ter o [Docker](https://www.docker.com/) e o [Docker Compose](https://docs.docker.com/compose/) instalados em sua máquina.

2. **Arquivo `docker-compose.yml`:**

   Exemplo de conteúdo:

   ```yaml
   version: '3.8'
   services:
     backend:
       build: ./backend
       container_name: backend
       env_file: ./backend/.env
       ports:
         - "5000:5000"
       depends_on:
         - mongo
     frontend:
       build: ./frontend
       container_name: frontend
       ports:
         - "3000:3000"
     mongo:
       image: mongo:latest
       container_name: mongo
       restart: always
       ports:
         - "27017:27017"
       volumes:
         - mongo_data:/data/db

   volumes:
     mongo_data:
   ```

3. **Construção e execução dos containers:**

   No diretório raiz do projeto, execute:

   ```bash
   docker-compose up --build
   ```

   Este comando fará o build dos containers do backend e frontend, iniciará o MongoDB e orquestrará a comunicação entre eles.

4. **Acessando a aplicação:**
   - **Backend:** `http://localhost:5000`
   - **Swagger (Documentação da API):** `http://localhost:5000/apidocs`
   - **Frontend:** `http://localhost:3000`

---

## Funcionalidades

### Backend

- **Importação de Dados:** Lê o arquivo `udata.json` e importa os dados para a coleção `users` do MongoDB.
- **API REST:**
  - **GET /users:** Lista todos os usuários.
  - **GET /users/<username>:** Retorna os detalhes de um usuário específico.
  - **POST /users:** Cria um novo usuário.
  - **PUT /users/<username>:** Atualiza os dados de um usuário.
  - **DELETE /users/<username>:** Deleta um usuário.

### Frontend

- **Página Principal:** 
  - Exibe uma tabela com os usuários, incluindo colunas para username, roles, timezone, status ativo, data de criação e ações.
  - Ações de edição e exclusão com confirmação.
  - Botão para criar um novo usuário, que abre um modal com o formulário.
  
- **Página de Detalhes do Usuário:**
  - Exibe as informações completas do usuário.
  - Permite edição e exclusão diretamente na página.

---

## Detalhes Técnicos

- **Princípios SOLID e Clean Code:**  
  O projeto segue a separação de responsabilidades, com a lógica de acesso a dados isolada na camada de serviços (`user_service.py`) e a definição dos modelos utilizando `dataclasses`.

- **Uso do `python-dotenv`:**  
  As configurações do MongoDB são carregadas de um arquivo `.env`, facilitando o gerenciamento das variáveis de ambiente.

- **Controle de Dependências:**  
  As versões das dependências estão fixadas no arquivo `requirements.txt` para evitar incompatibilidades. Em especial, o Werkzeug foi fixado na versão 2.0.3 para evitar o erro relacionado à função `url_quote`.

- **Integração Backend-Frontend:**  
  A API Flask está configurada com CORS para permitir que o frontend VueJS se comunique sem restrições.

---

## Dependências e Versões

Arquivo `backend/requirements.txt`:

```txt
Flask==2.1.3
Werkzeug==2.0.3
pymongo==4.3.3
flask-cors==3.0.10
python-dotenv==0.21.0
flasgger==0.9.5
```

Arquivo `frontend/package.json`:

```json
{
  "name": "crud-vue-flask",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  },
  "dependencies": {
    "vue": "^3.2.0",
    "vue-router": "^4.0.0",
    "primevue": "^3.10.0",
    "primeicons": "^5.0.0"
  },
  "devDependencies": {
    "vite": "^3.0.0"
  }
}
```

---

## Considerações Finais

- **Modularidade e Manutenibilidade:**  
  A estrutura do projeto facilita a manutenção e futuras expansões, permitindo que cada parte seja evoluída de forma independente.

- **Facilidade de Uso:**  
  As instruções detalhadas permitem que qualquer usuário, mesmo sem conhecimento prévio sobre o projeto, possa instalá-lo e executá-lo corretamente.

- **Melhores Práticas:**  
  O código segue os princípios SOLID e Clean Code, garantindo legibilidade, modularidade e separação clara das responsabilidades.

Caso haja dúvidas ou sugestões de melhoria, sinta-se à vontade para contribuir com o projeto ou abrir uma issue no repositório.

---