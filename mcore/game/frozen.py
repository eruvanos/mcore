import os
import sys
from pathlib import Path


def get_resource_path(default_path: str = '.') -> Path:
    return Path(getattr(sys, '_MEIPASS', default_path)) / 'resources'


def fix_cwd_for_frozen_execution():
    if hasattr(sys, '_MEIPASS'):
        os.chdir(Path(getattr(sys, '_MEIPASS', '.')))
