#!/usr/bin/env python3

from re import sub

def format_array_dc(arr):
    return ("\n        - " if len(arr) > 0 else '') + "\n        - ".join(arr)

def variable_replacements_fn(s, default_image):
    def inner(id, deps, volumes, instance_name, hostname, image=None):
        return s.format(
            id=id,
            deps=format_array_dc(deps),
            volumes=format_array_dc(volumes),
            container_name=f"{id}-php" if id else 'php',
            image=image if image is not None else default_image,
            instance_name=instance_name,
            hostname=hostname,
        )
    return inner

def snake_case(s):
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()

def indent(mlstr, level = 1, width = 4):
    return '\n'.join(map(lambda l: (' ' * level * width) + l, mlstr.split("\n")))
