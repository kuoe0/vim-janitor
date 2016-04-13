#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 KuoE0 <kuoe0.tw@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import vim
import sys
import re

def clean_up_multiple_empty_lines():
    old_buffer = vim.current.buffer
    new_buffer = old_buffer[0:1]

    for idx in range(len(old_buffer))[1:]:
        if len(old_buffer[idx]):
            # not the empty line
            new_buffer.append(old_buffer[idx])
        if not len(old_buffer[idx]) and old_buffer[idx] != old_buffer[idx - 1]:
            # the first empty line
            new_buffer.append(old_buffer[idx])

    # Remove empty line at begin
    if not len(new_buffer[0]):
        new_buffer = new_buffer[1:]

    # Remove empty line at end
    if not len(new_buffer[-1]):
        new_buffer = new_buffer[:-1]

    vim.current.buffer[:] = new_buffer

def clean_up_trailing_spaces():
    old_buffer = vim.current.buffer
    new_buffer = map(lambda line: line.rstrip(), old_buffer)
    vim.current.buffer[:] = new_buffer

def clean_up():
    clean_up_trailing_spaces()
    clean_up_multiple_empty_lines()

eval(sys.argv[0])()
