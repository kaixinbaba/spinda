# -*- coding: utf-8 -*-
import os
import re
import inspect
from collections import defaultdict

import click
import prettytable
from colorama import Fore, Style
from tqdm import tqdm

"""Main module."""


def smc(line):
    """is start multi comment"""
    return line.startswith("'''") or line.startswith('"""')


def emc(line):
    """is end multi comment"""
    return line.endswith("'''") or line.endswith('"""')


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
        self.tb = prettytable.PrettyTable(['总文件数量', f'{self.mode}源码数量'])

    def table(self):
        self.tb.add_row([self.total_file_count, self.src_file_count])
        return self.tb


class SourceFile:

    def __init__(self, abspath):
        self.abspath = abspath
        self.name = os.path.split(abspath)[1]
        self.total_line = 0
        self.src_line = 0
        self.blank_line = 0
        self.comment_line = 0
        self.src_ratio = 0.0
        self.blank_ratio = 0.0
        self.comment_ratio = 0.0

    def read_file(self):
        raise NotImplementedError()

    @staticmethod
    def new_file(abspath, mode):
        if mode == 'py':
            return PythonSourceFile(abspath=abspath)
        else:
            # TODO other like java
            pass

    @staticmethod
    def get_sratio(line, total_line):
        if total_line == 0:
            return '0.0%'
        else:
            return str((line / total_line) * 100)[:4] + '%'


class PythonSourceFile(SourceFile):

    def __init__(self, **kwargs):
        super(PythonSourceFile, self).__init__(**kwargs)
        self.ext = 'py'
        self.all_class_dict = defaultdict(set)
        self.read_file()

    def read_file(self):
        with open(self.abspath, 'r', encoding='utf-8') as f:
            in_multi_comment = False
            for line in f:
                self.total_line += 1
                line = line.strip()
                if in_multi_comment:
                    self.comment_line += 1
                    if emc(line):
                        in_multi_comment = False
                else:
                    if smc(line):
                        if emc(line):
                            in_multi_comment = False
                        else:
                            in_multi_comment = True
                        self.comment_line += 1
                    elif line.startswith("#"):
                        self.comment_line += 1
                    elif line == '':
                        self.blank_line += 1
                    else:
                        self.src_line += 1
                        result = re.match(r'class\s+(.*):', line)
                        if result is not None:
                            name = result.groups()[0]
                            name = name.split('(')
                            # whole_classname = os.path.join(self.abspath, name[0].strip())
                            whole_classname = name[0].strip()
                            if len(name) == 1:
                                self.all_class_dict[whole_classname].add('object')
                            else:
                                parent_classes = name[1][:-1].split(",")
                                for p in parent_classes:
                                    p = p.strip()
                                    self.all_class_dict[whole_classname].add(p)
        self.src_ratio = self.get_sratio(self.src_line, self.total_line)
        self.blank_ratio = self.get_sratio(self.blank_line, self.total_line)
        self.comment_ratio = self.get_sratio(self.comment_line, self.total_line)


class SourceLineSummary(Summary):

    def __init__(self, **kwargs):
        super(SourceLineSummary, self).__init__(**kwargs)
        self.all_file = {}
        self.all_file_class_dict = {}
        self.all_class = set()
        self.reverse_all_file_class_dict = {}
        self.tb = prettytable.PrettyTable(['文件名', '总行数', '源码行数', '空行数', '注释行数', '源码率', '空行率', '注释率'])

    def table(self):
        for abspath, file in self.all_file.items():
            filename = file.name
            # filename = abspath
            self.tb.add_row([filename, file.total_line, file.src_line, file.blank_line, file.comment_line,
                             file.src_ratio, file.blank_ratio, file.comment_ratio])
        return self.tb

    def add_source_file(self, abspath):
        self.all_file[abspath] = SourceFile.new_file(abspath, self.mode)

    def mix_all_file(self):
        all_file_class_dict = {}
        for file in self.all_file.values():
            class_in_one_file = file.all_class_dict
            all_file_class_dict.update(class_in_one_file)
        return all_file_class_dict

    def get_all_class(self):
        for s, ps in self.all_file_class_dict.items():
            self.all_class.update([s])
            self.all_class.update(ps)

    def print_tree(self):
        # sub -> parents dict
        self.all_file_class_dict = self.mix_all_file()
        self.get_all_class()
        # parent -> subs dict
        self.reverse_all_file_class_dict = self.reverse_class_dict()
        self._print_tree(self.reverse_all_file_class_dict, 'object', 0)
        # self._print_tree(self.reverse_all_file_class_dict, 'Exception', 0)
        # self._print_tree(self.reverse_all_file_class_dict, 'Exception', 0)
        # self._print_tree(self.reverse_all_file_class_dict, 'dict', 0)

    def _print_tree(self, p2s_dict, current_parent, depth):
        print("|   " * depth + "+----" + current_parent)
        for sub in p2s_dict[current_parent]:
            self._print_tree(p2s_dict, sub, depth + 1)

    def reverse_class_dict(self):
        result = defaultdict(set)
        for c in self.all_class:
            self.collect_one_parent_all_sub(c, result)
        return result

    def collect_one_parent_all_sub(self, parent, result):
        for sub, parents in self.all_file_class_dict.items():
            if parent in parents:
                result[parent].add(sub)


def scan(**kwargs):
    Main(**kwargs).scan()


class Main:
    def __init__(self, path='.', mode='py',
                 include_hidden=False, line=False, file=False, obj=False,
                 **kwargs):
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
        self.show_all = not (line or file or obj)
        self.show_line = line
        self.show_file = file
        self.show_obj = obj

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
            try:
                path_in_list = os.path.join(self.abspath, name)
                if os.path.isdir(path_in_list) and name != 'build':
                    self._handle_dir(path_in_list, self.mode, self.include_hidden)
                elif os.path.isfile(path_in_list):
                    self._handle_file(path_in_list, self.mode)
            except Exception as e:
                pass
        if self.show_file or self.show_all:
            print(Fore.GREEN + f"{'-'*50} 文件总览  {'-'*50}")
            print(self.fileSummary.table())
            print(Style.RESET_ALL)
        if self.show_line or self.show_all:
            print(Fore.GREEN + f"{'-'*50} 行总览  {'-'*50}")
            print(self.lineSummary.table())
            print(Style.RESET_ALL)
        if self.show_obj or self.show_all:
            print(Fore.GREEN + f"{'-'*50} 对象总览  {'-'*50}")
            self.lineSummary.print_tree()
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

    def _handle_dir(self, abspath, mode, include_hidden):
        for name in filter(lambda n: self.is_not_hidden(n, include_hidden),
                           os.listdir(abspath)):
            path_in_list = os.path.join(abspath, name)
            if os.path.isdir(path_in_list):
                self._handle_dir(path_in_list, mode, include_hidden)
            elif os.path.isfile(path_in_list):
                self._handle_file(path_in_list, mode)
