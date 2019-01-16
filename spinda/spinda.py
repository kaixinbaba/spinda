# -*- coding: utf-8 -*-
import os

import click
from tqdm import tqdm

"""Main module."""


class SpindaBaseError(Exception):

    def __init__(self, message):
        self.message = message


class ArgumentError(SpindaBaseError):

    def __init__(self, message):
        super(ArgumentError, self).__init__(message)


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
        raise ArgumentError(f'路径 [{abspath}] 不存在！请检查！')
    # TODO 需要询问吗
    click.echo(f'准备开始扫描路径 [{abspath}]')
    for name in tqdm(os.listdir(abspath), desc='正在扫描 : ', ncols=80):
        path_in_list = os.path.join(abspath, name)
        if os.path.isdir(path_in_list):
            _handle_dir(path_in_list)
        elif os.path.isfile(path_in_list):
            _handle_file(path_in_list)


def _handle_file(abspath):
    pass


def _handle_dir(abspath):
    pass
