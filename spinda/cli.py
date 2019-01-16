# -*- coding: utf-8 -*-
import click

from spinda import scan, SpindaBaseError


@click.command()
@click.argument('path', nargs=1, required=True, default='.', type=str)
@click.option('-m', '--mode', type=click.Choice(['py']), default='py',
              help='重点关注哪种编程语言的项目，默认python')
@click.option('-i', '--ignore-hidden', is_flag=True, default=False,
              help='是否忽略隐藏文件和目录，默认关闭')
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
