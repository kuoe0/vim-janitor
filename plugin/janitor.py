# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 KuoE0 <kuoe0.tw@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""

import os.path
import platform
import re
import subprocess
import tempfile
import vim

DEBUG = False


def debug(msg):
    if DEBUG:
        print(msg)


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


def get_added_lines():
    the_file = vim.eval("expand('%')")
    with tempfile.NamedTemporaryFile(delete=False) as f:
        tmp_file = f.name
    vim.command('write! {0}'.format(tmp_file))

    cmd = 'diff -u {0} {1}'.format(the_file, tmp_file)
    if platform.system() == 'Windows':
        # hide command prompt
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    else:
        startupinfo = None
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                         stderr=open(os.devnull, 'w'),
                         startupinfo=startupinfo)
    output, _ = p.communicate()
    output = output.decode('utf8')

    lineno = None
    lineno_to_clean_up = []
    header_pattern = re.compile(
        r'\@\@\s+-(?P<delete>[0-9,]+)\s+\+(?P<add>[0-9,+]+)\s\@\@')

    for line in output.splitlines():
        # enter a chunk
        if line.startswith('@@'):
            add_info = header_pattern.search(line).group('add')
            lineno = int(add_info.split(',')[0])
            continue

        if line.startswith('-'):
            continue

        if lineno and line.startswith('+'):
            lineno_to_clean_up.append(lineno)

        if lineno:
            lineno += 1

    return [x - 1 for x in lineno_to_clean_up]


def clean_up_multiple_blank_lines_at_begin_and_end(cursor_row):
    if not len(vim.current.buffer[0]):
        if 0 < cursor_row:
            cursor_row -= 1
        del vim.current.buffer[0]
    if not len(vim.current.buffer[-1]):
        if len(vim.current.buffer) - 1 < cursor_row:
            cursor_row -= 1
        del vim.current.buffer[-1]
    return cursor_row


@restore_cursor_decorator
def clean_up_multiple_blank_lines(cursor_row, cursor_col):

    current_buffer = vim.current.buffer
    blank_lineno = [lineno for lineno, line in enumerate(
        current_buffer) if not len(line)]
    lines_to_delete = [blank_lineno[idx] for idx in range(
        len(blank_lineno))[1:] if blank_lineno[idx] - 1 == blank_lineno[idx - 1]]

    # swap buffer
    new_buffer = [line for idx, line in enumerate(
        current_buffer) if idx not in lines_to_delete]
    vim.current.buffer[:] = new_buffer

    # restore cursor position
    removed_line_before_cursor_row = list(map(lambda lineno: lineno < cursor_row,
                                              lines_to_delete)).count(True)
    new_cursor_row = cursor_row - removed_line_before_cursor_row
    # clean up blank lines at file begin and file end
    new_cursor_row = clean_up_multiple_blank_lines_at_begin_and_end(
        new_cursor_row)
    # boundary check
    new_cursor_row = 1 if new_cursor_row < 1 else new_cursor_row
    new_cursor_row = len(vim.current.buffer) if new_cursor_row > len(
        vim.current.buffer) else new_cursor_row
    return (new_cursor_row, cursor_col)


@restore_cursor_decorator
def clean_up_multiple_blank_lines_only_added(cursor_row, cursor_col):

    current_buffer = vim.current.buffer
    added_lines_list = get_added_lines()
    lines_to_delete = []

    for lineno in added_lines_list:
        if len(current_buffer[lineno]):
            continue
        # previous line is blank line
        if lineno - 1 >= 0 and not len(current_buffer[lineno - 1]):
            lines_to_delete.append(lineno)
        # next line is blank line
        elif lineno + 1 < len(current_buffer) and not len(current_buffer[lineno + 1]):
            lines_to_delete.append(lineno)

    # swap buffer
    new_buffer = [line for idx, line in enumerate(
        current_buffer) if idx not in lines_to_delete]
    vim.current.buffer[:] = new_buffer

    # restore cursor position
    removed_line_before_cursor_row = list(map(lambda lineno: lineno < cursor_row,
                                              lines_to_delete)).count(True)
    # clean up blank lines at file begin and file end
    new_cursor_row = cursor_row - removed_line_before_cursor_row
    new_cursor_row = clean_up_multiple_blank_lines_at_begin_and_end(
        new_cursor_row)
    # boundary check
    new_cursor_row = 1 if new_cursor_row < 1 else new_cursor_row
    new_cursor_row = len(vim.current.buffer) if new_cursor_row > len(
        vim.current.buffer) else new_cursor_row
    return (new_cursor_row, cursor_col)


@restore_cursor_decorator
def clean_up_trailing_spaces(*args):
    old_buffer = vim.current.buffer
    new_buffer = map(lambda line: line.rstrip(), old_buffer)
    vim.current.buffer[:] = new_buffer
    return args


@restore_cursor_decorator
def clean_up_trailing_spaces_only_added(*args):

    added_lines_list = get_added_lines()

    for lineno in added_lines_list:
        line = vim.current.buffer[lineno]
        vim.current.buffer[lineno] = line.rstrip()

    return args


@restore_cursor_decorator
def clean_up(cursor_row, cursor_col):
    filetype = vim.eval('&ft')

    if vim.eval('g:janitor_auto_clean_up_trailing_space_only_added') == '1':
        if filetype not in vim.eval('g:janitor_exclude_on_trailing_spaces'):
            clean_up_trailing_spaces_only_added()
    elif vim.eval('g:janitor_auto_clean_up_trailing_space') == '1':
        if filetype not in vim.eval('g:janitor_exclude_on_trailing_spaces'):
            clean_up_trailing_spaces()

    if vim.eval('g:janitor_auto_clean_up_blank_lines_only_added') == '1':
        if filetype not in vim.eval('g:janitor_exclude_on_blank_lines'):
            clean_up_multiple_blank_lines_only_added()
    elif vim.eval('g:janitor_auto_clean_up_blank_lines') == '1':
        if filetype not in vim.eval('g:janitor_exclude_on_blank_lines'):
            clean_up_multiple_blank_lines()

    return vim.current.window.cursor


def is_multiple_blank_lines_exist():
    buffer = vim.current.buffer
    for idx in range(len(buffer))[1:]:
        if not len(buffer[idx]) and buffer[idx] == buffer[idx - 1]:
            vim.command("let l:multiple_blank_lines_exist = 1")
            return
    vim.command("let l:multiple_blank_lines_exist = 0")


def is_trailing_spaces_exist():
    buffer = vim.current.buffer
    trailing_space_pattern = re.compile('\s+$')
    for line in buffer:
        search_result = trailing_space_pattern.search(line)
        if search_result:
            vim.command("let l:trailing_spaces_exist = 1")
            return
    vim.command("let l:trailing_spaces_exist = 0")
