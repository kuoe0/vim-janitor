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

def restore_cursor_decorator(action):
    current_cursor_position = vim.current.window.cursor
    def wrapper_function():
        new_cursor_position = action(*current_cursor_position)
        vim.current.window.cursor = new_cursor_position
    return wrapper_function

@restore_cursor_decorator
def clean_up_multiple_empty_lines(cursor_row, cursor_col):

    old_buffer = vim.current.buffer
    new_buffer = old_buffer[0:1]
    removed_line_before_cursor_row = 0

    for idx in range(len(old_buffer))[1:]:
        if len(old_buffer[idx]):
            # not the empty line
            new_buffer.append(old_buffer[idx])
        elif not len(old_buffer[idx]) and old_buffer[idx] != old_buffer[idx - 1]:
            # the first empty line
            new_buffer.append(old_buffer[idx])
        else:
            if idx < cursor_row:
                removed_line_before_cursor_row += 1

    # Remove empty line at begin
    if not len(new_buffer[0]):
        new_buffer = new_buffer[1:]

    # Remove empty line at end
    if not len(new_buffer[-1]):
        new_buffer = new_buffer[:-1]

    vim.current.buffer[:] = new_buffer

    new_cursor_row = cursor_row - removed_line_before_cursor_row
    if new_cursor_row > len(new_buffer):
        new_cursor_row = len(new_buffer)

    return (new_cursor_row, cursor_col)

@restore_cursor_decorator
def clean_up_trailing_spaces(cursor_row, cursor_col):
    old_buffer = vim.current.buffer
    new_buffer = map(lambda line: line.rstrip(), old_buffer)
    vim.current.buffer[:] = new_buffer
    return (cursor_row, cursor_col)

@restore_cursor_decorator
def clean_up(cursor_row, cursor_col):
    clean_up_trailing_spaces()
    clean_up_multiple_empty_lines()
    return vim.current.window.cursor

def is_multiple_empty_lines_exist():
    buffer = vim.current.buffer
    for idx in range(len(buffer))[1:]:
        if not len(buffer[idx]) and buffer[idx] == buffer[idx - 1]:
            vim.command("let l:multiple_empty_lines_exist = 1")
            return
    vim.command("let l:multiple_empty_lines_exist = 0")

def is_trailing_spaces_exist():
    buffer = vim.current.buffer
    trailing_space_pattern = re.compile('\s+$')
    for line in buffer:
        search_result = trailing_space_pattern.search(line)
        if search_result:
            vim.command("let l:trailing_spaces_exist = 1")
            return
    vim.command("let l:trailing_spaces_exist = 0")
