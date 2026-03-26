# Briefing de Logomarca - Flask + Railway

Projeto mobile-first para coleta de briefing de logomarca, com visual moderno estilo agência de marketing.

## Recursos

- Formulário público em múltiplas etapas
- Múltipla escolha quando necessário
- Upload múltiplo de imagens de referência
- Respostas salvas em Postgres
- Painel admin para login, listagem e visualização dos briefings
- Upload persistente em `/data/uploads` para Railway Volume
- Layout moderno, responsivo e com foco em mobile

## Stack

- Flask
- SQLAlchemy
- Flask-Migrate
- PostgreSQL
- HTML + CSS + JS

## Como rodar localmente

1. Crie e ative um ambiente virtual
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

4. Configure o `.env`
5. Rode as migrações e suba o app:

```bash
flask db init
flask db migrate -m "init"
flask db upgrade
python seed_admin.py
python run.py
```

## Deploy no Railway

### Variáveis de ambiente

Configure no Railway:

- `SECRET_KEY`
- `DATABASE_URL`
- `ADMIN_NAME`
- `ADMIN_EMAIL`
- `ADMIN_PASSWORD`
- `UPLOAD_ROOT=/data/uploads`
- `MAX_CONTENT_LENGTH_MB=30`

### Volume

Crie um volume no Railway e monte em:

```bash
/data
```

O sistema criará automaticamente:

```bash
/data/uploads/reference_images
```

## Admin

Acesse:

- `/admin/login`
- `/admin`

Crie o admin inicial com:

```bash
python seed_admin.py
```

## Estrutura

```bash
app/
  admin/
  public/
  static/
  templates/
  __init__.py
  models.py
  utils.py
migrations/
run.py
wsgi.py
seed_admin.py
```
