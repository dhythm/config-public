#!/usr/bin/env python3
"""
Silero VADを使用して音声区間を検出するスクリプト。

Usage:
    python detect_speech.py <input_audio> <output_json>

Example:
    python detect_speech.py temp/audio_16k.wav temp/speech_segments.json
"""

import json
import sys
from pathlib import Path

import torch

torch.set_num_threads(1)

from silero_vad import get_speech_timestamps, load_silero_vad, read_audio


def detect_speech_segments(
    audio_path: str,
    threshold: float = 0.5,
    min_silence_duration_ms: int = 400,
    speech_pad_ms: int = 150,
    min_speech_duration_ms: int = 250,
    sampling_rate: int = 16000,
) -> list[dict]:
    """
    音声ファイルから発話区間を検出する。

    Args:
        audio_path: 入力音声ファイルのパス
        threshold: VADの閾値（0.0〜1.0）
        min_silence_duration_ms: 無音と判定する最小時間（ミリ秒）
        speech_pad_ms: 発話区間の前後に追加するパディング（ミリ秒）
        min_speech_duration_ms: 発話と判定する最小時間（ミリ秒）
        sampling_rate: サンプリングレート

    Returns:
        発話区間のリスト [{"start": float, "end": float}, ...]
    """
    model = load_silero_vad()
    wav = read_audio(audio_path, sampling_rate=sampling_rate)

    speech_timestamps = get_speech_timestamps(
        wav,
        model,
        threshold=threshold,
        min_silence_duration_ms=min_silence_duration_ms,
        speech_pad_ms=speech_pad_ms,
        min_speech_duration_ms=min_speech_duration_ms,
        sampling_rate=sampling_rate,
    )

    segments = []
    for ts in speech_timestamps:
        segments.append(
            {
                "start": ts["start"] / sampling_rate,
                "end": ts["end"] / sampling_rate,
            }
        )

    return segments


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_audio> <output_json>")
        sys.exit(1)

    input_audio = sys.argv[1]
    output_json = sys.argv[2]

    if not Path(input_audio).exists():
        print(f"Error: Input file not found: {input_audio}")
        sys.exit(1)

    print(f"Detecting speech segments in: {input_audio}")
    segments = detect_speech_segments(input_audio)
    print(f"Found {len(segments)} speech segments")

    if segments:
        total_speech = sum(s["end"] - s["start"] for s in segments)
        print(f"Total speech duration: {total_speech:.2f} seconds")

    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"Saved segments to: {output_json}")


if __name__ == "__main__":
    main()
