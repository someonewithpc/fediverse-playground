#!/usr/bin/env python3
"Fediverse Playground - GNU social v3"

from util import variable_replacements_fn

def config():
    "Configuration function for GNU social v3"

social_v3 = {
    'social-v3': {
        'display_name': 'GNU social v3',
        'dependencies': [
            { 'type': 'web', 'volumes': { './public': '/var/www/social/public', '{config}': '/var/nginx/{config}' }},
            { 'type': 'db' },
            { 'type': 'social-v3-php', 'container_name': '{id}', 'definition': variable_replacements_fn("""
{id}:
    build: docker/php
    restart: always
    tty: true
    container_name: {container_name}
    volumes: {volumes}
        - ./software/social-v3/source:/var/www/social
        - ./docker/social/install.sh:/etc/entrypoint.d/social_install.sh
        - ./docker/php/entrypoint.sh:/bin/entrypoint.sh
        - ./docker/db/wait_for_db.sh:/bin/wait_for_db.sh
    command: /entrypoint.sh
                """, None),
            },
        ],
        'config': config,
        'source': ('git@codeberg.org:GNUsocial/gnu-social.git', 'v3'),
    },
}
