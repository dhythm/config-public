if exists('g:vscode')
    " VSCode extension
else
    " ordinary Neovim
    " Search
    set nocompatible
    set path+=**
    set wildmenu

    " Edit configurations
    set tabstop=2
    set expandtab
    set softtabstop=2
    set autoindent
    set shiftwidth
    set backspace=indent,eol,start
    set showmatch
    set matchtime=1
    set formatoptions+=mM
    set formatoptions-=ro
    set formatoptions=q
    set pumheight=10

    " Display configurations
    set number
    set ruler
    set list
    set listchars=tab:>.,trail:_,extends:>,precedes:<,nbsp:%
    set wrap
    set display=lastline
    set laststatus
    set cmdheight=2
    set showcmd
    set title
    set encoding=utf-8
    set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
    set fileformats=unix,dos,mac
    syntax on

    " Keymaps
    imap ( ()<Left>
    imap [ []<Left>
    imap { {}<Left>
    cnoremap <C-p> <Up>
    cnoremap <C-n> <Down>
endif
