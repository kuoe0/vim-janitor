#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 KuoE0 <kuoe0.tw@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import re
import subprocess
import os.path
import sys
import vim

DEBUG = False

def debug(msg):
    if DEBUG:
        print msg

def vim_input(message):
    vim.command('call inputsave()')
    vim.command("let user_input = input('" + message + ": ')")
    vim.command('call inputrestore()')
    return vim.eval('user_input')

def restore_cursor_decorator(action):
    def wrapper_function():
        debug('Action: ' + action.__name__)
        cur_cursor = vim.current.window.cursor
        debug("old: {0}".format(str(cur_cursor)))

        new_cursor = action(*cur_cursor)
        debug("new: {0}".format(str(new_cursor)))
        vim.current.window.cursor = new_cursor
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
def clean_up_trailing_spaces(*args):
    old_buffer = vim.current.buffer
    new_buffer = map(lambda line: line.rstrip(), old_buffer)
    vim.current.buffer[:] = new_buffer
    return args

@restore_cursor_decorator
def clean_up_trailing_spaces_only_added(*args):
    cmd = 'git rev-parse --git-dir'
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    ret = p.stdout.readline().strip()
    if not ret.endswith('.git'):
        raise Exception('Not in a git repo.')

    filename = vim.eval("expand('%')")
    cmd = 'git diff -U0 {0}'.format(filename)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)

    lineno = None
    lineno_to_clean_up = []
    header_pattern = re.compile(r'\@\@\s+-(?P<delete>[0-9,]+)\s+\+(?P<add>[0-9,+]+)\s\@\@')
    for line in p.stdout.readlines():
        # enter a chunk
        if line.startswith('@@'):
            add_info = header_pattern.search(line).group('add')
            lineno = int(add_info.split(',')[0])
            continue

        if lineno and line.startswith('+'):
            lineno_to_clean_up.append(lineno)
            lineno += 1
            continue

    for lineno in lineno_to_clean_up:
        # zero-based line number
        line = vim.current.buffer[lineno - 1]
        vim.current.buffer[lineno - 1] = line.rstrip()
    return args

@restore_cursor_decorator
def clean_up(cursor_row, cursor_col):
    scavenger_clean_trailing_spaces_only_changed = int(vim.eval('g:scavenger_clean_trailing_spaces_only_changed'))
    debug('scavenger_clean_trailing_spaces_only_changed = {0}'.format(scavenger_clean_trailing_spaces_only_changed))
    if scavenger_clean_trailing_spaces_only_changed != 0:
        try:
            clean_up_trailing_spaces_only_added()
        except Exception as err:
            print err.message
            ret = ''
            if scavenger_clean_trailing_spaces_only_changed == 2:
                ret = 'y'
            if scavenger_clean_trailing_spaces_only_changed == 3:
                ret = 'n'
            while (ret not in ['Y', 'y', 'N', 'n']):
                ret = vim_input('Want to clean up ALL trailing spaces? [Y/n]')
            if ret in ['Y', 'y']:
                clean_up_trailing_spaces()
    else:
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
