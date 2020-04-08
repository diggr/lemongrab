import click
import os

from click.testing import CliRunner
from lemongrab.cli import cli

def test_init(clean_cwd):
    runner = CliRunner()
    result = runner.invoke(cli, ["init", "test"])
    assert result.exit_code == 0
