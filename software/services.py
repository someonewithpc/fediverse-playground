#!/usr/bin/env python3

from util import variable_replacements_fn

SERVICES = {
    'web': variable_replacements_fn(
        """
web:
    {image}
    depends_on: {deps}
    restart: always
    tty: false
    ports:
        - "80:80"
        - "443:443"
    volumes: {volumes}
        - ./docker/web/nginx.conf:/var/nginx/nginx.conf
        """,
        'image: nginx:alpine',
    ),

    'db': variable_replacements_fn(
        """
db:
    {image}
    restart: always
    tty: false
    environment:
        - PGDATA=/var/lib/postgres/data
    volumes: {volumes}
        - database:/var/lib/postgres/data
        """,
        'image: postgres:alpine'
    ),
}