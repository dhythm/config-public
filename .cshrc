#---------------------------------------------------------------------
# config of csh
#---------------------------------------------------------------------
# banner
echo ""
echo " ############################### "
echo "       Welcome to MacOSX !       "
echo " ############################### "
echo ""
#---------------------------------------------------------------------
# ファイル・ディレクトリ作成のパーミッション設定
umask   022

# パス設定
set path = ""
set path = ($path /bin)
set path = ($path /usr/bin)
set path = ($path /usr/sbin)
set path = ($path /usr/local/bin)
set path = ($path $HOME/bin)
set path = ($path $HOME/local/bin)

# python 設定
set path = ($path $HOME/.pyenv/versions/anaconda3-4.2.0/bin)

#---------------------------------------------------------------------
# shell の設定
#---------------------------------------------------------------------
# skip remaining setup if not an interactive shell
if ($?USER == 0 || $?prompt == 0) exit

# TABキーで候補の表示
set autolist
# histroy の設定
set history=100
set savehist=(100 merge)
# %m:ホスト名 $/:カレントディレクトリ
set prompt="%m:%/%# "
# file名の補完を行う(cshのみの機能)
set filec

# 補完設定
complete cd 'p/1/d/'
complete open 'p/*/d/'
complete open 'p/*/f:{*.{c,cc,dat,eps,h,jpg,key,mk,pages,pdf,plt,png,ps,rtf,sh,tex,txt},Makefile,.*}/'
complete {dataview,dofft,doifft} 'p/*/f:*.{dat,txt}/'

#---------------------------------------------------------------------
# UNIX コマンドの設定
#---------------------------------------------------------------------
# ls の設定
setenv LSCOLORS gxfxxxxxcxxxxxxxxxxxxx

# aliases の設定
alias cd        'cd \!*;echo $cwd'
alias cp        'cp -iv'
alias mv        'mv -iv'
alias rm        'rm -iv'
alias ls        'ls -FG'    # F:--classify, G:--no-group
alias rsync     'rsync -avu --delete --stats --progress'

alias pwd       'echo $cwd'
alias reload     source ~/.cshrc
alias updatedb  'sudo /usr/libexec/locate.updatedb'

alias MacVim    'open -a /Applications/MacVim.app/Contents/MacOS/MacVim'

