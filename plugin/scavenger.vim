let s:plugin_path = escape(expand('<sfile>:p:h'), '\')

" highlight the empty line more than one
highlight MultipleEmptyLines ctermbg=red guibg=red
call matchadd('MultipleEmptyLines', '\_^\_$\n\_^\_$\n')

" highlight trailing space
highlight TrailingSpaces ctermbg=red guibg=red
call matchadd('TrailingSpaces', '\s\+$')


if has('python')

	function! LoadPythonFile()
		exe 'pyfile ' . escape(s:plugin_path, ' ') . '/scavenger.py'
	endfunc

    function! CleanUp()
        python import sys
        python sys.argv = ['clean_up']
		call LoadPythonFile()
    endfunc

    function! CleanUpMultipleEmptyLines()
        python import sys
        python sys.argv = ['clean_up_multiple_empty_lines']
		call LoadPythonFile()
    endfunc

    function! CleanUpTrailingSpaces()
        python import sys
        python sys.argv = ['clean_up_trailing_spaces']
		call LoadPythonFile()
    endfunc

    function! IsMultipleEmptyLinesExist()
        python import sys
        python sys.argv = ['is_multiple_empty_lines_exist']
		call LoadPythonFile()

        if l:multiple_empty_lines_exist
            echo "There are multiple empty lines."
        endif
    endfunc

    function! IsTrailingSpacesExist()
        python import sys
        python sys.argv = ['is_trailing_spaces_exist']
		call LoadPythonFile()

        if l:trailing_spaces_exist
            echo "There are trailing spaces."
        endif
    endfunc

    if exists("g:auto_clean_up_when_write")
        if g:auto_clean_up_when_write
            autocmd BufWritePre * call CleanUp()
        endif
    endif
elseif has('python3')
    pyfile3 scavenger.py3
endif
