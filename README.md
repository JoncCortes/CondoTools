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
- `DATABASE_URL`
- `CORS_ALLOWED_ORIGINS`
- `RENDER_EXTERNAL_HOSTNAME`
- `DJANGO_SETTINGS_MODULE` (`config.settings.production`)
- `ALLOWED_HOSTS` (opcional)

### Frontend
- `VITE_API_URL` (ex.: `https://<backend>.onrender.com/api`)

## Rodar local

### Backend
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

### Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

## Login seed
- `admin@platform.com` / `123456`
- `sindico@aurora.com` / `123456`
- `porteiro@aurora.com` / `123456`
- `morador@aurora.com` / `123456`

## Condomínio ativo (PLATFORM_ADMIN)
- No topo do app existe um seletor “Condomínio ativo”.
- Essa seleção é persistida no `localStorage`.
- O frontend envia `X-CONDOMINIUM-ID` automaticamente para recursos condo-scoped.
- Sem condomínio ativo, páginas condo-scoped ficam vazias e operações de criação retornam erro claro.

## Deploy Render
1. Push no GitHub
2. New + Blueprint
3. O `render.yaml` cria Postgres + backend + frontend static.
4. Build backend executa install + collectstatic + migrate.
5. Build frontend executa `npm ci && npm run build` e publica `dist`.

## Pós deploy
No Shell do backend:
```bash
python manage.py migrate
python manage.py seed
```
