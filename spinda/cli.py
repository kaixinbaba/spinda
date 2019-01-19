# -*- coding: utf-8 -*-
import click

from spinda import scan, SpindaBaseError, __version__


@click.command()
@click.argument('path', nargs=1, required=True, default='.', type=str)
@click.option('-m', '--mode', type=click.Choice(['py']), default='py',
              help='重点关注哪种编程语言的项目，默认python')
@click.option('-i', '--include-hidden', is_flag=True, default=False,
              help='是否忽略隐藏文件和目录，默认关闭')
@click.option('-l', '--line', is_flag=True, default=False,
              help='是否展示源码行数统计')
@click.option('-f', '--file', is_flag=True, default=False,
              help='是否展示文件统计')
@click.option('-o', '--obj', is_flag=True, default=False,
              help='是否展示文件统计')
@click.version_option(prog_name='spinda', version=__version__)
# def main(path=None, mode=None, ignore_hidden=None):
def main(**kwargs):
    """代码项目扫描命令行工具"""
    click.secho(str(kwargs), fg='yellow')
    try:
        scan(**kwargs)
    except SpindaBaseError as sbe:
        click.secho(str(sbe), fg='red')
    except Exception as e:
        raise e
