---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Commit the current work with conventional commits
---

# Commit with proper message

## Instructions

1. `git diff --cached --quiet` で staged 変更の有無を判定する
   - staged 変更が **ある** 場合（exit code が 0 以外）→ `git add` は実行せず、staged のものだけを対象にする
   - staged 変更が **ない** 場合（exit code が 0）→ `git add -A` で全変更をステージする
2. `git --no-pager diff --cached`
3. Think commit_message in English from the staged diff
4. `git commit -m <commit_message>`

## Guideline

- コミットメッセージは修正内容を元に考えてください。
- follow Conventional Commits
- staged / unstaged が混在している場合は、ユーザーが意図的に staged したものだけをコミット対象とし、unstaged を巻き込まない。
