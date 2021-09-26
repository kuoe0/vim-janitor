" vim:fenc=utf-8
"
" Copyright © 2016 KuoE0 <kuoe0.tw@gmail.com>
"
" Distributed under terms of the MIT license.

" --------------------------------
" Init
" --------------------------------
" Add the python plugin to the path (both Python2 and Python3 supported)
let script_path = expand('<sfile>:p:h') . '/janitor.py'
if !has('python') && !has('python3')
   finish
endif
execute (has('python3') ? 'py3file' : 'pyfile') script_path

" --------------------------------
" Variable (s)
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
function! CleanUp()
	execute (has('python3') ? 'python3' : 'python') "clean_up()"
endfunc

function! CleanUpMultipleBlankLines()
	execute (has('python3') ? 'python3' : 'python') "clean_up_multiple_blank_lines()"
endfunc

function! CleanUpMultipleBlankLinesOnlyAdded()
	execute (has('python3') ? 'python3' : 'python') "clean_up_multiple_blank_lines_only_added()"
endfunc

function! CleanUpTrailingSpaces()
	execute (has('python3') ? 'python3' : 'python') "clean_up_trailing_spaces()"
endfunc

function! CleanUpTrailingSpacesOnlyAdded()
	execute (has('python3') ? 'python3' : 'python') "clean_up_trailing_spaces_only_added()"
endfunc

function! IsMultipleBlankLinesExist()
	execute (has('python3') ? 'python3' : 'python') "is_multiple_blank_lines_exist()"
	if l:multiple_blank_lines_exist
		echo "There are multiple blank lines."
	endif
endfunc

function! IsTrailingSpacesExist()
	execute (has('python3') ? 'python3' : 'python') "is_trailing_spaces_exist()"
	if l:trailing_spaces_exist
		echo "There are trailing spaces."
	endif
endfunc

if g:janitor_auto_clean_up_on_write
	autocmd BufWritePre * call CleanUp()
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
