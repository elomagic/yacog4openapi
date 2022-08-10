#!/usr/bin/env python

from click.testing import CliRunner
from src.genclient import gen_code


def test_something():
    print('*****************')
    runner = CliRunner()
    result = runner.invoke(gen_code, ['--source=test/openapi.json'])
    assert result.exit_code == 0
    assert result.output == 'Super'
