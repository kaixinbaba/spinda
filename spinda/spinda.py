# -*- coding: utf-8 -*-
import os

import click

"""Main module."""


def print_hello():
    print('hello in spinda from main')


SUCCESS = 0
FAIL = 1


def scan(path='.'):
    """整个项目真正的入口函数
    path : 需要扫描的路径，默认是当前路径
    """
    if path.startswith('/'):
        abspath = path
    else:
        abspath = os.path.abspath(path)
    # check path exists
    if not os.path.exists(abspath):
        click.secho(f'路径 [{abspath}] 不存在！请检查！', fg='red')
        return FAIL
    # TODO 需要询问吗
    click.echo(f'准备开始扫描路径 [{abspath}]')
    return SUCCESS
