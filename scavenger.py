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
    new_buffer = []

    # Default to true to delete empty line at beginnig.
    last_line_is_empty = True
    for line in old_buffer:
        if not len(line):
            if last_line_is_empty:
                continue
            last_line_is_empty = True
        else:
            last_line_is_empty = False
        new_buffer.append(line)
    else:
        # Remove empty line at end
        if last_line_is_empty:
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
