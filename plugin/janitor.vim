" vim:fenc=utf-8
"
" Copyright © 2016 KuoE0 <kuoe0.tw@gmail.com>
"
" Distributed under terms of the MIT license.

" --------------------------------
" Add our plugin to the path
" --------------------------------
python import sys
python import vim
python sys.path.append(vim.eval('expand("<sfile>:h")'))

" --------------------------------
" Initial variables
" --------------------------------
if !exists('g:janitor_enable_highlight')
	let g:janitor_enable_highlight = 1
endif

if !exists('g:janitor_auto_clean_up_on_write')
	let g:janitor_auto_clean_up_on_write = 0
endif

if !exists('g:janitor_auto_clean_up_trailing_space_only_added')
	let g:janitor_auto_clean_up_trailing_space_only_added = 0
endif

if !exists('g:janitor_auto_clean_up_blank_lines_only_added')
	let g:janitor_auto_clean_up_blank_lines_only_added=0
endif

if !exists('g:janitor_auto_clean_up_only_added')
	let g:janitor_auto_clean_up_only_added = 0
endif

if !exists('g:janitor_auto_clean_up_trailing_space')
	let g:janitor_auto_clean_up_trailing_space = 0
endif

if !exists('g:janitor_auto_clean_up_blank_lines')
	let g:janitor_auto_clean_up_blank_lines = 0
endif

if !exists('g:janitor_auto_clean_up')
	let g:janitor_auto_clean_up = 0
endif

if !exists('g:janitor_exclude_on_blank_lines')
	let g:janitor_exclude_on_blank_lines = []
endif

if !exists('g:janitor_exclude_on_trailing_spaces')
	let g:janitor_exclude_on_trailing_spaces = []
endif

if !exists('g:janitor_is_highlight')
	let g:janitor_is_highlight = 0
endif

" If auto-clean-only-added is on, then so are these
if (g:janitor_auto_clean_up_only_added == 1)
	let g:janitor_auto_clean_up_trailing_space_only_added = 1
	let g:janitor_auto_clean_up_blank_lines_only_added = 1
endif
" If auto-clean is on, then so are these
if (g:janitor_auto_clean_up == 1)
	let g:janitor_auto_clean_up_trailing_space = 1
	let g:janitor_auto_clean_up_blank_lines = 1
endif

" --------------------------------
"  Function(s)
" --------------------------------
if has('python')

    function! CleanUp()
        python from janitor import clean_up
        python clean_up()
    endfunc

    function! CleanUpMultipleBlankLines()
        python from janitor import clean_up_multiple_blank_lines
        python clean_up_multiple_blank_lines()
    endfunc

    function! CleanUpMultipleBlankLinesOnlyAdded()
        python from janitor import clean_up_multiple_blank_lines_only_added
        python clean_up_multiple_blank_lines_only_added()
    endfunc

    function! CleanUpTrailingSpaces()
        python from janitor import clean_up_trailing_spaces
        python clean_up_trailing_spaces()
    endfunc

    function! CleanUpTrailingSpacesOnlyAdded()
        python from janitor import clean_up_trailing_spaces_only_added
        python clean_up_trailing_spaces_only_added()
    endfunc

    function! IsMultipleBlankLinesExist()
        python from janitor import is_multiple_blank_lines_exist
        python is_multiple_blank_lines_exist()
        if l:multiple_blank_lines_exist
            echo "There are multiple blank lines."
        endif
    endfunc

    function! IsTrailingSpacesExist()
        python from janitor import is_trailing_spaces_exist
        python is_trailing_spaces_exist()
        if l:trailing_spaces_exist
            echo "There are trailing spaces."
        endif
    endfunc

	if g:janitor_auto_clean_up_on_write
		autocmd BufWritePre * call CleanUp()
	endif
elseif has('python3')
    pyfile3 janitor.py3
endif

function! JanitorHighlightAll()
	let g:janitor_is_highlight = 1
	" highlight the blank line more than one
	highlight MultipleBlankLines ctermbg=red guibg=red
	let g:match_id_multiple_blank_lines = matchadd('MultipleBlankLines', '\_^\_$\n\_^\_$\n')
	" highlight trailing space
	highlight TrailingSpaces ctermbg=red guibg=red
	let g:match_id_trailing_spaces = matchadd('TrailingSpaces', '\s\+$')
endfunc

function! JanitorClearHighlight()
	let g:janitor_is_highlight = 0
	call matchdelete(g:match_id_multiple_blank_lines)
	call matchdelete(g:match_id_trailing_spaces)
endfunc

function! JanitorToggleHighlight()
	if g:janitor_is_highlight
		call JanitorClearHighlight()
	else
		call JanitorHighlightAll()
	endif
endfunc

if g:janitor_enable_highlight
	call JanitorHighlightAll()
endif

" --------------------------------
"  Expose our commands to the user
" --------------------------------

command! CleanUp                            call CleanUp()
command! CleanUpMultipleBlankLines          call CleanUpMultipleBlankLines()
command! CleanUpMultipleBlankLinesOnlyAdded call CleanUpMultipleBlankLinesOnlyAdded()
command! CleanUpTrailingSpaces              call CleanUpTrailingSpaces()
command! CleanUpTrailingSpacesOnlyAdded     call CleanUpTrailingSpacesOnlyAdded()
command! JanitorHighlightAll                call JanitorHighlightAll()
command! JanitorClearHighlight              call JanitorClearHighlight()
command! JanitorToggleHighlight             call JanitorToggleHighlight()
