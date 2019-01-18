# -*- coding: utf-8 -*-
import os

import click
import prettytable
from colorama import Fore, Style
from tqdm import tqdm

"""Main module."""


class SpindaBaseError(Exception):

    def __init__(self, message):
        self.message = message


class ArgumentError(SpindaBaseError):

    def __init__(self, message):
        super(ArgumentError, self).__init__(message)


class Summary:

    def table(self):
        raise NotImplementedError()


class FileSummary(Summary):
    def __init__(self):
        self.total_file_count = 0
        self.src_file_count = 0
        self.hidden_file_count = 0
        self.tb = prettytable.PrettyTable()

    def table(self):
        self.tb.add_column('总文件数量', [self.total_file_count])
        self.tb.add_column('源码数量', [self.src_file_count])
        return self.tb


class SourceFile:
    pass


class PythonSourceFile(SourceFile):
    pass


class SourceLineSummary(Summary):

    def __init__(self):
        pass

    def table(self):
        pass

    def add_source_file(self, abspath):
        pass


class SourceObjectSummary(Summary):

    def __init__(self):
        pass

    def table(self):
        pass

    def add_source_file(self, abspath):
        pass


fileSummary = FileSummary()
lineSummary = SourceLineSummary()
objectSummary = SourceObjectSummary()


def scan(**kwargs):
    Main().scan(**kwargs)


class Main:
    def __init__(self):
        pass

    def _check_arg(**kwargs):
        pass

    def scan(self, path='.', mode='py', include_hidden=False, **kwargs):
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
        for name in tqdm(list(filter(lambda n: self.is_not_hidden(n, include_hidden), os.listdir(abspath))),
            desc='正在扫描 : ', ncols=80):
            path_in_list = os.path.join(abspath, name)
            if os.path.isdir(path_in_list):
                self._handle_dir(path_in_list, mode, include_hidden)
            elif os.path.isfile(path_in_list):
                self._handle_file(path_in_list, mode)
        print(Fore.GREEN + "---------文件总览---------")
        print(fileSummary.table())
        print(Style.RESET_ALL)

    @staticmethod
    def is_not_hidden(name, include_hidden):
        name = os.path.split(name)[-1]
        if include_hidden:
            return True
        else:
            return not name.startswith('.')

    @staticmethod
    def _handle_file(abspath, mode):
        fileSummary.total_file_count += 1
        suffix_name = os.path.splitext(abspath)[-1][1:]
        if suffix_name == mode:
            fileSummary.src_file_count += 1
            lineSummary.add_source_file(abspath)
            objectSummary.add_source_file(abspath)

    def _handle_dir(self, abspath, mode, include_hidden):
        for name in filter(lambda n: self.is_not_hidden(n, include_hidden),
                           os.listdir(abspath)):
            path_in_list = os.path.join(abspath, name)
            if os.path.isdir(path_in_list):
                self._handle_dir(path_in_list, mode, include_hidden)
            elif os.path.isfile(path_in_list):
                self._handle_file(path_in_list, mode)
