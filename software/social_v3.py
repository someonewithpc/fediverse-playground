#!/usr/bin/env python3
"Fediverse Playground - GNU social v3"

def config():
    "Configuration function for GNU social v3"

social_v3 = {
    'social-v3': {
        'display_name': 'GNU social v3',
        'dependencies': [
            { 'type': 'web', 'volumes': { './public': '/var/www/social/public', '{config}': '/var/nginx/{config}' }},
            { 'type': 'db' },
            { 'type': 'php', 'container_name': '{id}', 'volumes': { './docker/social/install.sh': '/etc/entrypoint.d/social_install.sh', './software/social-v3': '/var/www/{id}' } },
        ],
        'config': config,
        'docker-image': 'build: docker/php',
        'source': ('git@codeberg.org:GNUsocial/gnu-social.git', 'v3'),
    },
}
