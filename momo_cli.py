"""Command-line helper to generate reading material from MoMo words and translate it."""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from momo_api import MoMoClient
from reading_generator import generate_reading
from translator import TranslateDirection, translate_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate reading from MoMo daily words.")
    parser.add_argument(
        "--date", help="Date to fetch words for (YYYY-MM-DD). Defaults to today's words via API.",
    )
    parser.add_argument(
        "--words",
        help="Comma-separated word list to use instead of fetching from the API.",
    )
    parser.add_argument(
        "--sentences",
        type=int,
        default=6,
        help="Number of sentences to include in the generated passage.",
    )
    parser.add_argument(
        "--direction",
        choices=["en2zh", "zh2en"],
        default="en2zh",
        help="Translation direction for the generated passage.",
    )
    parser.add_argument(
        "--base-url",
        help="Override the MoMo API base URL (defaults to env MOMO_API_BASE or https://api.maimemo.com).",
    )
    parser.add_argument(
        "--token",
        help="MoMo API token (defaults to env MOMO_API_TOKEN).",
    )
    parser.add_argument(
        "--daily-endpoint",
        help="Endpoint path for today's words (defaults to env MOMO_DAILY_ENDPOINT).",
    )
    parser.add_argument(
        "--translate-url",
        help="LibreTranslate-compatible URL (defaults to env LIBRE_TRANSLATE_URL).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path to save the generated reading and translation.",
    )
    return parser.parse_args()


def load_words(args: argparse.Namespace) -> List[str]:
    if args.words:
        return [w.strip() for w in args.words.split(",") if w.strip()]

    client = MoMoClient(token=args.token, base_url=args.base_url, daily_endpoint=args.daily_endpoint)
    if args.date:
        return client.fetch_words_for_date(args.date)
    return client.fetch_today_words()


def main() -> None:
    args = parse_args()
    words = load_words(args)

    if not words:
        raise SystemExit("No words retrieved. Provide --words or check your MoMo API settings.")

    passage = generate_reading(words, sentences=args.sentences)
    translated = translate_text(passage, direction=args.direction, url=args.translate_url)

    output_lines = [
        "=== Words ===",
        ", ".join(words),
        "\n=== Generated Reading ===",
        passage,
        "\n=== Translation ===",
        translated,
    ]

    output = "\n".join(output_lines)
    print(output)

    if args.output:
        args.output.write_text(output, encoding="utf-8")
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()
