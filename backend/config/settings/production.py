from .base import *  # noqa
import os

DEBUG = False

render_host = os.getenv("RENDER_EXTERNAL_HOSTNAME")
if render_host:
    ALLOWED_HOSTS.append(render_host)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

frontend_origin = "https://condotools-frontend.onrender.com"
if frontend_origin not in CORS_ALLOWED_ORIGINS:
    CORS_ALLOWED_ORIGINS.append(frontend_origin)

CORS_ALLOWED_ORIGIN_REGEXES = [
    *CORS_ALLOWED_ORIGIN_REGEXES,
    *[x.strip() for x in os.getenv("CORS_ALLOWED_ORIGIN_REGEXES", "").split(",") if x.strip()],
]
