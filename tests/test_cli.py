import click
import os

from click.testing import CliRunner
from lemongrab.cli import cli

def test_init(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(cli, ["init"])
    assert result.exit_code == 0
