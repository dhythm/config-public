#!/usr/bin/env python3
"""
Whisperを使用して音声ファイルを文字起こしするスクリプト。

Usage:
    python transcribe.py <input_audio> <output_json>

Example:
    python transcribe.py temp/voice_audio.wav temp/whisper_result.json
"""

import json
import sys
from pathlib import Path


def transcribe_audio(
    audio_path: str,
    model_name: str = "large-v3",
    language: str = "ja",
) -> dict:
    """
    Whisperで音声ファイルを文字起こしする。

    Args:
        audio_path: 入力音声ファイルのパス
        model_name: Whisperモデル名（large-v3, medium など）
        language: 言語コード

    Returns:
        Whisperの出力結果
    """
    import whisper

    try:
        print(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
    except Exception as e:
        if model_name == "large-v3":
            print(f"Failed to load {model_name}, falling back to medium: {e}")
            model_name = "medium"
            model = whisper.load_model(model_name)
        else:
            raise

    print(f"Transcribing: {audio_path}")
    result = model.transcribe(
        audio_path,
        language=language,
        word_timestamps=True,
    )

    return result


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_audio> <output_json>")
        sys.exit(1)

    input_audio = sys.argv[1]
    output_json = sys.argv[2]

    if not Path(input_audio).exists():
        print(f"Error: Input file not found: {input_audio}")
        sys.exit(1)

    result = transcribe_audio(input_audio)

    # 統計情報を出力
    total_chars = sum(len(seg["text"]) for seg in result["segments"])
    total_words = sum(
        len(seg.get("words", [])) for seg in result["segments"]
    )
    print(f"\n=== Transcription Results ===")
    print(f"Segments: {len(result['segments'])}")
    print(f"Total characters: {total_chars}")
    print(f"Total words: {total_words}")

    # 結果を保存
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_json}")


if __name__ == "__main__":
    main()
