---
allowed-tools: Bash(gh:*), Bash(git:*)
description: Update a PR description
---

## Input 

#$ARGUMENtS

## Context

- Current git status: !`git status`
- Changes in this PR: !`git diff master...HEAD`
- Commits in this PR: !`git log --oneline master..HEAD`
- PR template: @.github/PULL_REQUEST_TEMPLATE.md

## Implementation

対象の PR の記載内容と、現在のソースコードを確認し、内容が不適切な場合は更新を提案する。
