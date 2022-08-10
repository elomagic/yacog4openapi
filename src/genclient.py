#!/usr/bin/env python

"""
OpenAPI Client Code Generator

Concept: Normalize OpenAPI description > Process normalize data model by a template engine

https://jinja.palletsprojects.com/en/3.1.x/
"""
import os.path

import click
import json
import requests
import string_utils
from jinja2 import Environment, FileSystemLoader, select_autoescape

configuration = {}

identified_enums = []
identified_dtos = []
identified_info = {}


def load_configuration(filename: str) -> None:
    global configuration
    with open(filename) as f:
        configuration = json.load(f)


def load_openapi_file(source: str) -> dict:
    # TODO Add yaml support
    if source.startswith("https://"):
        response = requests.get(source)
        return response.content
    else:
        with open(source) as f:
            return json.load(f)


@click.command()
@click.option("--source", help="OpenAPI source file")
def gen_code(source: str):
    global identified_info

    open_api: dict = load_openapi_file(source)

    print(f'Identified endpoints:')
    for endpoint in open_api['paths']:
        print(f'\tEndpoint: {endpoint}')

    if 'components' in open_api:
        components: dict = open_api['components']
        if 'schemas' in components:
            schemas: dict = components['schemas']
            collect_enums(schemas)
            collect_dtos(schemas)

    identified_info = open_api['info']

    process_templates()


def collect_enums(components: dict) -> None:
    global identified_enums

    for key in components:
        dto = components[key]
        if dto['type'] == 'object':
            for field_name in dto['properties']:
                prop = dto['properties'][field_name]
                # TODO Check also in items (arrays)
                if 'type' in prop and prop['type'] == 'array':
                    prop = prop['items']

                if 'enum' in prop:
                    prop['name'] = field_name
                    identified_enums.append(prop)


def collect_dtos(components: dict) -> None:
    global identified_dtos

    for key in components:
        dto = components[key]
        dto['name'] = key
        dto['fields'] = []
        for field_name in dto['properties']:
            field = dto['properties'][field_name]
            field['name'] = field_name
            field['datatype'] = map_datatype(dto['properties'][field_name])

            dto['fields'].append(field)

        identified_dtos.append(dto)


def process_templates() -> None:

    process_template(configuration['template'], configuration['output'])


def map_datatype(items: dict) -> str:
    global configuration
    # TODO Support of sets and lists

    # "$ref" : "#/components/schemas/Location"
    if '$ref' in items:
        items['ref'] = items['$ref'][items['$ref'].rindex('/')+1:]
        return items['$ref'][items['$ref'].rindex('/')+1:]

    prop_type = items['type']
    prop_format = items['format'] if 'format' in items else ''

    if prop_type == 'array':
        print('Arrays currently unsupported')
        return items['name']

    key = f'{prop_type},{prop_format}'

    if key in configuration["datatype-map"]:
        return configuration["datatype-map"][key]
    else:
        print(f'Missing datatype mapping for key \'{key}\'')

    return ''


def process_template(template_file: str, output: str) -> None:
    global identified_info
    global identified_dtos
    global identified_enums

    template_path = os.path.abspath(os.path.dirname(template_file))

    env = Environment(
        loader=FileSystemLoader(template_path),
        autoescape=select_autoescape()
    )

    # Additional custom filters
    env.filters['camelcase'] = string_utils.camel_case
    env.filters['rightpad'] = string_utils.right_pad

    print(f'Loading template {template_file}')
    template = env.get_template(os.path.basename(template_file))
    print(f'Processing template {template}')

    render_output = template.render(enum_types=identified_enums, dto_types=identified_dtos, info=identified_info)

    print(f'Writing rendered output to {output}')
    with open(output, 'w') as f:
        f.write(render_output)


if __name__ == '__main__':
    load_configuration('configuration.json')
    gen_code()
