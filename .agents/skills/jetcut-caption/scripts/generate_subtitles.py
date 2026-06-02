#!/usr/bin/env python3
"""
Whisperの出力からテロップ用の字幕JSONを生成するスクリプト。
BudouXを使用して日本語の自然な文節で分割する。

Usage:
    python generate_subtitles.py <whisper_json> <output_json>

Example:
    python generate_subtitles.py temp/whisper_result.json temp/subtitles.json
"""

import json
import sys
from pathlib import Path

import budoux


def get_font_size(max_line_length: int) -> int:
    """最長行の文字数に応じたフォントサイズを返す。"""
    if max_line_length <= 8:
        return 72
    elif max_line_length <= 12:
        return 64
    elif max_line_length <= 18:
        return 56
    elif max_line_length <= 24:
        return 48
    else:
        return 42


def split_into_two_lines(text: str, parser: budoux.Parser) -> list[str]:
    """
    テキストをBudouXで文節分割し、均等な2行に分割する。
    """
    chunks = parser.parse(text)

    if len(chunks) <= 1:
        return [text]

    # 最も均等に分割できる位置を探す
    total_len = len(text)
    target_len = total_len / 2

    best_split = 1
    best_diff = float("inf")
    current_len = 0

    for i, chunk in enumerate(chunks[:-1]):
        current_len += len(chunk)
        diff = abs(current_len - target_len)
        if diff < best_diff:
            best_diff = diff
            best_split = i + 1

    line1 = "".join(chunks[:best_split])
    line2 = "".join(chunks[best_split:])

    return [line1, line2]


def split_long_segment(
    text: str, start: float, end: float, parser: budoux.Parser, max_chars: int = 30
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


def generate_subtitles(whisper_result: dict) -> list[dict]:
    """
    Whisperの出力から字幕JSONを生成する。
    """
    parser = budoux.load_default_japanese_parser()
    subtitles = []
    subtitle_id = 0

    for segment in whisper_result.get("segments", []):
        text = segment.get("text", "").strip()
        start = segment.get("start", 0)
        end = segment.get("end", 0)

        if not text:
            continue

        # 長いセグメントを分割
        split_segments = split_long_segment(text, start, end, parser)

        for split_seg in split_segments:
            seg_text = split_seg["text"]
            seg_start = split_seg["start"]
            seg_end = split_seg["end"]

            # 行分割
            if len(seg_text) <= 18:
                lines = [seg_text]
            else:
                lines = split_into_two_lines(seg_text, parser)

            # フォントサイズを決定
            max_line_len = max(len(line) for line in lines)
            font_size = get_font_size(max_line_len)

            # 最終チェック: 各行が30文字以下であることを確認
            final_lines = []
            for line in lines:
                if len(line) > 30:
                    # 再分割が必要
                    sub_lines = split_into_two_lines(line, parser)
                    final_lines.extend(sub_lines)
                else:
                    final_lines.append(line)

            # 2行を超える場合はさらに分割が必要
            if len(final_lines) > 2:
                # 2行ずつに分けて複数の字幕に
                for i in range(0, len(final_lines), 2):
                    sub_lines = final_lines[i : i + 2]
                    sub_duration = (seg_end - seg_start) / ((len(final_lines) + 1) // 2)
                    sub_start = seg_start + (i // 2) * sub_duration
                    sub_end = sub_start + sub_duration

                    max_len = max(len(l) for l in sub_lines)
                    subtitles.append(
                        {
                            "id": subtitle_id,
                            "start": round(sub_start, 3),
                            "end": round(sub_end, 3),
                            "lines": sub_lines,
                            "fontSize": get_font_size(max_len),
                        }
                    )
                    subtitle_id += 1
            else:
                subtitles.append(
                    {
                        "id": subtitle_id,
                        "start": round(seg_start, 3),
                        "end": round(seg_end, 3),
                        "lines": final_lines,
                        "fontSize": font_size,
                    }
                )
                subtitle_id += 1

    return subtitles


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <whisper_json> <output_json>")
        sys.exit(1)

    whisper_json = sys.argv[1]
    output_json = sys.argv[2]

    if not Path(whisper_json).exists():
        print(f"Error: Input file not found: {whisper_json}")
        sys.exit(1)

    with open(whisper_json, encoding="utf-8") as f:
        whisper_result = json.load(f)

    subtitles = generate_subtitles(whisper_result)

    print(f"\n=== Subtitle Generation Results ===")
    print(f"Total subtitles: {len(subtitles)}")

    # 統計
    total_chars = sum(sum(len(line) for line in sub["lines"]) for sub in subtitles)
    avg_chars = total_chars / len(subtitles) if subtitles else 0
    print(f"Total characters: {total_chars}")
    print(f"Average characters per subtitle: {avg_chars:.1f}")

    # 保存
    Path(output_json).parent.mkdir(parents=True, exist_ok=True)
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(subtitles, f, ensure_ascii=False, indent=2)

    print(f"Saved to: {output_json}")


if __name__ == "__main__":
    main()
