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


## CORS e header customizado multi-tenant
- O backend usa `django-cors-headers` com `CorsMiddleware` no topo da pilha de middlewares.
- `CORS_ALLOWED_ORIGINS` já inclui `https://condotools-frontend.onrender.com` e pode ser sobrescrito por env var.
- `CORS_ALLOWED_ORIGIN_REGEXES` também pode ser configurado por env var para cenários com subdomínios dinâmicos.
- O header `x-condominium-id` está liberado em `CORS_ALLOW_HEADERS`, permitindo preflight/OPTIONS para chamadas multi-tenant do frontend.

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

## UX padronizada e formulários guiados
- A tela de **Unidades** agora usa campos humanos: **Número da unidade**, **Bloco/Torre**, **Andar** e **Observações**.
- O campo técnico `code` foi mantido apenas para compatibilidade interna e é preenchido automaticamente (`Bloco-Número`).
- Formulários das entidades principais priorizam `select` para relacionamentos (ex.: unidade, morador, área comum), evitando digitação manual de IDs.

## Configurações (somente Admin da Plataforma)
A rota `/settings` foi reorganizada em abas:
1. **Condomínios**: CRUD simplificado com seleção de condomínio ativo.
2. **Usuários**: criação com dropdowns de **Perfil** e **Condomínio**.
3. **Assistente**: fluxo guiado em 3 passos:
   - Escolher/criar condomínio.
   - Criar primeiro síndico.
   - Criar unidades em lote por intervalo ou lista.

## Assistente (API)
- `POST /api/condominiums/wizard/setup/`: cria (ou usa) condomínio e cadastra o primeiro síndico.
- `POST /api/condominiums/{id}/bulk-units/`: criação em lote de unidades via intervalo (`mode=range`) ou lista (`mode=list`).


## RBAC (Permissões por Perfil)
- Catálogo oficial de permissões disponível em `GET /api/permissions/registry/`.
- Permissões efetivas do usuário logado em `GET /api/permissions/me/`.
- Configurações editáveis por perfil em `GET/POST/PATCH /api/role-permissions/` (somente `PLATFORM_ADMIN`).
- A aba **Permissões** em `/settings` permite editar toggles por role, salvar e restaurar padrão.
- O backend aplica bloqueio real por permissão (DRF). O frontend usa as permissões para ocultar menu, botões e rotas sem acesso.
