# -*- coding: utf-8 -*-

"""Console script for spinda."""
import click

from spinda import scan, SpindaBaseError


@click.command()
@click.argument('path', nargs=1, required=True, default='.', type=str)
def main(path):
    """Console script for spinda."""
    try:
        scan(path)

    except SpindaBaseError as sbe:
        click.secho(str(sbe), fg='red')
    except Exception as e:
        raise e
