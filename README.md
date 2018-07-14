# VS Code

Vim Keybinding で連続入力できない場合の対策は下記の通り。
```
$ defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false         # For VS Code
$ defaults write com.microsoft.VSCodeInsiders ApplePressAndHoldEnabled -bool false # For VS Code Insider
```

VSCodeVim では、Insert mode から Normal mode に戻る際に IME をトグル出来ない。  
Google IME 環境設定上のことえりカスタムキーマップ設定で、
```
入力文字なし(Precomposition)の場合に　"Ctrl+[" で　IME を無効化(Cancel and directive IME)を設定すること
```
で実現することが可能。  
ただし、その場合に　MacVim　の　IME Toggle　機能が正しく動かないことを検知している。
