" highlight the empty line more than one
highlight MultipleEmptyLines ctermbg=red guibg=red
call matchadd('MultipleEmptyLines', '\_^\_$\n\_^\_$\n')

" highlight trailing space
highlight TrailingSpaces ctermbg=red guibg=red
call matchadd('TrailingSpaces', '\s\+$')

" squash multiple empty lines to one line
" autocmd BufWritePre * !cat -s <sfile>

if has('python')
    function! CleanUp()
        python import sys
        python sys.argv = ['clean_up']
        pyfile scavenger.py
    endfunc

    function! CleanUpMultipleEmptyLines()
        python import sys
        python sys.argv = ['clean_up_multiple_empty_lines']
        pyfile scavenger.py
    endfunc

    function! CleanUpTrailingSpaces()
        python import sys
        python sys.argv = ['clean_up_trailing_spaces']
        pyfile scavenger.py
    endfunc

elseif has('python3')
    pyfile3 scavenger.py3
endif
