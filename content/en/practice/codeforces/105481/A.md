---
title: "CF 105481A - \u7231\u4e0a\u5b57\u5178"
description: "We are given a long piece of text that represents a story. The text contains words mixed with spaces and punctuation marks such as commas, periods, exclamation marks, and question marks."
date: "2026-06-23T18:19:34+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105481
codeforces_index: "A"
codeforces_contest_name: "2024 CCPC Liaoning Provincial Contest"
rating: 0
weight: 105481
solve_time_s: 54
verified: true
draft: false
---

[CF 105481A - \u7231\u4e0a\u5b57\u5178](https://codeforces.com/problemset/problem/105481/A)

**Rating:** -  
**Tags:** -  
**Solve time:** 54s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a long piece of text that represents a story. The text contains words mixed with spaces and punctuation marks such as commas, periods, exclamation marks, and question marks. Each word is a sequence of letters, and words may appear in different capitalizations, but we treat them in a case-insensitive way.

Alongside this text, we are given a small dictionary of words that the reader already knows. When the reader encounters a word in the story, if it is not in their known set, they will look it up once and then remember it permanently. However, the reader has a flawed perception of words: different morphological forms are considered different words. So “accept” and “accepted” are not the same, even though they share a root.

The task is to simulate reading the entire text from left to right and count how many distinct words are not in the initial known set. Each unknown word triggers exactly one dictionary lookup the first time it appears.

The text length can be up to 5 × 10^6 characters. This immediately rules out any solution that repeatedly scans or copies substrings in an inefficient way. We need a single linear pass over the text, extracting words on the fly and processing them incrementally. The dictionary size is at most 100 words, so membership checks are constant-time if we store them in a hash set.

A few edge cases matter in practice. Words must be normalized to lowercase because input words can have uppercase first letters. Punctuation appears immediately after words, so a naive split on spaces is insufficient if we do not strip punctuation carefully. Another subtle case is repeated unknown words: only the first occurrence should increase the answer.

## Approaches

A brute-force interpretation would be to split the entire text into tokens using spaces and punctuation, then for each token repeatedly check whether it appears in the known list. Since the known list is small, we could linearly scan it for every token. This would already be borderline but still feasible in isolation. The real issue is not the dictionary lookup, but the cost of repeatedly constructing substrings or scanning the text multiple times if done carelessly.

A worse brute-force approach would repeatedly scan the known list for each word using string comparisons, leading to O(total_words × n) behavior, but since n ≤ 100 this part is not the bottleneck. The true inefficiency arises if we try to split using regex or repeated string operations that allocate many intermediate objects on a 5 million character string.

The key observation is that we only need a single pass over the text. We can accumulate characters into a buffer while reading, and whenever we hit a non-letter boundary, we finalize the word, normalize it, and process it immediately. This avoids any extra passes or heavy parsing overhead.

We store known words in a hash set, and we also maintain another set for words we have already looked up during reading. Each word is processed in O(1) average time.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(T × n) or worse with heavy parsing | O(T) | Too slow / unsafe |
| Optimal | O(T) | O(T + n) | Accepted |

## Algorithm Walkthrough

We scan the text character by character and extract words incrementally.

1. Initialize an empty set `known` containing all given dictionary words.
2. Initialize an empty set `seen_unknown` to track words already counted as dictionary lookups.
3. Initialize an empty string buffer `current`.
4. Traverse each character in the text:

1. If the character is a letter, append its lowercase form to `current`.
2. Otherwise, if `current` is non-empty, process it as a completed word.
5. When processing a completed word:

1. If it is not in `known` and not in `seen_unknown`, increment the answer and insert it into `seen_unknown`.
2. Clear `current`.
6. After the loop ends, process any remaining word in `current` using the same logic.
7. Output the accumulated answer.

The reason we normalize on the fly is to avoid storing mixed-case variants, which would break equality checks. The reason we delay counting until word completion is to ensure punctuation does not interfere with word boundaries.

### Why it works

At any point in the scan, `current` represents exactly one contiguous sequence of letters from the text. Every word in the input is separated by a non-letter character, so every word is eventually finalized exactly once. Because we insert unknown words into `seen_unknown` immediately upon first encounter, subsequent occurrences do not affect the answer. The invariant is that `seen_unknown` always contains exactly those words that have been counted, and `known` contains all words that do not require counting at all.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    text = sys.stdin.readline().rstrip("\n")
    n = int(sys.stdin.readline())
    known_words = sys.stdin.readline().split()

    known = set(known_words)
    seen_unknown = set()

    ans = 0
    current = []

    def process(word):
        nonlocal ans
        if not word:
            return
        if word not in known and word not in seen_unknown:
            seen_unknown.add(word)
            ans += 1

    for ch in text:
        if ch.isalpha():
            current.append(ch.lower())
        else:
            if current:
                process("".join(current))
                current.clear()

    if current:
        process("".join(current))

    print(ans)

if __name__ == "__main__":
    solve()
```

The main performance consideration is avoiding repeated string concatenation inside the loop. We accumulate characters in a list and only join when a word boundary is reached. This keeps the complexity linear in the total number of characters.

We also explicitly lowercase every character during accumulation, which avoids a second pass over the word later.

## Worked Examples

Consider the sample-like input:

```
I love Liaoning. Love Dalian!
1
love
```

We process the text sequentially.

| Step | Current Char Stream | Completed Word | Known? | Seen Unknown | Answer |
| --- | --- | --- | --- | --- | --- |
| 1 | "i" | I | no | {i} | 1 |
| 2 | "love" | love | yes | {} | 1 |
| 3 | "liaoning" | Liaoning | no | {liaoning} | 2 |
| 4 | "love" | Love | yes | {} | 2 |
| 5 | "dalian" | Dalian | no | {liaoning, dalian} | 3 |

This trace shows that repeated occurrences of known words do not affect the answer, while unknown words are counted only once.

Now consider a case with repetition and punctuation:

```
Hello hello! HELLO?
0
```

| Step | Current Char Stream | Completed Word | Seen Unknown | Answer |
| --- | --- | --- | --- | --- |
| 1 | "hello" | hello | {hello} | 1 |
| 2 | "hello" | hello | {hello} | 1 |
| 3 | "hello" | hello | {hello} | 1 |

This confirms case normalization and duplicate suppression.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(T) | Each character is processed once, and each word is inserted/checked in hash sets in O(1) average time |
| Space | O(T + n) | Worst case stores all characters of current word processing plus dictionary sets |

The constraints allow up to 5 million characters, so a linear scan with constant-time operations per character is sufficient within limits. Memory usage remains safe since only sets of words and a small buffer are stored.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve
    return solve()

# Note: assume solve() prints output, adjust if needed

# Sample-style case
# assert run("I love Liaoning. Love Dalian!\n1\nlove\n") == "3\n"

# Minimum input
assert run("A\n0\n") == "1\n", "single word unknown"

# All known words
assert run("Hello world\n2\nhello world\n") == "0\n", "all known"

# Repeated unknown words
assert run("test test test\n0\n") == "1\n", "only first occurrence counts"

# Case normalization
assert run("Hi HI hI\n0\n") == "1\n", "case insensitive"

# Punctuation boundary
assert run("a,b.c!d?\n0\n") == "4\n", "all split correctly"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single word | 1 | minimal unknown handling |
| All known | 0 | dictionary filtering |
| Repeated unknown | 1 | deduplication |
| Mixed case | 1 | normalization |
| Punctuation-heavy | 4 | correct tokenization |

## Edge Cases

One edge case is when the text ends with a letter sequence without punctuation. In that case, without explicit handling, the final word would never be processed. The solution fixes this by running `process(current)` after the loop ends.

Input:

```
hello world
0
```

During traversal, “hello” and “world” are processed at the space boundary, and no words remain in the buffer at the end. The final flush does nothing, confirming correctness.

Another edge case is multiple consecutive punctuation characters or spaces. Since processing only triggers on transitions from letters to non-letters, repeated delimiters do not create empty words.

Input:

```
a,,!!b??
0
```

The algorithm extracts “a” and “b” as two separate words, and both are counted exactly once.
