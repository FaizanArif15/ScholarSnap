# 📚 ScholarSnap

**ScholarSnap** is an intelligent automation system that fetches, summarizes, and emails the latest research papers from [arXiv](https://arxiv.org) using AI.  
It integrates **Celery**, **Redis**, **PostgreSQL**, and **Gmail API** — orchestrated with **Docker Compose** — to run fully automated research updates every few minutes.

---

## 🚀 Features

✅ Fetches latest research papers from arXiv automatically  
✅ Extracts and saves PDFs with metadata  
✅ Generates AI-based paper summaries using LangChain + OpenAI  
✅ Sends summarized emails through Gmail API  
✅ Manages schedules using Celery Beat  
✅ Uses PostgreSQL as persistent storage  
✅ Built with Docker for simple deployment  

---

## 🏗️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | Python 3.12 |
| **Task Queue** | Celery |
| **Scheduler** | Celery Beat |
| **Database** | PostgreSQL |
| **Cache & Broker** | Redis |
| **Email API** | Gmail API |
| **Containerization** | Docker & Docker Compose |
| **Process Manager** | Supervisor |

---

## ⚙️ Prerequisites

Before starting, make sure you have installed:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.12+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (for local dependency management)

---

## 🧩 Environment Setup

Create a `.env` file in the project root:

```bash
# OpenAPI key
OPENAI_API_KEY=

# PostgreSQL
DB_HOST=db
DB_PORT=5432
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_CT_NAME=postgres # db container name

# Emails
EMAIL_SENDER=
EMAIL_RECIPIENTS=

# Redis
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
INTERVAL_MINUTES=5

# Container
CT_NAME=scholarsnap_app
```

---

## 🐳 Run with Docker

To build and start all services:

```bash
docker compose up -d --build
```

This will start:

- `scholarsnap` (main app)
- `db` (PostgreSQL)
- `redis` (Redis server)

To view logs:

```bash
docker compose logs -f scholarsnap
```

To stop everything:

```bash
docker compose down
```

---

## 🧠 Local Development (Without Docker)

If you prefer to run it locally:

```bash
uv sync
uv run main.py
```

Start Celery worker:
```bash
uv run celery -A celery_app worker --loglevel=INFO
```

Start Celery beat scheduler:
```bash
uv run celery -A celery_app beat --loglevel=INFO
```

---

## 🗃️ Accessing the Database

### 🖥️ Via pgAdmin

If pgAdmin is installed locally:
| Field | Value |
|--------|--------|
| **Host** | `127.0.0.1` |
| **Port** | `5432` |
| **Database** | `` |
| **Username** | `` |
| **Password** | `` |

Make sure `ports: - "5432:5432"` is added in your `docker-compose.yml` for the `db` service.


## ⚡ Troubleshooting

| Issue | Solution |
|--------|-----------|
| `Error: connection refused` | Ensure PostgreSQL container is running and port `5432` is exposed |
| `Cannot connect to redis:6379` | Verify Redis is running and accessible from Celery |
| `Permission denied (.venv)` | Delete `.venv` folder and re-run `uv sync` |
| `SSL: CERTIFICATE_VERIFY_FAILED` | Ensure valid SSL certificates or disable verification for Gmail API (dev only) |

---

## 🧩 Project Structure

```
ScholarSnap/
├── agent.py                      # Main logic to fetch, summarize, and email papers
├── arxiv.py                      # Handles paper fetching from arXiv API
├── celery_app.py                 # Celery + Beat configuration and scheduling
├── db.py                         # Database initialization and queries
├── tasks.py                      # Celery tasks (runs agent as async job)
├── gmail_service.py              # Gmail API service initialization and send emails
├── gmail_auth.py                 # Manual Gmail token generation script
├── main.py                       # Main scheduler (used outside Celery)
├── Dockerfile                    # Docker image setup for ScholarSnap
├── docker-compose.yml            # Multi-service orchestration (App + DB + Redis)
├── supervisord.conf              # Process manager for Celery worker & beat
├── supervisord.log / .pid        # Supervisor runtime files
├── pyproject.toml                # Project dependencies and metadata (for uv)
├── uv.lock                       # Locked dependency versions
├── LICENSE                       # License file
├── README.md                     # Documentation (this file)
├── credentials.json              # Google OAuth credentials file
├── token.json                    # Generated Gmail token
├── celerybeat-schedule           # Celery beat schedule database
├── arxiv_papers/                 # Folder containing downloaded research papers
│   └── ABC....pdf
├── flower_data/                  # Flower dashboard data (optional)
├── flower_db/                    # Flower DB files (optional)
├── logs/                         # Log folder (Supervisor-managed)
│   ├── celery_beat.err.log
│   ├── celery_beat.out.log
│   ├── celery_worker.err.log
│   ├── celery_worker.out.log
│   ├── flower_dash.err.log
│   └── flower_dash.out.log
├── __pycache__/                  # Compiled Python bytecode
│   ├── agent.cpython-312.pyc
│   ├── arxiv.cpython-312.pyc
│   ├── celery_app.cpython-312.pyc
│   ├── db.cpython-312.pyc
│   ├── gmail_service.cpython-312.pyc
│   ├── main.cpython-312.pyc
│   └── tasks.cpython-312.pyc

```
---

## 📨 Manual Gmail Token Generation (for local runs)

> ⚠️ Gmail authentication does **not** work automatically inside Docker containers because it requires a browser login.  
> You must generate the token **manually** before running Docker.

### Steps:

1. Make sure `credentials.json` (downloaded from Google Cloud Console) is in your project folder.  
2. Run the following command **locally (not inside Docker)**:

```bash
uv run gmail_auth.py
```

---

## 🧑‍💻 Author

👤 **Faizan Arif**  
📧 Email: [faizanarif1884@gmail.com](mailto:faizanarif1884@gmail.com)  
🌐 GitHub: [github.com/FaizanArif15](https://github.com/FaizanArif15)

---

## 🪄 License

This project is licensed under the **MIT License** — free to use and modify with attribution.

---

