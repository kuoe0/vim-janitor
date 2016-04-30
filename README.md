# vim-scavenger

Multiple blank lines and trailing white spaces cleaner for Vim.

Vim-scavenger supports both Vim and [Neovim](https://neovim.io/).

```
       _
      (_)
 _   _ _ ____ ___ ___  ____ ____ _   _ ____ ____   ____  ____  ____
| | | | |    (___)___)/ ___) _  | | | / _  )  _ \ / _  |/ _  )/ ___)
 \ V /| | | | | |___ ( (__( ( | |\ V ( (/ /| | | ( ( | ( (/ /| |
  \_/ |_|_|_|_| (___/ \____)_||_| \_/ \____)_| |_|\_|| |\____)_|
                                                 (_____|
```

## Requirement

### Vim

Need Python 2.x support for Vim. Check with the following command: `vim --version | grep "+python"`.

### Neovim

Install [neovim/python-client](https://github.com/neovim/python-client). Currently, Just install the client of Python 2.x.

## Functions

### `:CleanUp`

Delete all multiple blank lines and trailing spaces.

### `:CleanUpMultipleBlankLines`

`:CleanUpMultipleBlankLines`

Delete all multiple blank lines.

### `:CleanUpTrailingSpaces`

Delete all trailing spaces.

### `:CleanUpTrailingSpacesOnlyAdded`

Delete the trailing spaces on added lines.

### `:ScavengerHighlightAll`

Highlight all blank lines and trailing spaces with red color.

### `:ScavengerClearHighlight`

Clear all highlight on all blank lines and trailing spaces.

### `:ScavengerToggleHighlight`

Toggle highlight.

## Settings

### `g:scavenger_enable_highlight`

Enable to highlight when open files or not .

- default value: `1`
- value `1`: Highlight all multiple blank lines and trailing spaces when open files.
- value `0`: Do not highlight multiple blank lines and trailing spaces when open files.

### `g:scavenger_auto_clean_up_on_write`

Enable to clear multiple blank lines and trailing spaces when save files or not.

- default value: `0`
- value `1`: Clear multiple blank lines and trailing spaces when save files automatically.
- value `0`: Do not clear multiple blank lines and trailing spaces when save files automatically.

### `g:scavenger_auto_clean_up_trailing_spaces_only_added`

Enable to clear trailing spaces on the current changes. Work with `g:scavenger_auto_clean_up_on_write` setting.

- default value: `0`
- value `1`: Clear trailing spaces on added lines when save files automatically.
- value `0`: Clear ALL trailing spaces when save files automatically.

### `g:scavenger_exclude_on_trailing_space`

An exclusive list of filetypes used to not clean up trailing spaces when call `CleanUp`.

- default value: `[]`

### `g:scavenger_exclude_on_blank_lines`

An exclusive list of filetypes used to not clean up blank lines when call `CleanUp`. It is useful on Python for PEP8-compliant.

- default value: `[]`

For example:

```
# do not clean up multiple blank lines for PEP8-compliant
let g:scavenger_exclude_on_blank_linse = ['python']
```
