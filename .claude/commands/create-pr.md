---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Generate PR description and automatically create pull request on GitHub
---

## Context

- Current git status: `git status`
- Changes in this PR: `git diff master...HEAD`
- Commits in this PR: `git log --oneline master..HEAD`
- Show default branch: `gh repo view --json defaultBranchRef`
- PR template: @.github/PULL_REQUEST_TEMPLATE.md

## Implementation

適切な粒度でコミットし、PR を作成してください。
PR はデフォルトブランチ向けに作成してください。
**使用例:** `/create-pr` → 自動で PR 作成完了

