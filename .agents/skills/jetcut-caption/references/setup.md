# 環境構築手順

このスキルを使用するための環境構築手順。

## 前提条件

- Homebrew がインストール済み
- macOS または Linux

## 1. 基本ツールのインストール

```bash
# ffmpeg
brew install ffmpeg

# Node.js (v18以上)
brew install node

# Python (3.10以上推奨)
brew install python

# uv (Python パッケージマネージャー)
brew install uv
```

## 2. Python 環境の作成

プロジェクトディレクトリで以下を実行：

```bash
# Python環境を初期化
uv init --python 3.11

# 必要なパッケージをインストール
uv add openai-whisper torch torchaudio silero-vad budoux
```

### トラブルシューティング

- **torchaudio 2.9以降**: `torchcodec` が必要な場合がある
  ```bash
  uv add torchcodec
  ```

- **Apple Silicon (M1/M2/M3)**: GPU対応版のtorchを使用
  ```bash
  uv add torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  ```

## 3. Whisper モデルのダウンロード

Whisperを初めて使用する際に自動でダウンロードされる。
事前にダウンロードしたい場合：

```python
import whisper
model = whisper.load_model("large-v3")
```

モデルサイズ一覧：
- `large-v3`: 最高精度、約3GB、VRAM 10GB推奨
- `medium`: バランス型、約1.5GB、VRAM 5GB推奨
- `small`: 軽量、約500MB
- `base`: 最軽量、約150MB

メモリが不足する場合は `medium` を使用する。

## 4. Remotion プロジェクトのセットアップ

```bash
# Remotionプロジェクトを作成
npx create-video@latest

# 対話形式の質問:
# - プロジェクト名: remotion-project
# - テンプレート: Blank
# - パッケージマネージャー: npm

# プロジェクトディレクトリに移動
cd remotion-project

# 追加パッケージをインストール
npm install budoux @remotion/google-fonts

# Remotionスキルを追加（オプション）
npx skills add remotion-dev/skills

# ルートディレクトリに戻る
cd ..
```

## 5. 確認

以下が準備できていることを確認：

- [ ] `ffmpeg -version` が動作する
- [ ] `uv run python -c "import whisper"` が動作する
- [ ] `uv run python -c "import silero_vad"` が動作する
- [ ] `uv run python -c "import budoux"` が動作する
- [ ] Remotionプロジェクトが存在する

すべてOKなら環境構築完了。
