# -*- coding: utf-8 -*-

"""Console script for spinda."""
import sys
import click

from spinda import scan


@click.command()
@click.argument('path', nargs=1, required=True, default='.', type=str)
def main(path):
    """Console script for spinda."""
    if scan(path) == 0:
        sys.exit(0)
    else:
        sys.exit(1)
