from typing import Optional
import sys
import os

import click

from .application import use_cases
from .application.app_config import settings
from .adapters.building import GraphBuilder
from .adapters.printing import ClickPrinter
from .adapters.filesystem import FileSystem
from .adapters.user_options import IniFileUserOptionReader


settings.configure(
    USER_OPTION_READERS=[
        IniFileUserOptionReader(),
    ],
    GRAPH_BUILDER=GraphBuilder(),
    PRINTER=ClickPrinter(),
    FILE_SYSTEM=FileSystem(),
)

EXIT_STATUS_SUCCESS = 0
EXIT_STATUS_ERROR = 1


@click.command()
@click.option('--config', default=None, help='The config file to use.')
def lint_imports_command(config: Optional[str]) -> int:
    return lint_imports(config_filename=config)


def lint_imports(config_filename: Optional[str] = None) -> int:
    # Add current directory to the path, as this doesn't happen automatically.
    sys.path.insert(0, os.getcwd())

    passed = use_cases.lint_imports(config_filename=config_filename)

    if passed:
        return EXIT_STATUS_SUCCESS
    else:
        return EXIT_STATUS_ERROR
