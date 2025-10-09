---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Generate PR description and automatically create pull request on GitHub
---

## Context

- Current git status: `git status`
- Show default branch: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`
- Changes in this PR: `git diff $(gh repo view --json defaultBranchRef --jq -r '.defaultBranchRef.name')...HEAD`
- Commits in this PR: `git log --oneline $(gh repo view --json defaultBranchRef --jq -r '.defaultBranchRef.name')..HEAD`
- PR template: @.github/PULL_REQUEST_TEMPLATE.md

## Implementation

適切な粒度でコミットし、PR を作成してください。
PR はデフォルトブランチ向けに作成してください。
**重要: `gh pr create` コマンドでは `--base` オプションを指定しないでください。デフォルトでリポジトリのデフォルトブランチが使用されます。**
**使用例:** `/create-pr` → 自動で PR 作成完了
