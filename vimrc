"---------------------------------------------------------------------------
" Last Change:  2017/12/30
" Maintainer:   Yura Okada
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

"---------------------------------------------------------------------------
" 編集に関する設定

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
set fileencodings=iso-2022-jp,euc-jp,sjis,utf-8
set fileformats=unix,dos,mac

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

" 新しいウィンドウを開く方向
set splitbelow
set splitright

"---------------------------------------------------------------------------
" キーマップ設定

imap ( ()<Left>
imap [ []<Left>
imap { {}<Left>
nnoremap Y y$

"---------------------------------------------------------------------------
" Neobundle に関する設定

" vim の起動時のみ runtimepath に neobundle.vim を追加する
if has('vim_starting')
    set runtimepath+=~/.vim/bundle/neobundle.vim
endif

call neobundle#begin(expand('~/.vim/bundle'))
    NeoBundleFetch 'Shougo/neobundle.vim'

    NeoBundle 'Shougo/unite.vim'
    NeoBundle 'Shougo/neocomplcache'
    NeoBundle 'Shougo/neosnippet'
    NeoBundle 'Shougo/neosnippet-snippets'

    NeoBundle 'itchyny/lightline.vim'
    NeoBundle 'plasticboy/vim-markdown'
    NeoBundle 'kannokanno/previm'
    NeoBundle 'tyru/open-browser.vim'
    NeoBundle 'pangloss/vim-javascript'
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
" ファイルタイプ/プラグイン/インデントの検出
" ※なるべく最後に記載する
filetype plugin indent on
"---------------------------------------------------------------------------
