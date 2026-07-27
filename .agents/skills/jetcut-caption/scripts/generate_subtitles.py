#!/usr/bin/env python3
"""
Whisperの出力からテロップ用の字幕JSONを生成するスクリプト。
BudouXを使用して日本語の自然な文節で分割する。

原則1テロップ=1行（横型動画）。縦型動画は --two-line-mode で2行分割を許容する。
フォントサイズは文字量によらず固定（--font-size、既定48px / 1080p基準）。

Usage:
    python generate_subtitles.py <whisper_json> <output_json> [--max-line-chars N] [--two-line-mode] [--font-size N]

Example:
    # 横型動画（原則1行）
    python generate_subtitles.py temp/whisper_result.json temp/subtitles.json
    # 縦型動画（2行許容・1行短め）
    python generate_subtitles.py temp/whisper_result.json temp/subtitles.json --two-line-mode --max-line-chars 12
"""

import json
import sys
from pathlib import Path

import budoux

# 1行に収める最大文字数。原則1テロップ=1行とし、
# 表示時間が短くなりすぎる場合のみ例外的に2行へ結合する。
MAX_LINE_CHARS = 20
MIN_TELOP_DURATION = 0.6
DEFAULT_FONT_SIZE = 48


def merge_short_pieces(pieces: list[dict]) -> list[dict]:
    """
    表示時間が短すぎるテロップを隣と結合する（結合後は2行表示になる）。
    結合は例外ケースなので、文字数が2行に収まる場合のみ行う。
    """
    merged = []
    for piece in pieces:
        duration = piece["end"] - piece["start"]
        if (
            merged
            and duration < MIN_TELOP_DURATION
            and len(merged[-1]["text"]) + len(piece["text"]) <= MAX_LINE_CHARS * 2
        ):
            prev = merged[-1]
            prev["text"] += piece["text"]
            prev["end"] = piece["end"]
        else:
            merged.append(dict(piece))
    return merged


def split_into_two_lines(
    text: str, parser: budoux.Parser, max_line_chars: int | None = None
) -> list[str]:
    """
    テキストをBudouXで文節分割し、均等な2行に分割する。
    max_line_chars指定時は各行がその文字数に収まる分割位置を優先し、
    文節境界では収まらない場合は中央で強制分割する（校正ステップで調整する前提）。
    """
    chunks = parser.parse(text)
    total_len = len(text)
    target_len = total_len / 2

    # 文節境界の分割候補を列挙
    candidates = []
    current_len = 0
    for chunk in chunks[:-1]:
        current_len += len(chunk)
        candidates.append(current_len)

    if max_line_chars is not None:
        fitting = [
            c for c in candidates
            if c <= max_line_chars and total_len - c <= max_line_chars
        ]
        if fitting:
            split_at = min(fitting, key=lambda c: abs(c - target_len))
        elif total_len <= max_line_chars * 2:
            # 文節境界では収まらないので中央で強制分割
            split_at = (total_len + 1) // 2
        else:
            split_at = candidates[0] if candidates else (total_len + 1) // 2
    else:
        if not candidates:
            return [text]
        split_at = min(candidates, key=lambda c: abs(c - target_len))

    if split_at <= 0 or split_at >= total_len:
        return [text]

    return [text[:split_at], text[split_at:]]


def split_long_segment(
    text: str, start: float, end: float, parser: budoux.Parser, max_chars: int = MAX_LINE_CHARS
) -> list[dict]:
    """
    長いセグメントを複数のテロップに分割する。
    時間は文字数比で按分する。
    """
    if len(text) <= max_chars:
        return [{"text": text, "start": start, "end": end}]

    # BudouXで文節分割
    chunks = parser.parse(text)

    # 読点で優先的に分割
    result = []
    current_text = ""
    current_start = start

    total_duration = end - start
    total_chars = len(text)
    chars_processed = 0

    for chunk in chunks:
        # 読点が含まれている場合は分割ポイント
        if "、" in chunk or "。" in chunk:
            current_text += chunk
            if len(current_text) > 0:
                chars_processed += len(current_text)
                current_end = start + (chars_processed / total_chars) * total_duration
                result.append(
                    {
                        "text": current_text.strip(),
                        "start": current_start,
                        "end": current_end,
                    }
                )
                current_start = current_end
                current_text = ""
        elif len(current_text) + len(chunk) > max_chars:
            # 最大文字数を超える場合は分割
            if len(current_text) > 0:
                chars_processed += len(current_text)
                current_end = start + (chars_processed / total_chars) * total_duration
                result.append(
                    {
                        "text": current_text.strip(),
                        "start": current_start,
                        "end": current_end,
                    }
                )
                current_start = current_end
                current_text = ""
            current_text = chunk
        else:
            current_text += chunk

    # 残りを追加
    if current_text.strip():
        result.append(
            {
                "text": current_text.strip(),
                "start": current_start,
                "end": end,
            }
        )

    return result


def generate_subtitles(
    whisper_result: dict,
    max_line_chars: int = MAX_LINE_CHARS,
    two_line_mode: bool = False,
    font_size: int = DEFAULT_FONT_SIZE,
) -> list[dict]:
    """
    Whisperの出力から字幕JSONを生成する。

    Args:
        max_line_chars: 1行の最大文字数
        two_line_mode: Trueなら2行分割を標準とする（縦型動画向け）。
            Falseなら原則1行とし、表示時間が短すぎる場合のみ2行に結合する。
        font_size: 全テロップ共通の固定フォントサイズ（px）
    """
    parser = budoux.load_default_japanese_parser()
    subtitles = []
    subtitle_id = 0

    # 1テロップに入れる最大文字数: 原則1行モードでは1行分、2行モードでは2行分
    max_telop_chars = max_line_chars * 2 if two_line_mode else max_line_chars

    for segment in whisper_result.get("segments", []):
        text = segment.get("text", "").strip()
        start = segment.get("start", 0)
        end = segment.get("end", 0)

        if not text:
            continue

        # 長いセグメントを分割
        split_segments = split_long_segment(text, start, end, parser, max_telop_chars)

        # 原則1行モード: 表示時間が短すぎるテロップは例外的に隣と結合（→2行になる）
        if not two_line_mode:
            split_segments = merge_short_pieces(split_segments)

        for split_seg in split_segments:
            seg_text = split_seg["text"]
            seg_start = split_seg["start"]
            seg_end = split_seg["end"]

            # 行分割: 1行に収まらないものだけ2行にする
            if len(seg_text) <= max_line_chars:
                lines = [seg_text]
            else:
                lines = split_into_two_lines(seg_text, parser, max_line_chars)

            subtitles.append(
                {
                    "id": subtitle_id,
                    "start": round(seg_start, 3),
                    "end": round(seg_end, 3),
                    "lines": lines,
                    "fontSize": font_size,
                }
            )
            subtitle_id += 1

    return subtitles


def main():
    import argparse

    arg_parser = argparse.ArgumentParser(description="Whisper出力から字幕JSONを生成")
    arg_parser.add_argument("whisper_json")
    arg_parser.add_argument("output_json")
    arg_parser.add_argument(
        "--max-line-chars",
        type=int,
        default=MAX_LINE_CHARS,
        help="1行の最大文字数（横型: 20推奨 / 縦型: 12推奨）",
    )
    arg_parser.add_argument(
        "--two-line-mode",
        action="store_true",
        help="2行分割を標準とする（縦型動画向け）。指定なしは原則1行。",
    )
    arg_parser.add_argument(
        "--font-size",
        type=int,
        default=DEFAULT_FONT_SIZE,
        help="全テロップ共通の固定フォントサイズ（px、1080p基準）",
    )
    args = arg_parser.parse_args()

    whisper_json = args.whisper_json
    output_json = args.output_json

    if not Path(whisper_json).exists():
        print(f"Error: Input file not found: {whisper_json}")
        sys.exit(1)

    with open(whisper_json, encoding="utf-8") as f:
        whisper_result = json.load(f)

    subtitles = generate_subtitles(
        whisper_result,
        max_line_chars=args.max_line_chars,
        two_line_mode=args.two_line_mode,
        font_size=args.font_size,
    )

    print(f"\n=== Subtitle Generation Results ===")
    print(f"Total subtitles: {len(subtitles)}")

    # 統計
    total_chars = sum(sum(len(line) for line in sub["lines"]) for sub in subtitles)
    avg_chars = total_chars / len(subtitles) if subtitles else 0
    two_line_count = sum(1 for sub in subtitles if len(sub["lines"]) > 1)
    print(f"Total characters: {total_chars}")
    print(f"Average characters per subtitle: {avg_chars:.1f}")
    print(f"Two-line subtitles: {two_line_count}")

    # 保存
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_json}")


if __name__ == "__main__":
    main()
