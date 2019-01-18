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

    def __init__(self, mode):
        self.mode = mode

    def table(self):
        raise NotImplementedError()


class FileSummary(Summary):
    def __init__(self, **kwargs):
        super(FileSummary, self).__init__(**kwargs)
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

    def __init__(self, **kwargs):
        super(SourceLineSummary, self).__init__(**kwargs)
        pass

    def table(self):
        pass

    def add_source_file(self, abspath):
        pass


class SourceObjectSummary(Summary):

    def __init__(self, **kwargs):
        super(SourceObjectSummary, self).__init__(**kwargs)
        pass

    def table(self):
        pass

    def add_source_file(self, abspath):
        pass


def scan(**kwargs):
    Main(**kwargs).scan()


class Main:
    def __init__(self, path='.', mode='py', include_hidden=False, **kwargs):
        self.path = path
        if self.path.startswith('/'):
            self.abspath = self.path
        else:
            self.abspath = os.path.abspath(self.path)
        self._check_arg()
        self.mode = mode
        self.include_hidden = include_hidden
        self.fileSummary = FileSummary(mode=mode)
        self.lineSummary = SourceLineSummary(mode=mode)
        self.objectSummary = SourceObjectSummary(mode=mode)

    def _check_arg(self):
        # check path exists
        if not os.path.exists(self.abspath):
            raise ArgumentError(f'路径 [{self.abspath}] 不存在！请检查！')

    def scan(self):
        """整个项目真正的入口函数
        path : 需要扫描的路径，默认是当前路径
        """
        # TODO 需要询问吗
        click.echo(f'准备开始扫描路径 [{self.abspath}]')
        for name in tqdm(list(filter(lambda n: self.is_not_hidden(n, self.include_hidden), os.listdir(self.abspath))),
                         desc='正在扫描 : ', ncols=80):
            path_in_list = os.path.join(self.abspath, name)
            if os.path.isdir(path_in_list):
                self._handle_dir(path_in_list, self.mode, self.include_hidden)
            elif os.path.isfile(path_in_list):
                self._handle_file(path_in_list, self.mode)
        print(Fore.GREEN + "---------文件总览---------")
        print(self.fileSummary.table())
        print(Style.RESET_ALL)

    @staticmethod
    def is_not_hidden(name, include_hidden):
        name = os.path.split(name)[-1]
        if include_hidden:
            return True
        else:
            return not name.startswith('.')

    def _handle_file(self, abspath, mode):
        self.fileSummary.total_file_count += 1
        suffix_name = os.path.splitext(abspath)[-1][1:]
        if suffix_name == mode:
            self.fileSummary.src_file_count += 1
            self.lineSummary.add_source_file(abspath)
            self.objectSummary.add_source_file(abspath)

    def _handle_dir(self, abspath, mode, include_hidden):
        for name in filter(lambda n: self.is_not_hidden(n, include_hidden),
                           os.listdir(abspath)):
            path_in_list = os.path.join(abspath, name)
            if os.path.isdir(path_in_list):
                self._handle_dir(path_in_list, mode, include_hidden)
            elif os.path.isfile(path_in_list):
                self._handle_file(path_in_list, mode)
