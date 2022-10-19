#!/usr/bin/env python3
"Fediverse Playground - GNU social v2"

def config():
    "Configuration function for GNU social v2"

social_v2 = {
    'social-v2': {
        'display_name': 'GNU social v2',
        'dependencies': [
            { 'type': 'web' },
            { 'type': 'db' },
            { 'type': 'php' },
        ],
        'config': config,
        'source': ('git@codeberg.org:GNUsocial/gnu-social.git', 'nightly'),
    }
}
