#!/usr/bin/env python3
"Fediverse Playground - GNU social v3"

from os import makedirs
from os.path import exists
from subprocess import Popen
import re

from util import variable_replacements_fn

def config(instance):
    "Configuration function for GNU social v3"
    if not exists('files/'):
        makedirs('files', exist_ok=True)

    if not exists(f"files/{instance['id']}.nginx.conf"):
        with open(f"files/{instance['id']}.nginx.conf", 'w') as f:
            with open(f"instances/{instance['id']}/docker/nginx/nginx.conf", 'r') as orig:
                s = orig.read()
                for reg, repl in [(r'%hostname%', instance['hostname']), (r'php:9000', f"{instance['id']}:9000"), (r'root /var/www/social', f"root /var/www/{instance['id']}")]:
                    s = re.sub(reg, repl, s)
                f.write(s)

    if not exists(f"files/{instance['hostname']}"):
        makedirs(f"files/{instance['hostname']}", exist_ok=True)

    if not exists(f"files/{instance['hostname']}/privkey.pem") or not exists(f"files/{instance['hostname']}/fullchain.pem"):
        with Popen([
                'openssl', 'req', '-x509', '-nodes', '-newkey', 'rsa:1024',
                '-days', '365', '-keyout', f"files/{instance['hostname']}/privkey.pem",
                '-out', f"files/{instance['hostname']}/fullchain.pem", '-subj', '/CN=localhost',
        ]) as p:
            p.communicate()

    if not exists(f"instances/{instance['id']}/.env.local"):
        with open(f"instances/{instance['id']}/.env.local", 'w') as f:
            f.write("""
DATABASE_URL=postgresql://postgres:fediverse-playground@db:5432/{instance['id']}
MAILER_DSN=sendmail://localhost
MESSENGER_TRANSPORT_DSN=sync://
""")

social_v3 = {
    'social-v3': {
        'display_name': 'GNU social v3',
        'dependencies': [
            { 'type': 'web', 'volumes': { './instances/{id}/public': '/var/www/{id}/public', '{config}': '/etc/nginx/conf.d/{config}', './files/{hostname}/': '/etc/letsencrypt/live/{hostname}' }},
            { 'type': 'db' },
            { 'type': 'redis' },
            { 'type': 'social-v3-php', 'container_name': '{id}', 'definition': (variable_replacements_fn("""
{id}:
    build: instances/{id}/docker/php
    restart: always
    tty: true
    environment:
        - SOCIAL_DBMS=postgres
        - DBMS=postgres
        - SOCIAL_DB={id}
        - SOCIAL_USER=postgres
        - POSTGRES_PASSWORD=fediverse-playground
        - SOCIAL_PASSWORD=fediverse-playground
        - CONFIG_DOMAIN={hostname}
        - CONFIG_NODE_NAME={instance_name}
        - SOCIAL_ADMIN_EMAIL=
        - SOCIAL_SITE_PROFILE=public
    volumes: {volumes}
        - ./instances/{id}:/var/www/social
        - ./instances/{id}/docker/php/entrypoint.sh:/entrypoint.sh
        - ./instances/{id}/docker/db/wait_for_db.sh:/wait_for_db.sh
        - ./instances/{id}/docker/social/install.sh:/var/entrypoint.d/social_install.sh
        - /var/www/social/docker
    command: /entrypoint.sh
                """, None), config),
            },
        ],
        'source': ('git@codeberg.org:GNUsocial/gnu-social.git', 'v3'),
    },
}
