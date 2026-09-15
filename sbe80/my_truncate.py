# Copyright (C) 2026 Bryan A. Jones.
#
# This file is part of the Literate Programming Book.
#
# The Literate Programming Book is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# The Literate Programming Book is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
# Public License for more details.
#
# You should have received a [copy](../../LICENSE.md) of the GNU General Public
# License along with the Literate Programming Book. If not, see
# [https://www.gnu.org/licenses/](https://www.gnu.org/licenses/).
#
# `my_truncate.py` - holds LLM-generated code for the
# [warmup\_truncate.py](warmup_truncate.py) test bench
# ====================================================
#
# Paste the LLM's answer here, replacing everything below.
#
# Do not edit its code, and do not ask it a follow-up question. The point of the
# warm-up is to see what one sentence bought you. The editor lints as you type,
# so expect underlines under the pasted code; those are style opinions, and
# fixing them is editing.
#
# Your function must be named `truncate`. If the LLM named it something else,
# add an alias at the bottom of the file:
#
# ```
#   truncate = shorten_string
# ```
#
# Code
# ----
#
# The follwoing code was generated using GPT 5.6 luna
#
# I want you to write a python function named truncate that takes an input
# string and truncates after 100 characters with an ellipsis. Ideally the
# function would truncate in a manner that makes sense grammatically. The
# following list shows more detailed specifications to facilitate this. 
#
# * no ellipsis in the middle of a word unless the word is very long
# * ignore leading or trailing whitespace
# * do not put an ellipsis after punctuation.
# * use the ellipsis character, not three periods
# * I want 'character' to refer to a grapheme
# * The ellipsis will also be the 101st character not the 100th character
# * Both the amount of characters before the elipsis and the length of a "long word" 
#   should be input arguments
#
# Afterwards review this spec and list potential problem areas, and solutions

import regex


def truncate(text: str, max_chars: int = 100, long_word: int = 20) -> str:
    """
    Truncate text to max_chars graphemes, adding '…' as the next grapheme.

    Parameters
    ----------
    text : str
        The input string.
    max_chars : int
        Number of graphemes allowed before the ellipsis.
    long_word : int
        A word at least this many graphemes long may be split.

    Returns
    -------
    str
        The truncated string, with '…' as the (max_chars + 1)th grapheme.
    """

    # Remove leading/trailing whitespace.
    text = text.strip()

    # Split into Unicode grapheme clusters.
    graphemes = regex.findall(r"\X", text)

    # No truncation necessary.
    if len(graphemes) <= max_chars:
        return text

    # Candidate cutoff.
    cutoff = max_chars

    # Don't leave trailing whitespace before the ellipsis.
    while cutoff > 0 and graphemes[cutoff - 1].isspace():
        cutoff -= 1

    # Find the beginning of the word containing the cutoff.
    word_start = cutoff
    while word_start > 0 and not graphemes[word_start - 1].isspace():
        word_start -= 1

    word_length = cutoff - word_start

    # If we're in a normal-length word, back up to the previous word.
    if word_length < long_word:
        cutoff = word_start

        # Remove whitespace immediately before the ellipsis.
        while cutoff > 0 and graphemes[cutoff - 1].isspace():
            cutoff -= 1

    # If the cutoff is immediately after punctuation, back up so that
    # punctuation remains attached to the preceding text rather than
    # having the ellipsis follow it.
    punctuation = set(".,!?;:")
    while cutoff > 0 and graphemes[cutoff - 1] in punctuation:
        cutoff -= 1

    # Remove trailing whitespace once more after any adjustment.
    while cutoff > 0 and graphemes[cutoff - 1].isspace():
        cutoff -= 1

    return "".join(graphemes[:cutoff]) + "…"