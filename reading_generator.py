"""Simple reading passage generator that injects target words into sentences."""
from __future__ import annotations

import random
import textwrap
from typing import Iterable, List


TEMPLATES = [
    "The {word} appeared repeatedly in today's study session.",
    "To remember {word}, the student wove it into a personal story.",
    "Practice shows that using {word} in context improves retention.",
    "During the mock exam, {word} helped unlock the meaning of a passage.",
    "After reviewing {word}, a quick summary was written to reinforce it.",
    "The mentor asked for an example sentence that included {word}.",
    "A short dialogue was crafted so that {word} sounded natural.",
    "Connecting {word} with related concepts created a semantic map.",
    "A highlight in the reading was the precise use of {word}.",
    "Repeating {word} aloud strengthened pronunciation and recall.",
]


def generate_reading(words: Iterable[str], sentences: int = 5, width: int = 88) -> str:
    """Generate a paragraph that reuses the provided words.

    The generator rotates through the given words and randomly picks sentence templates
    to keep the output varied but stable enough for memorization practice.
    """

    word_list: List[str] = [w.strip() for w in words if w.strip()]
    if not word_list:
        return ""

    random.shuffle(word_list)
    chosen_templates = random.sample(TEMPLATES, k=min(sentences, len(TEMPLATES)))

    sentences_out: List[str] = []
    for idx in range(sentences):
        word = word_list[idx % len(word_list)]
        template = chosen_templates[idx % len(chosen_templates)]
        sentences_out.append(template.format(word=word))

    paragraph = " ".join(sentences_out)
    return textwrap.fill(paragraph, width=width)


__all__ = ["generate_reading"]
