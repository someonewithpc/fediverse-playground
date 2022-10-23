#!/usr/bin/env python3

from os import makedirs
from os.path import exists
from subprocess import Popen
from util import variable_replacements_fn

def web_config(instance):
    if not exists('files/'):
        makedirs('files', exist_ok=True)

    if not exists('files/nginx.conf'):
        with open('files/nginx.conf', 'w') as f:
            f.write("""
events {
  worker_connections  4096;  ## Default: 1024
}

http {
  include   /etc/nginx/vhosts/*.conf;
}
 """)


    if not exists('files/letsencrypt/'):
        makedirs('files/letsencrypt', exist_ok=True)

    if not exists('files/letsencrypt/options-ssl-nginx.conf'):
        with Popen(['curl', '-s', 'https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf', '-o', 'files/letsencrypt/options-ssl-nginx.conf']) as p:
            pass

    if not exists('files/letsencrypt/ssl-dhparams.pem'):
        with Popen(['curl', '-s', 'https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem', '-o', 'files/letsencrypt/ssl-dhparams.pem']) as p:
            pass

def db_config(instance):
    pass

SERVICES = {
    'web': (variable_replacements_fn(
        """
web:
    {image}
    restart: always
    tty: false
    ports:
        - "80:80"
        - "443:443"
    volumes: {volumes}
        - ./files/nginx.conf:/etc/nginx/nginx.conf
        - ./files/letsencrypt/options-ssl-nginx.conf:/etc/letsencrypt/options-ssl-nginx.conf
        - ./files/letsencrypt/ssl-dhparams.pem:/etc/letsencrypt/ssl-dhparams.pem
        """,
        'image: nginx:alpine',
    ), web_config),

    'db': (variable_replacements_fn(
        """
db:
    {image}
    restart: always
    tty: false
    environment:
        - PGDATA=/var/lib/postgres/data
        - POSTGRES_PASSWORD=fediverse-playground
        - POSTGRES_USER=postgres
    volumes: {volumes}
        - database:/var/lib/postgres/data
        """,
        'image: postgres:alpine'
    ), db_config),
}
