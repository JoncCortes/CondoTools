# CondoTools Monorepo

Monorepo com backend Django/DRF (multi-tenant) e frontend React/Vite, pronto para deploy no Render.

## Estrutura

```text
/
  backend/
  frontend/
  render.yaml
  README.md
```

## Variáveis de ambiente

### Backend (Render Web Service)
- `SECRET_KEY`
- `DEBUG` (`False` em produção)
- `DATABASE_URL` (fornecida pelo banco Postgres do Render)
- `CORS_ALLOWED_ORIGINS` (ex.: URL do frontend no Render)
- `RENDER_EXTERNAL_HOSTNAME` (host público do backend no Render)
- `DJANGO_SETTINGS_MODULE` (`config.settings.production` no Render)
- `ALLOWED_HOSTS` (opcional; padrão local `localhost,127.0.0.1`)

### Frontend (Render Static Site)
- `VITE_API_URL` (ex.: `https://<backend>.onrender.com/api`)

## Backend local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
export $(cat .env | xargs)
python manage.py migrate
python manage.py seed
python manage.py runserver
```

## Frontend local

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

## Deploy no Render (Blueprint)

1. Faça push do repositório para o GitHub.
2. No Render: **New + Blueprint** e selecione o repositório.
3. O `render.yaml` criará:
   - **Postgres Database** (`condotools-db`)
   - **Backend Web Service** (Django + Gunicorn)
   - **Frontend Static Site** (Vite build)
4. O backend usa no build:
   - `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
5. O backend inicia com:
   - `gunicorn config.wsgi:application`
6. O frontend builda com:
   - `npm ci && npm run build`
   e publica `dist`.

## Pós-deploy: migrations e seed

Após o primeiro deploy do backend no Render:

1. Abra o **Shell** do serviço backend.
2. Rode:

```bash
python manage.py migrate
python manage.py seed
```

> Observação: o `buildCommand` já executa `migrate`; esses comandos acima são úteis para reaplicar/manualmente e para seed inicial.

## Endpoints úteis

- JWT login: `POST /api/auth/token/`
- JWT refresh: `POST /api/auth/token/refresh/`
- Swagger: `/api/docs/`
- OpenAPI schema: `/api/schema/`
