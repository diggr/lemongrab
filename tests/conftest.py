import os
import pytest

from pathlib import Path

@pytest.fixture()
def clean_cwd(tmp_path):
    old_cwd = Path.cwd()
    os.chdir(tmp_path)
    yield
    os.chdir(old_cwd)
