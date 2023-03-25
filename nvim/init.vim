source ~/.vimrc
autocmd InsertLeave * :silent !/usr/local/bin/im-select com.apple.inputmethod.Kotoeri.RomajiTyping.Roman

" PLUGIN SETTINGS
call plug#begin('~/.config/nvim/plugged')

Plug 'tpope/vim-surround'
Plug 'lambdalisue/fern.vim'

call plug#end()
