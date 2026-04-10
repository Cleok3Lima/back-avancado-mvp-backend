# Diário de Episódios — Rick & Morty API

API REST construída com **FastAPI** e **SQLite** para gerenciar um diário pessoal de episódios da série Rick and Morty.

---

## Arquitetura

```
┌─────────────────┐        REST/JSON        ┌──────────────────────────┐
│  Frontend React  │ ──────────────────────► │   Backend FastAPI (8000)  │
└─────────────────┘                          └───────────┬──────────────┘
                                                         │
                                          ┌──────────────┴──────────────┐
                                          │                              │
                                   ┌──────▼──────┐            ┌─────────▼────────┐
                                   │  SQLite DB   │            │  Rick & Morty API │
                                   │  diario.db   │            │  rickandmortyapi  │
                                   └─────────────┘            └──────────────────┘
```

---

## Pré-requisitos

- Python 3.11+
- pip
- Docker (opcional)

---

## Como rodar localmente

### Sem Docker

```bash
# 1. Clone o repositório
git clone <url-do-repo>
cd back-avancado-mvp-backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Inicie o servidor
uvicorn main:app --reload
```

A API estará disponível em: **http://localhost:8000**
Documentação Swagger em: **http://localhost:8000/docs**

### Com Docker

```bash
# Build da imagem
docker build -t rickmorty-api .

# Rodar o container
docker run -p 8000:8000 rickmorty-api
```

---

## Rotas disponíveis

### Autenticação

| Método | Rota               | Autenticação | Descrição                                  |
|--------|--------------------|--------------|--------------------------------------------|
| `POST` | `/auth/register`   | Não          | Cadastra novo usuário                      |
| `POST` | `/auth/login`      | Não          | Faz login e retorna token JWT              |
| `GET`  | `/auth/me`         | Bearer JWT   | Retorna dados do usuário autenticado       |

### Diário *(requer Bearer JWT)*

| Método   | Rota              | Descrição                                         |
|----------|-------------------|---------------------------------------------------|
| `GET`    | `/diario`         | Lista entradas do diário do usuário autenticado   |
| `POST`   | `/diario`         | Cria uma nova entrada no diário                   |
| `PUT`    | `/diario/{id}`    | Atualiza nota e/ou avaliação de uma entrada       |
| `DELETE` | `/diario/{id}`    | Remove uma entrada do diário                      |

### Episódios *(públicos)*

| Método | Rota              | Descrição                                            |
|--------|-------------------|------------------------------------------------------|
| `GET`  | `/`               | Health check — verifica se a API está no ar          |
| `GET`  | `/episodios`      | Lista episódios paginados; aceita `?season=1..5` para filtrar por temporada  |
| `GET`  | `/episodios/{id}` | Retorna detalhes do episódio + personagens completos |

### Parâmetros de query em `GET /diario`

| Parâmetro   | Tipo    | Padrão              | Descrição                                                                                     |
|-------------|---------|---------------------|-----------------------------------------------------------------------------------------------|
| `page`      | int     | `1`                 | Página atual                                                                                  |
| `limit`     | int     | `10`                | Itens por página (máx. 100)                                                                   |
| `avaliacao` | int     | *(opcional)*        | Filtrar entradas por avaliação (1 a 5)                                                        |
| `order_by`  | string  | `created_at_desc`   | `created_at_desc`, `created_at_asc`, `avaliacao_desc` ou `avaliacao_asc`                      |

---

## API Externa

| Campo             | Valor                                             |
|-------------------|---------------------------------------------------|
| **Nome**          | The Rick and Morty API                            |
| **URL**           | https://rickandmortyapi.com                       |
| **Licença**       | MIT                                               |
| **Cadastro**      | Não necessário — API pública e gratuita           |
| **Autenticação**  | Nenhuma                                           |

### Rotas utilizadas

| Rota                                            | Descrição                              |
|-------------------------------------------------|----------------------------------------|
| `GET /api/episode?page={n}`                     | Lista de episódios paginada            |
| `GET /api/episode/{id}`                         | Detalhes de um episódio específico     |
| `GET /api/character/{ids}`                      | Dados de múltiplos personagens por ID  |

---

## Estrutura de arquivos

```
back-avancado-mvp-backend/
├── Dockerfile
├── requirements.txt
├── README.md
├── main.py           # Ponto de entrada, configuração CORS e registro de routers
├── database.py       # Engine SQLAlchemy, SessionLocal, Base, get_db
├── models.py         # Modelos ORM: DiarioEntry e User
├── schemas.py        # Schemas Pydantic (diário + auth)
├── security.py       # Hash de senha (bcrypt) e geração/validação de JWT
├── dependencies.py   # Dependência get_current_user (valida Bearer token)
└── routers/
    ├── __init__.py
    ├── auth.py      # Rotas de cadastro, login e /me
    ├── diario.py    # Rotas CRUD do diário (protegidas por JWT)
    └── episodios.py # Rotas que consomem a API do Rick and Morty (públicas)
```
