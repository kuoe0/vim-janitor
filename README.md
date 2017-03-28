# vim-janitor

Multiple blank lines and trailing white spaces cleaner for Vim.

Vim-janitor supports both Vim and [Neovim](https://neovim.io/).

```
        _                 _             _ __
 _   __(_)___ ___        (_)___ _____  (_) /_____  _____
| | / / / __ `__ \______/ / __ `/ __ \/ / __/ __ \/ ___/
| |/ / / / / / / /_____/ / /_/ / / / / / /_/ /_/ / /
|___/_/_/ /_/ /_/   __/ /\__,_/_/ /_/_/\__/\____/_/
                   /___/
```

Generated by [patorjk.com](http://patorjk.com/software/taag/#p=display&f=Slant&t=vim-janitor).

## Requirement

### Vim

Need Python 2.x support for Vim. Check with the following command: `vim --version | grep "+python"`.

### Neovim

Install [neovim/python-client](https://github.com/neovim/python-client). Currently, Just install the client of Python 2.x.

## Functions

### `:CleanUp`

Delete all multiple blank lines and trailing spaces.

### `:CleanUpMultipleBlankLines`

Delete all multiple blank lines.

### `:CleanUpMultipleBlankLinesOnlyAdded`

Delete all multiple blank lines on added lines.

### `:CleanUpTrailingSpaces`

Delete all trailing spaces.

### `:CleanUpTrailingSpacesOnlyAdded`

Delete the trailing spaces on added lines.

### `:JanitorHighlightAll`

Highlight all blank lines and trailing spaces with red color.

### `:JanitorClearHighlight`

Clear all highlight on all blank lines and trailing spaces.

### `:JanitorToggleHighlight`

Toggle highlight.

## Settings

### `g:janitor_enable_highlight`

Enable to highlight when open files or not .

- default value: `1`
- value `1`: Highlight all multiple blank lines and trailing spaces when open files.
- value `0`: Do not highlight multiple blank lines and trailing spaces when open files.

### `g:janitor_auto_clean_up_on_write`

Enable to clear multiple blank lines and trailing spaces when save files or not.

- default value: `0`
- value `1`: Clear multiple blank lines and trailing spaces when save files automatically.
- value `0`: Do not clear multiple blank lines and trailing spaces when save files automatically.

### `g:janitor_auto_clean_up_trailing_space_only_added`

Enable to clear only trailing whitespace on the current changes. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear only trailing whitespace on added lines when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_auto_clean_up_blank_lines_only_added`

Enable to clear only blank lines on the current changes. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear only blank lines on added lines when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_auto_clean_up_only_added`

Enable to clear only on the current changes. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear only on added lines when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_auto_clean_up_trailing_space`

Enable to clear all trailing whitespace. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear all trailing whitespace when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_auto_clean_up_blank_lines`

Enable to clear all blank lines. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear all blank lines when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_auto_clean_up`

Enable to clear all blank lines and trailing whitespace. Work with `g:janitor_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear all blank lines and trailing whitespace when save files automatically.
- value `0`: Clear ALL lines when save files automatically.

### `g:janitor_exclude_on_trailing_space`

An exclusive list of filetypes used to not clean up trailing spaces when call `CleanUp`.

- default value: `[]`

### `g:janitor_exclude_on_blank_lines`

An exclusive list of filetypes used to not clean up blank lines when call `CleanUp`. It is useful on Python for PEP8-compliant.

- default value: `[]`

For example:

```
# do not clean up multiple blank lines for PEP8-compliant
let g:janitor_exclude_on_blank_linse = ['python']
```

## Warning

- **Every time you save (write) the file, the redo history will be cleaned up!**
