# Powerlevel10k Instant Prompt
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# プラグイン
# `source $ZSH/oh-my-zsh.sh` より前で実行
plugins=(git)

# Oh-My-Zsh の設定
export ZSH="$HOME/.oh-my-zsh"
source $ZSH/oh-my-zsh.sh

# Powerlevel10k の設定
source $ZSH/custom/themes/powerlevel10k/powerlevel10k.zsh-theme
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# 環境変数
export LANG=ja_JP.UTF-8
export VOLTA_HOME="$HOME/.volta"
export PATH="$VOLTA_HOME/bin:$HOME/.local/bin:$HOME/.deno/bin:$PATH"

# anyenv 初期化
eval "$(anyenv init -)"

# Zsh のオプション
setopt IGNOREEOF share_history histignorealldups

# ヒストリー設定
HISTFILE=~/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

# カラー設定
autoload -Uz colors
colors
export LSCOLORS=gxfxcxdxbxegedabagacag
export LS_COLORS='di=36;40:ln=35;40:so=32;40:pi=33;40:ex=31;40:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;46'

# コマンド補完の最適化
autoload -Uz compinit
compinit -u

# キーバインド
bindkey "^P" up-line-or-beginning-search
bindkey "^N" down-line-or-beginning-search

# エイリアス設定
alias ls='ls -lhGF'
alias cp='cp -iv'
alias mv='mv -iv'
alias rm='rm -iv'
alias reload='source ~/.zshrc'
alias mvim='open -a /Applications/MacVim.app/Contents/MacOS/MacVim'
alias simrec='xcrun simctl io booted recordVideo rec.mp4'

# Git エイリアス
alias ga='git add'
alias gaa='git add .'
alias gaaa='git add --all'
alias gau='git add --update'
alias gb='git branch'
alias gbd='git branch -D '
alias gc='git commit'
alias gcm='git commit --message'
alias gcf='git commit --fixup'
alias gco='git checkout'
alias gcob='git checkout -b'
alias gcom='git checkout master'
alias gcos='git checkout staging'
alias gcod='git checkout develop'
alias gd='git diff'
alias gda='git diff HEAD'
alias gi='git init'
alias glg='git log --graph --oneline --decorate --all'
alias gld='git log --pretty=format:"%h %ad %s" --date=short --all'
alias gm='git merge --no-ff'
alias gma='git merge --abort'
alias gmc='git merge --continue'
alias gp='git pull'
alias gpo='git pull origin'
alias gpom='git pull origin master'
alias gpoc='git pull origin `git rev-parse --abbrev-ref HEAD`'
alias gpuoc='git pull origin HEAD'
alias gpr='git pull --rebase'
alias gpuo='git push origin'
alias gpuom='git push origin master'
alias gr='git rebase'
alias gs='git status'
alias gss='git status --short'
alias gst='git stash'
alias gsta='git stash apply'
alias gstd='git stash drop'
alias gstl='git stash list'
alias gstp='git stash pop'
alias gsts='git stash save'
