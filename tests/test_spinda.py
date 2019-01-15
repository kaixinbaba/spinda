#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spinda` package."""

from spinda import scan


def test_path():
    assert 1 == scan('/zjxjkj')
    assert 1 == scan('dkjfkdjfkdj')
    assert 0 == scan()
