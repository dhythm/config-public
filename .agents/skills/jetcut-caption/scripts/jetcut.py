#!/usr/bin/env python3
"""
検出した音声区間を使って無音部分をカット（ジェットカット）するスクリプト。

Usage:
    python jetcut.py <input_video> <segments_json> <output_video>

Example:
    python jetcut.py input/video.mp4 temp/speech_segments.json temp/cut_video.mp4
"""

import json
import subprocess
import sys
from pathlib import Path


def get_video_duration(video_path: str) -> float:
    """ffprobeで動画の長さを取得する。"""
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        video_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def jetcut_simple(
    input_video: str, segments: list[dict], output_video: str
) -> None:
    """
    シンプルなfilter_complexで無音カットを実行する。
    セグメント数が少ない場合に使用。
    """
    if not segments:
        print("No segments to process, copying original video")
        subprocess.run(["cp", input_video, output_video], check=True)
        return

    filter_parts = []
    concat_inputs = []

    for i, seg in enumerate(segments):
        start = seg["start"]
        end = seg["end"]
        # ビデオとオーディオのトリム
        filter_parts.append(
            f"[0:v]trim=start={start}:end={end},setpts=PTS-STARTPTS[v{i}]"
        )
        filter_parts.append(
            f"[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS[a{i}]"
        )
        concat_inputs.append(f"[v{i}][a{i}]")

    # concat フィルターの入力順序: [v0][a0][v1][a1]...
    concat_filter = f"{''.join(concat_inputs)}concat=n={len(segments)}:v=1:a=1[outv][outa]"
    filter_parts.append(concat_filter)

    filter_complex = ";".join(filter_parts)

    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        input_video,
        "-filter_complex",
        filter_complex,
        "-map",
        "[outv]",
        "-map",
        "[outa]",
        "-c:v",
        "libx264",
        "-preset",
        "fast",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        output_video,
    ]

    subprocess.run(cmd, check=True)


def jetcut_chunked(
    input_video: str,
    segments: list[dict],
    output_video: str,
    chunk_size: int = 10,
) -> None:
    """
    チャンク方式で無音カットを実行する。
    セグメント数が多い場合（50個以上）に使用。
    """
    temp_dir = Path(output_video).parent / "jetcut_chunks"
    temp_dir.mkdir(parents=True, exist_ok=True)

    chunk_files = []

    # チャンクごとに処理
    for chunk_idx in range(0, len(segments), chunk_size):
        chunk_segments = segments[chunk_idx : chunk_idx + chunk_size]
        chunk_output = temp_dir / f"chunk_{chunk_idx:04d}.mp4"
        chunk_files.append(str(chunk_output))

        print(
            f"Processing chunk {chunk_idx // chunk_size + 1}/{(len(segments) + chunk_size - 1) // chunk_size}"
        )
        jetcut_simple(input_video, chunk_segments, str(chunk_output))

    # チャンクを結合
    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, "w") as f:
        for chunk_file in chunk_files:
            f.write(f"file '{chunk_file}'\n")

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list),
        "-c",
        "copy",
        output_video,
    ]
    subprocess.run(cmd, check=True)

    # 一時ファイルを削除
    for chunk_file in chunk_files:
        Path(chunk_file).unlink(missing_ok=True)
    concat_list.unlink(missing_ok=True)
    temp_dir.rmdir()


def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <input_video> <segments_json> <output_video>")
        sys.exit(1)

    input_video = sys.argv[1]
    segments_json = sys.argv[2]
    output_video = sys.argv[3]

    if not Path(input_video).exists():
        print(f"Error: Input video not found: {input_video}")
        sys.exit(1)

    if not Path(segments_json).exists():
        print(f"Error: Segments file not found: {segments_json}")
        sys.exit(1)

    with open(segments_json, encoding="utf-8") as f:
        segments = json.load(f)

    # 元の動画の長さを取得
    original_duration = get_video_duration(input_video)
    print(f"Original video duration: {original_duration:.2f} seconds")

    # ジェットカット実行
    Path(output_video).parent.mkdir(parents=True, exist_ok=True)

    if len(segments) >= 50:
        print(f"Using chunked processing for {len(segments)} segments")
        jetcut_chunked(input_video, segments, output_video)
    else:
        print(f"Processing {len(segments)} segments")
        jetcut_simple(input_video, segments, output_video)

    # カット後の動画の長さを取得
    cut_duration = get_video_duration(output_video)
    cut_rate = (1 - cut_duration / original_duration) * 100

    print(f"\n=== Jetcut Results ===")
    print(f"Original duration: {original_duration:.2f} seconds")
    print(f"Cut duration: {cut_duration:.2f} seconds")
    print(f"Cut rate: {cut_rate:.1f}%")
    print(f"Output: {output_video}")


if __name__ == "__main__":
    main()
