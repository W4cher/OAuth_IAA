# 🔐 OAuth_IAA — Authentication Server (Identity Provider)

Servidor de autenticação centralizado (**Identity Provider**) desenvolvido em **Django REST Framework**, com emissão de tokens **JWT**, **autenticação de dois fatores (TOTP)**, proteção contra **ataques de força bruta** e **registo de auditoria** da atividade dos utilizadores.

Projeto académico da unidade curricular de IAA.

---

## ✨ Funcionalidades

| Área | Implementação |
|---|---|
| **Registo e login** | Registo de utilizadores e login por email (`EmailAuthBackend` + modelo `CustomUser`) |
| **Tokens JWT** | Emissão e renovação de tokens com `djangorestframework-simplejwt`, com **blacklist** de tokens revogados |
| **2FA (TOTP)** | Segundo fator com códigos temporários (`django-otp`, plugin TOTP) e QR code para apps autenticadoras |
| **Proteção contra força bruta** | Bloqueio após tentativas falhadas com `django-axes` |
| **Auditoria** | Registo da atividade dos utilizadores com `django-activity-stream` |
| **Emails transacionais** | Templates de login, confirmação e recuperação de password |

## 🧭 Endpoints

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/auth/` | Página de autenticação |
| `POST` | `/register/` | Registo de um novo utilizador |
| `POST` | `/login/` | Login |
| `POST` | `/token/` | Obter par de tokens JWT (access + refresh) |
| `POST` | `/token/refresh/` | Renovar o token de acesso |

---

## 🛠️ Tecnologias

Python · Django 5 · Django REST Framework · SimpleJWT · django-otp · django-axes · django-activity-stream · SQLite (desenvolvimento)

---

## 🚀 Como correr localmente

```bash
cd Auth_Server
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r Requirements.txt

cp .env.example .env              # e define a tua DJANGO_SECRET_KEY
export $(cat .env | xargs)        # Windows (PowerShell): define as variáveis manualmente

python manage.py migrate
python manage.py runserver
```

Para gerar uma `DJANGO_SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🔒 Notas de segurança

- A `SECRET_KEY` e o modo `DEBUG` são lidos de **variáveis de ambiente**: nenhum segredo fica no código.
- A base de dados local (`db.sqlite3`) **não** é versionada.
- Em produção: `DJANGO_DEBUG=False`, `ALLOWED_HOSTS` definido, HTTPS obrigatório e uma base de dados dedicada.

---

Autor: [Garcia Lisboa Mateus](https://github.com/W4cher)
