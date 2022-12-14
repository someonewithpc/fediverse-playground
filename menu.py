#!/usr/bin/env python

import sys
from subprocess import Popen
from os import makedirs, path

from whiptail import Whiptail

from software import SOFTWARE
from util import snake_case
from util.config import load_config, write_config

w = Whiptail(title="Fediverse Playground", backtitle="Fediverse Playground", height=0, width=0)
config = load_config()

def add_or_edit(kind):
    """Add or Edit an entry"""
    def inner():
        first_prompt = []
        rc = 0
        if kind == 'add':
            first_prompt, rc = w.menu(
                msg='Which software would you like to add?',
                items=list(zip(SOFTWARE.keys(), [SOFTWARE[soft]['display_name'] for soft in SOFTWARE])),
            )
        else:
            instance_id, rc = w.menu(
                msg='Which instance would you like to edit?',
                items=list(zip([inst['instance_id'] for inst in config], [f"{inst['instance_type']} - {inst['name']}" for inst in config]))
            )
            first_prompt = [idx for idx, inst in enumerate(config) if inst['instance_id'] == instance_id][0]

        if first_prompt == '' or rc != 0:
            sys.exit('Invalid instance type')

        hostname, rc = w.inputbox(
            msg='What hostname should this instance be available under?',
            default='.localhost' if kind == 'add' else config[first_prompt]['hostname']
        )
        if hostname == '' or rc != 0:
            sys.exit('Invalid hostname')

        name, rc = w.inputbox(
            msg='What should this instance be called?',
            default='' if kind == 'add' else config[first_prompt]['name'],
        )
        if name == '' or rc != 0:
            sys.exit('Invalid name')

        instance_id, rc = w.inputbox(
            msg='What name should the Docker containers use?',
            default=snake_case(name) if kind == 'add' else config[first_prompt]['instance_id'],
        )
        if instance_id == '' or rc != 0:
            sys.exit('Invalid ID')

        instance_type = first_prompt if kind == 'add' else config[first_prompt]['instance_type']

        source, rc = w.inputbox(
            msg=f"Where would you like to fetch '{SOFTWARE[instance_type]['display_name']}'?",
            default=SOFTWARE[instance_type]['source'][0] if kind == 'add' else config[first_prompt]['source'][0]
        )
        if source == '' or rc != 0:
            sys.exit('Invalid source')

        reference, rc = w.inputbox(
            msg=f"What reference would you like to use for '{SOFTWARE[instance_type]['display_name']}'?",
            default=SOFTWARE[instance_type]['source'][1] if kind == 'add' else config[first_prompt]['source'][1]
        )
        if reference == '' or rc != 0:
            sys.exit('Invalid reference')


        if kind == 'edit':
            config.pop(first_prompt)
            print(f"Edited {instance_type} - {instance_id}")
        else:
            print(f"Added {instance_type} - {instance_id}")

        config.append({'instance_type': instance_type, 'hostname': hostname, 'name': name, 'instance_id': instance_id, 'source': (source, reference)})

    return inner

def clone():
    makedirs('instances', exist_ok=True)
    local_clones = [f"instances/{inst['instance_id']}" for inst in config if path.exists(f"instances/{inst['instance_id']}")]

    for inst in config:
        if not path.exists(f"instances/{inst['instance_id']}"):
            p = Popen(['git', 'clone', inst['source'][0], f"instances/{inst['instance_id']}", '--dissociate', *[part for lc in local_clones for part in ['--reference', lc]]])
            out, err = p.communicate()

def dump_config():
    write_config(config)
    print('Wrote `docker-compose.yaml`')

def do_exit():
    global run
    run = False
    write_config(config)
    print('Exiting...')

run = True
while run:
    w.title = "Fediverse Playground"

    msg = f"Added {len(config)} config" if len(config) > 0 else 'No config'
    selection, rc = w.menu(msg=msg, items=['Add an Instance', 'Edit an Instance', 'Clone Software', 'Dump `docker-compose.yaml`', 'Exit'])

    if rc != 0:
        print('Cancelling')
        break

    w.title = selection

    {
        'Add an Instance': add_or_edit('add'),
        'Edit an Instance': add_or_edit('edit'),
        'Clone Software': clone,
        'Dump `docker-compose.yaml`': dump_config,
        'Exit': do_exit,
    }[selection]()
