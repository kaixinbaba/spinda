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


class Summary:
    def __init__(self):
        self.total_file_count = 0
        self.max_folder_depth = 0
        self.src_file_count = 0
        self.hidden_file_count = 0

    def __str__(self):
        return f'''
        源文件数量       [{self.src_file_count}]
        总文件数量       [{self.total_file_count}]
        最大目录深度       [{self.max_folder_depth}]
        '''


summary = Summary()


def scan(path='.', mode='py', ignore_hidden=False, **kwargs):
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
    global summary
    for name in tqdm(list(filter(lambda n: is_not_hidden(n, ignore_hidden),
                                 os.listdir(abspath))),
                     desc='正在扫描 : ', ncols=80):

        summary.max_folder_depth += 1
        print(name)
        path_in_list = os.path.join(abspath, name)
        if os.path.isdir(path_in_list):
            _handle_dir(path_in_list, mode, ignore_hidden)
        elif os.path.isfile(path_in_list):
            _handle_file(path_in_list, mode)
    click.secho(str(summary), fg='green')


def is_not_hidden(name, ignore_hidden):
    name = os.path.split(name)[-1]
    if ignore_hidden:
        return not name.startswith('.')
    else:
        return True


def _handle_file(abspath, mode):
    global summary
    summary.total_file_count += 1
    suffix_name = os.path.splitext(abspath)[-1][1:]
    if suffix_name == mode:
        print(suffix_name)
        summary.src_file_count += 1


def _handle_dir(abspath, mode, ignore_hidden):
    global summary
    summary.max_folder_depth += 1
    for name in filter(lambda n: is_not_hidden(n, ignore_hidden),
                       os.listdir(abspath)):
        path_in_list = os.path.join(abspath, name)
        if os.path.isdir(path_in_list):
            _handle_dir(path_in_list, mode, ignore_hidden)
        elif os.path.isfile(path_in_list):
            _handle_file(path_in_list, mode)
