---
name: jetcut-caption
description: |
  Automatically cuts silent parts of videos (jet cut) and adds AI-generated subtitles using Whisper transcription.
  Use this skill when the user wants to:
  - Add subtitles/captions to a video
  - Remove silent parts from a video (jet cut, jump cut)
  - Edit video with automatic captioning
  - Transcribe video and generate subtitles
  Input: video file (mp4, mov, webm, etc.) Output: video with subtitles and silent parts removed.
---

# Jetcut Caption

動画の無音部分を自動カット（ジェットカット）し、AI文字起こしで高品質な字幕テロップを追加するスキル。

## 処理の流れ

1. **環境確認** - 必要なツールがなければセットアップ
2. **音声抽出** - 動画から音声を抽出
3. **ジェットカット** - Silero VADで無音区間を検出し、無音部分をカット
4. **文字起こし** - Whisperで音声をテキスト化
5. **字幕生成** - BudouXで自然な日本語分割、LLMで校正
6. **動画レンダリング** - Remotionで字幕を合成して出力

## 環境確認

作業を始める前に、以下の環境を確認する。不足があれば `references/setup.md` を読んでセットアップを実行する。

### 必須ツール
- ffmpeg（音声抽出・動画変換）
- Python環境（uv または poetry）
- Node.js v18以上

### 必須Pythonパッケージ
- openai-whisper
- torch, torchaudio
- silero-vad
- budoux

### 必須モデル
- Whisper large-v3（または medium をフォールバック）

### Remotionプロジェクト
- プロジェクトが存在しない場合は作成が必要

環境が整っていない場合は、ユーザーに確認の上でセットアップを実行する。

---

## Step 1: 音声抽出

入力動画から音声を抽出する。

```bash
mkdir -p temp output
ffmpeg -y -i "<入力動画>" -ar 16000 -ac 1 temp/audio_16k.wav
ffmpeg -y -i "<入力動画>" -ar 44100 -ac 1 temp/voice_audio.wav
```

- `audio_16k.wav`: VAD用（16kHz）
- `voice_audio.wav`: Whisper用・最終出力用（44.1kHz）

---

## Step 2: ジェットカット（無音カット）

`scripts/detect_speech.py` を実行して音声区間を検出する。

```bash
uv run scripts/detect_speech.py temp/audio_16k.wav temp/speech_segments.json
```

検出した音声区間を使って `scripts/jetcut.py` で無音部分をカットする。

```bash
uv run scripts/jetcut.py "<入力動画>" temp/speech_segments.json temp/cut_video.mp4
```

カット前後の秒数とカット率をログに出力する。

---

## Step 3: カット済み動画から音声を再抽出

```bash
ffmpeg -y -i temp/cut_video.mp4 -ar 44100 -ac 1 temp/voice_audio.wav
```

---

## Step 4: Whisper文字起こし

`scripts/transcribe.py` を実行する。

```bash
uv run scripts/transcribe.py temp/voice_audio.wav temp/whisper_result.json
```

- large-v3を使用（メモリ不足時はmediumにフォールバック）
- word_timestamps=True で単語レベルのタイムスタンプを取得

---

## Step 5: 字幕生成

`scripts/generate_subtitles.py` を実行する。動画の向きでコマンドを使い分ける。

```bash
# 横型動画（原則1行）
uv run scripts/generate_subtitles.py temp/whisper_result.json temp/subtitles.json

# 縦型動画（横幅が狭いため2行を許容、1行は短めに）
uv run scripts/generate_subtitles.py temp/whisper_result.json temp/subtitles.json --two-line-mode --max-line-chars 12
```

### 字幕生成ルール

1. **行数**: 原則1テロップ=1行（横型動画）。2行は例外で、分割すると表示時間が0.6秒未満になる場合のみ隣のテロップと結合して2行にする。縦型動画は `--two-line-mode` で2行分割を標準とする
2. **文字数制限**: 1行最大20文字（横型）/ 12文字（縦型）。超える場合は読点や文節境界で別テロップに分割
3. **フォントサイズ**: 文字量によらず全テロップ固定（既定48px、1080p基準）。テロップごとにサイズを変えない
4. **時間按分**: 分割時はstart/endを文字数比で按分

### 出力フォーマット

```json
[
  {
    "id": 0,
    "start": 0.5,
    "end": 2.3,
    "lines": ["原則1行のテキスト"],
    "fontSize": 48
  }
]
```

---

## Step 6: 字幕のLLM校正（重要）

字幕の品質は動画全体の品質を左右する。`temp/subtitles.json` を読み込み、以下の校正を行う。

### 校正項目

1. **誤字・誤変換の修正**
   - Whisperの認識ミスを修正
   - 同音異義語の正しい選択

2. **専門用語・固有名詞の校正**
   - 技術用語、製品名、人名などを正しい表記に
   - ユーザーから文脈情報があれば活用

3. **表記揺れの統一**
   - 同じ言葉は同じ表記に統一
   - 数字の表記（漢数字/アラビア数字）を統一

4. **自然な区切り位置**
   - 意味の切れ目で改行
   - 助詞だけが次の行に行かないよう調整

5. **読みやすさの確認**
   - 1行あたりの文字数バランス
   - 表示時間に対して読める文字数か

### 校正のやり方

1. `temp/subtitles.json` を読み込む
2. 全テロップを通して内容を把握
3. 上記の観点で校正
4. 修正後、同じファイルを上書き保存

校正以外の変更（内容の追加・削除）は行わない。

---

## Step 7: 動画情報の取得と変換

ffprobeでtemp/cut_video.mp4の情報を確認する。

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,codec_name,pix_fmt,r_frame_rate -of json temp/cut_video.mp4
```

以下のいずれかに該当する場合は変換が必要：
- HEVC(H.265) または AV1 コーデック
- 10bit色深度
- 30fps以外のフレームレート

変換コマンド:
```bash
ffmpeg -y -i temp/cut_video.mp4 -c:v libx264 -pix_fmt yuv420p -r 30 -preset fast -crf 18 -c:a aac -b:a 192k temp/cut_video_converted.mp4
/bin/cp -f temp/cut_video_converted.mp4 temp/cut_video.mp4
rm temp/cut_video_converted.mp4
```

---

## Step 8: Remotionコンポーネント生成

`templates/` ディレクトリのテンプレートを使用してsrc/に配置する。

### Root.tsx
`templates/Root.tsx` をコピーし、以下の値を実際の値に置き換える：
- `durationInFrames`: カット済み動画の秒数 × 30
- `width` / `height`: **1080p基準の固定値**を使う（横型: 1920x1080 / 縦型: 1080x1920）。
  動画の実解像度が低くても、コンポジションは1080p基準にして動画側を `objectFit: "contain"` でスケールする。
  フォントサイズ（固定px）が1080p前提のため、動画の実寸をそのまま使うと低解像度動画で字幕が過大になる。
  ただし動画のアスペクト比が16:9/9:16と異なる場合は、アスペクト比を保ったまま長辺を1920に合わせる。

### MainVideo.tsx, Subtitle.tsx
`templates/` からそのままコピー。

---

## Step 9: 静的ファイルの配置

```bash
cp temp/cut_video.mp4 public/
cp temp/voice_audio.wav public/
cp temp/subtitles.json public/
```

---

## Step 10: Remotionレンダリング

```bash
npx remotion render MainVideo output/final.mp4 --timeout=120000
```

エラー時の対応:
- タイムアウト: `npx remotion upgrade` を実行してから再試行
- その他のエラー: エラー内容を分析してソースコードを修正

---

## Step 11: 完了

```bash
open output/final.mp4
```

最終報告:
- カット前後の秒数とカット率
- テロップの件数
- 出力ファイルのパス

---

## エラー時の自動リカバリ

各ステップでエラーが発生した場合：
1. エラー内容を分析
2. 原因を特定して修正
3. そのステップを再実行
4. 成功したら次のステップへ

途中で止まらず、最後まで自動で実行すること。
