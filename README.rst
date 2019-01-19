======
spinda
======


.. image:: https://img.shields.io/pypi/v/spinda.svg
        :target: https://pypi.python.org/pypi/spinda

.. image:: https://img.shields.io/travis/kaixinbaba/spinda.svg
        :target: https://travis-ci.org/kaixinbaba/spinda

.. image:: https://img.shields.io/pypi/l/spinda.svg
        :target: https://pypi.org/project/spinda/

.. image:: https://img.shields.io/pypi/pyversions/spinda.svg
        :target: https://pypi.org/project/spinda/

A tool for counting the number of lines of code
and object relationships in a project...


* Free software: GNU General Public License v3


Features
--------
- python project statistics √
- file count statistics √
- code line statistics √
- class object statistics √



Getting start
-------------
Install from pip
    >>> pip install spinda
Install from the source
    >>> git clone https://github.com/kaixinbaba/spinda.git
    >>> cd spinda
    >>> python setup.py install
How to use?
    >>> cd /some/you/want/to/statistics/path
    >>> spinda
Get more help?
    >>> spinda --help
        Usage: spinda [OPTIONS] PATH
          代码项目扫描命令行工具
        Options:
          -m, --mode [py]       重点关注哪种编程语言的项目，默认python
          -i, --include-hidden  是否忽略隐藏文件和目录，默认关闭
          -l, --line            是否展示源码行数统计
          -f, --file            是否展示文件统计
          -o, --obj             是否展示文件统计
          --version             Show the version and exit.
          --help                Show this message and exit.

TODO
--------
- Class name same bug
- Other language


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

