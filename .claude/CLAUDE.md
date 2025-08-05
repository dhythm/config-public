# CLAUDE.md

## ガイドライン

NEVER: パスワードやAPIキーをハードコーディングしない
NEVER: ユーザーの確認なしにリモート環境に更新をかけるスクリプトを実行しない

YOU MUST: 日本語で回答する
YOU MUST: エラーハンドリングを実装
YOU MUST: 変更前に既存テストが通ることを確認

IMPORTANT: パフォーマンスへの影響を考慮
IMPORTANT: 後方互換性を維持
IMPORTANT: セキュリティベストプラクティスに従う
IMPORTANT: コードエクセレンス原則に基づき、テスト駆動開発（TDD）を実施する
IMPORTANT: TDDを実践する際は t-wada の推奨する進め方に従う
IMPORTANT: リファクタリングは Martin Fowler が推奨する進め方に従う
IMPORTANT: TypeScript を書くときは原則として function を利用する（class を利用しない）
