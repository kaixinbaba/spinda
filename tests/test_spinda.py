#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `spinda` package."""

from spinda import scan, ArgumentError
import pytest


def test_path():
    with pytest.raises(ArgumentError):
        scan('/zjxjkj')
    with pytest.raises(ArgumentError):
        scan('dkjfkdjfkdj')
    scan()
