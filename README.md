# Fediverse Playground

## Run multiple Fediverse Software locally, for development

Note that this is not necessarily a production ready system, it's very likely
some things are unsafely configured


## Supported software

 - GNU social v3
 - GNU social v2 (WIP)
 
## Setup ('installation')

This project uses Python for the configuration, and `docker` and/or `docker-compose` to run the containers. 

There's a virtual environment available, so you can run

```sh
./venv/bin/activate
```

Or install the following dependencies:
    
    - whiptail

with

```sh
pip install whiptail
```

Then, run

```sh
./configure
```

And follow the prompts. Simply add as many instances of each software as you desire and then run

```sh
docker-compose up -d
```

or

```sh
docker compose up -d
```

in newer versions of `docker`

The instances you configured should all be accessible in your browser under the
domains you specified (you may need to edit your `/etc/hosts` if you didn't use
`.localhost` domains)

## Contributing

Define your software in `software/` and it should automatically show up in the
interface and be configured correctly. Currently, this tool supports only
`nginx`, `postgres` and `redis` for shared services. Feel free to add your
dependencies to `software/services.py` if it makes sense for them to be shared
among multiple instances and with other software.
