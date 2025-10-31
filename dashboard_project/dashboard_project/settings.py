import os
from pathlib import Path

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# CONFIGURAÇÕES BÁSICAS
# ==========================================================
SECRET_KEY = "django-insecure-change-me-in-production"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# ==========================================================
# APLICAÇÕES INSTALADAS
# ==========================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "leitos",
]

# ==========================================================
# MIDDLEWARE
# ==========================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

# ==========================================================
# URLS E WSGI
# ==========================================================
ROOT_URLCONF = "dashboard_project.urls"
WSGI_APPLICATION = "dashboard_project.wsgi.application"
ASGI_APPLICATION = "dashboard_project.asgi.application"

# ==========================================================
# TEMPLATES
# ==========================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "dashboard_project" / "leitos" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# ==========================================================
# BANCO DE DADOS (SQLite)
# ==========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==========================================================
# INTERNACIONALIZAÇÃO
# ==========================================================
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ==========================================================
# ARQUIVOS ESTÁTICOS
# ==========================================================
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "leitos" / "static",
]

# ==========================================================
# PADRÕES
# ==========================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
