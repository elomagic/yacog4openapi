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

    print(f'Loading configuration \'{filename}\'')
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
@click.option("--source", default=None, help="OpenAPI source file (File and https are supported)")
@click.option("--template", default=None, help="Template file to generate an output file")
@click.option("--output", default=None, help="Name of the generated output file")
def gen_code(source: str, template: str, output: str):
    global identified_info
    global configuration

    configuration_filename = os.path.join(os.path.dirname(__file__), 'configuration.json')
    load_configuration(configuration_filename)

    if source is None:
        source = configuration['input']['source']

    if template is None:
        template = configuration['template']

    if output is None:
        output = configuration['output']

    print(f'Using source file: {source}')
    print(f'Using template file: {template}')
    print(f'Using output file: {output}')

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

    output_content = process_template(template)

    write_output(output, output_content)


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


def write_output(target_file: str, content: str) -> None:
    print(f'Writing rendered output to {target_file}')
    with open(target_file, 'w') as f:
        f.write(content)


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


def process_template(template_file: str) -> str:
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

    return template.render(enum_types=identified_enums, dto_types=identified_dtos, info=identified_info)


if __name__ == '__main__':
    gen_code()
