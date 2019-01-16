# -*- coding: utf-8 -*-
import click

from spinda import scan, SpindaBaseError


@click.command()
@click.argument('path', nargs=1, required=True, default='.', type=str)
@click.option('-m', '--mode', type=click.Choice(['py']), default='py',
              help='重点关注哪种编程语言的项目，默认python')
def main(path=None, mode=None):
    """代码项目扫描命令行工具"""
    try:
        scan(path, mode)

    except SpindaBaseError as sbe:
        click.secho(str(sbe), fg='red')
    except Exception as e:
        raise e
