#---------------------------------------------------------------------
# config of zsh
#---------------------------------------------------------------------
echo ""
echo " ############################### "
echo "        Welcome to macOS!        "
echo " ############################### "
echo ""
#---------------------------------------------------------------------
# 変数の設定
#---------------------------------------------------------------------
export NVM_DIR="~/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
#---------------------------------------------------------------------
# パスの設定
#---------------------------------------------------------------------
export PYENV_ROOT="$HOME/.pyenv"

export PATH=""
export PATH="$PATH:./node_modules/.bin"
export PATH="$PATH:$PYENV_ROOT/bin"
export PATH="$PATH:$HOME/bin"
export PATH="$PATH:/usr/local/bin"
export PATH="$PATH:/usr/sbin"
export PATH="$PATH:/usr/bin"
export PATH="$PATH:/sbin"
export PATH="$PATH:/bin"
eval "$(pyenv init -)"

#---------------------------------------------------------------------
# UNIX の設定
#---------------------------------------------------------------------
# Ctrl+D でログアウトすることを防ぐ
setopt IGNOREEOF

# 日本語設定
export LANG=ja_JP.UTF-8

# 色
autoload -Uz colors
colors
export LSCOLORS=gxfxcxdxbxegedabagacag
export LS_COLORS='di=36;40:ln=35;40:so=32;40:pi=33;40:ex=31;40:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;46'


# 補完 / 修正
autoload -Uz compinit
compinit
# setopt correct

# 履歴
setopt share_history
setopt histignorealldups
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

# プロンプト
# PROMPT="%m:%/%# "
PROMPT="%(?.%{${fg[green]}%}.%{${fg[red]}%})%n${reset_color}@${fg[blue]}%m${reset_color}(%*%) %~
%# "

# alias
alias ls='ls -lhGF'
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'
alias reload='source ~/.zshrc'
alias geth_start='geth --networkid "10" --nodiscover --datadir ~/local/eth_private --rpc --rpcaddr "localhost" --rpcport "8545" --rpccorsdomain "*" --rpcapi "eth,net,web3,personal" --targetgaslimit "20000000" console 2>> ~/local/eth_private/geth_err.log'
alias wallet2geth='/Applications/Ethereum\ Wallet.app/Contents/MacOS/Ethereum\ Wallet --rpc http://localhost:8545'
alias mvim='open -a /Applications/MacVim.app/Contents/MacOS/MacVim'
# alias code='open -a /Applications/Visual\ Studio\ Code.app'
alias simrec='xcrun simctl io booted recordVideo rec.mp4'
alias simlist='xcrun simctl list'
alias simkill='xcrun simctl erase all'
