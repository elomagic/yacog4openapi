#!/usr/bin/env python

from click.testing import CliRunner
from genclient import gen_code
from pathlib import Path


def test_something():

    Path("test-output").mkdir(parents=True, exist_ok=True)

    runner = CliRunner()
    result = runner.invoke(gen_code, [
        '--source=test/openapi.json',
        '--template=test/test-template.jinja2',
        '--output=test-output/test-unit.txt'])

    print(f'Output={result.output}')

    assert result.exit_code == 0

    with open('test-output/test-unit.txt') as f:
        generated_code_lines = f.readlines()

    assert generated_code_lines[0] == 'Weather Microservice API\n'
    assert generated_code_lines[1] == 'Simple DYI weather service API\n'
    assert generated_code_lines[2] == '0.0\n'
    assert generated_code_lines[3] == 'Apache 2.0\n'

    assert generated_code_lines[5] == '4'



