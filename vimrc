"---------------------------------------------------------------------------
" Maintainer:   Yuta Okada
"---------------------------------------------------------------------------
scriptencoding utf-8
"---------------------------------------------------------------------------
" 全体に関する設定

" 折りたたみ設定
set foldtext=Foldtext()
set foldcolumn=3
set fillchars=vert:\|
hi Folded gui=bold term=standout ctermbg=LightGrey ctermfg=DarkBlue guibg=Grey30 guifg=Grey80
hi FoldColumn gui=bold term=standout ctermbg=LightGrey ctermfg=DarkBlue guibg=Grey guifg=DarkBlue


"---------------------------------------------------------------------------
" 検索の挙動に関する設定

" 検索時に大文字小文字を区別しない
set ignorecase
" 大文字小文字が両方含まれる場合は区別する
set smartcase
" ファイルの最後まで検索すると最初に戻る
set wrapscan
" 挙動を vi 互換ではなく、Vim のデフォルト設定にする
set nocompatible

"---------------------------------------------------------------------------
" 編集に関する設定

" IMEのオン/オフ
"set imdisable
" ヤンクとクリップボードを共有
set clipboard=unnamed,autoselect
" タブ文字の画面上での幅
set tabstop=4
" <Tab>キーを押下時に半角スペースを挿入
set expandtab
" <Tab>キー押下時に挿入される空白の量
set softtabstop=4
" 自動インデント設定
set autoindent
" インデントの画面上での幅
set shiftwidth=4
" カーソルを行頭、行末で止まらないようにする
" set whichwrap=b,s,h,l,<,>,[,]
" バックスペースでインデントや改行を削除可能にする
set backspace=indent,eol,start
" 対応する括弧を表示する
set showmatch
" カーソルの移動時間(1->0.1秒)
set matchtime=1
" コマンドライン補完の拡張
set wildmenu
" テキスト挿入中の自動折り返しを日本語に対応させる
set formatoptions+=mM
" 改行時の自動コメントアウトを無効にする
set formatoptions-=ro
" 自動改行を無効にする
set formatoptions=q
" 補完メニューの高さ
set pumheight=10
"---------------------------------------------------------------------------
" 表示に関する設定

" 行番号を表示
set number
" ルーラーを表示
set ruler
" タブや改行を表示
set list
" 特殊文字の表示設定
set listchars=tab:>.,trail:_,extends:>,precedes:<,nbsp:%
" 行を折り返して表示
set wrap
" 折り返しの際に全量表示する
set display=lastline
" 暗い背景色に合わせた配色にする
set background=dark
" ステータス行を表示
set laststatus=2
" コマンドラインの高さの設定
set cmdheight=2
" コマンドをステータス行に表示
set showcmd
" タイトルを表示
set title
" エンコード設定
set encoding=utf-8
set fileencodings=utf-8,iso-2022-jp,euc-jp,sjis
set fileformats=unix,dos,mac

" 構文毎に文字色を変化させる
syntax on
" カラースキーマの指定
colorscheme desert
" 行番号の色
highlight LineNr ctermfg=darkyellow
"---------------------------------------------------------------------------
" ファイル操作に関する設定

" ファイル変更後のバックアップを作成しない
set nobackup
" ファイル変更後のバックアップ(上書きに成功すると削除)を作成する
set writebackup
" 編集前の作業コピーを作成しない
set noswapfile
" Undo情報の保存ファイルを作成しない
set noundofile
" バッファリスト移動時に保存を強制しない
set hidden

" 新しいウィンドウを開く方向
set splitbelow
set splitright

"---------------------------------------------------------------------------
" キーマップ設定

imap ( ()<Left>
imap [ []<Left>
imap { {}<Left>
nnoremap Y y$
nnoremap <silent> <C-l> :<C-u>nohlsearch<CR><C-l>
nnoremap <silent> [b :bprevious<CR>
nnoremap <silent> ]b :bnext<CR>
nnoremap <silent> [B :bfirst<CR>
nnoremap <silent> ]B :blast<CR>
inoremap <silent> jj <ESC>
cnoremap <C-p> <Up>
cnoremap <C-n> <Down>
" Split window
nmap Ss :split<Return><C-w>w
nmap Sv :vsplit<Return><C-w>w
" Move window
nmap <Space> <C-w>w
nmap Sh <C-w>h
nmap Sk <C-w>k
nmap Sj <C-w>j
nmap Sl <C-w>l
" Resize window
nmap <C-w><left> <C-w><
nmap <C-w><right> <C-w>>
nmap <C-w><up> <C-w>+
nmap <C-w><down> <C-w>-
" Move tab
nnoremap <Tab> :Tabnext<Return>
nnoremap <S-Tab> :Tabprev<Return>

"---------------------------------------------------------------------------
" Neobundle に関する設定

" vim の起動時のみ runtimepath に neobundle.vim を追加する
if has('vim_starting')
    set runtimepath+=~/.vim/bundle/neobundle.vim
endif

call neobundle#begin(expand('~/.vim/bundle'))
    NeoBundleFetch 'Shougo/neobundle.vim'

    NeoBundle 'Shougo/unite.vim'
    NeoBundle 'Shougo/neomru.vim'

    NeoBundle 'Shougo/neocomplcache'
    NeoBundle 'Shougo/neosnippet'
    NeoBundle 'Shougo/neosnippet-snippets'

    NeoBundle 'nathanaelkane/vim-indent-guides'
    NeoBundle 'itchyny/lightline.vim'
    NeoBundle 'pangloss/vim-javascript'
    NeoBundle 'vim-scripts/AnsiEsc.vim'
    NeoBundle 'leafgarland/typescript-vim.git'

    NeoBundle 'plasticboy/vim-markdown'
    NeoBundle 'kannokanno/previm'
    NeoBundle 'tyru/open-browser.vim'

"    NeoBundle 'scrooloose/nerdtree'
call neobundle#end()

NeoBundleCheck

"---------------------------------------------------------------------------
" neobundle-snippet に関する設定

" Plugin key-mappings.
" Note: It must be "imap" and "smap".  It uses <Plug> mappings.
imap <C-k>     <Plug>(neosnippet_expand_or_jump)
smap <C-k>     <Plug>(neosnippet_expand_or_jump)
xmap <C-k>     <Plug>(neosnippet_expand_target)

" SuperTab like snippets behavior.
" Note: It must be "imap" and "smap".  It uses <Plug> mappings.
imap <C-k>     <Plug>(neosnippet_expand_or_jump)
imap <expr><TAB>
  \ pumvisible() ? "\<C-n>" :
  \ neosnippet#expandable_or_jumpable() ?
  \    "\<Plug>(neosnippet_expand_or_jump)" : "\<TAB>"
smap <expr><TAB> neosnippet#expandable_or_jumpable() ?
  \ "\<Plug>(neosnippet_expand_or_jump)" : "\<TAB>"

" For conceal markers.
" if has('conceal')
"   set conceallevel=2 concealcursor=niv
" endif

" snippets ファイルの参照ディレクトリ
let g:neosnippet#snippets_directory='~/.vim/bundle/neosnippet-snippets/snippets/,~/.vim/snippets'
" 開始時に neocomplcache を起動する
let g:neocomplcache_enable_at_startup = 1
" smartcase(大文字小文字の区別)の設定
let g:neocomplcache_enable_smart_case = 1
" _ の補完を有効化
let g:neocomplcache_enable_underbar_completion = 1
" syntax の最小文字数を設定
let g:neocomplcache_min_syntax_length = 3

"---------------------------------------------------------------------------
" Markdown に関する設定

au BufRead,BufNewFile *.md set filetype=markdown
if has('mac')
  let g:previm_open_cmd = 'open -a Google\ Chrome'
endif

"---------------------------------------------------------------------------
" NERDTree に関する設定

" 隠しファイルを表示する
" let NERDTreeShowHidden = 1
" ファイル指定で開かれた場合はNERDTreeは表示しない
" if !argc()
"   autocmd vimenter * NERDTree|normal gg3j
" endif
" 他のバッファをすべて閉じた時にNERDTreeが開いていたらNERDTreeも一緒に閉じる。
" autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

"---------------------------------------------------------------------------
" vim-indent-guides の設定
" インデントを可視化
let g:indent_guides_enable_on_vim_startup = 1

"---------------------------------------------------------------------------
" ファイルタイプ/プラグイン/インデントの検出

filetype plugin indent on
"---------------------------------------------------------------------------
