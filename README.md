# Fediverse Playground

## Run multiple Fediverse Software locally, for development

> Note that this is not necessarily a production ready system, it's very likely
> some things are unsafely configured

A common problem when developing federated software is the need to test for
compatibility with other such software. This leads developers to test their
software against semi-random publicly available instances of their or other
software. This is not ideal since then developers may not have access to logs,
or to make changes, which slows down development. This project aims to solve
that by allowing you to run as many copies of each software locally.

## Supported software

 - GNU social v3
 - GNU social v2 (WIP)
 
Feel free to contribute your software! More will be added, such as GoToSocial,
Lemmy or Mastodon
 
## Setup ('installation')

This project uses Python for the configuration, and `docker` and/or `docker-compose` to run the containers. 

It's recommended you create a [Virtual Environment](https://docs.python.org/3/library/venv.html) with:

``` sh
python -m venv venv
```

and then you can run

```sh
source venv/bin/activate
```

If you prefer to use another method, the following dependencies are required:
    
    - whiptail

which can be installed with

```sh
pip install whiptail-dialog
```

Then, run

```sh
./configure
```

And follow the prompts. You can add and edit the instances you selected, which
get saved such that if you exit, you can rerun `configure` at any point, to
further modify your configuration, as well as dump the updated
`docker-compose.yml` file.

After configuring the instances you want, you need to select the `'Clone
Software'` option.

Simply add as many instances of each software as you desire and then run

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
