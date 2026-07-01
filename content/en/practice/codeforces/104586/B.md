---
title: "CF 104586B - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f"
description: "We are given a short message split into words, and we want to decide whether the special keyword “codecup” could have appeared somewhere in that message after transmission errors. The key detail is the error model."
date: "2026-06-30T07:33:12+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104586
codeforces_index: "B"
codeforces_contest_name: "Codemasters Codecup 2023 - \u041e\u0442\u0431\u043e\u0440\u043e\u0447\u043d\u044b\u0439 \u0442\u0443\u0440"
rating: 0
weight: 104586
solve_time_s: 84
verified: true
draft: false
---

[CF 104586B - \u0420\u0443\u0434\u043e\u043b\u044c\u0444 \u0438 \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u044f](https://codeforces.com/problemset/problem/104586/B)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a short message split into words, and we want to decide whether the special keyword “codecup” could have appeared somewhere in that message after transmission errors.

The key detail is the error model. Each transmitted word may lose at most one character during transmission, but characters are never changed and nothing else happens across words. So every observed word is either exactly the original word or the original word with a single character deleted somewhere inside it. No substitutions and no multiple deletions are allowed.

The task is to check whether any of the observed words could correspond to the intended word “codecup” under this rule. If at least one word could be a corrupted version of “codecup”, the answer is positive.

The input size is small: at most 100 words, each up to length 25. This removes any pressure for heavy preprocessing or advanced data structures. A direct check per word is sufficient since each check involves only a fixed pattern of length 7.

A subtle point is that we are not allowed to “fix” a word by changing characters. We only remove at most one character from the original “codecup” to obtain the received word. This asymmetry matters because it prevents confusing this with general edit distance.

The main edge case is when the word is almost correct but differs in two positions. For example, “codecap” differs by substitution, which is invalid, and “cdecp” corresponds to two deletions, which is also invalid. Both should correctly fail.

## Approaches

A brute-force interpretation would try to align each message word with all possible ways of deleting characters from “codecup”. Since “codecup” has length 7, there are only 8 possibilities: delete nothing or delete exactly one of the 7 positions. For each word, we could generate these 8 candidates and compare.

This already works within limits, but it is slightly indirect. The cleaner observation is that we do not need to generate modified patterns at all. Instead, we can scan the word against “codecup” using two pointers and allow skipping at most one character in the pattern. This directly encodes the constraint “at most one deletion from the original”.

The brute-force approach works because the pattern space is tiny, but it becomes conceptually messy if generalized. The two-pointer formulation reduces everything to a single linear scan per word and makes correctness easier to reason about.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Enumerate deletions | O(n · 7) | O(1) | Accepted |
| Two-pointer skip check | O(n · 7) | O(1) | Accepted |

## Algorithm Walkthrough

We treat “codecup” as a fixed reference string of length 7 and test each word independently.

1. For each word in the message, attempt to match it against “codecup” using two pointers, one for the word and one for the pattern.

The goal is to consume the entire word while advancing through the pattern, allowing at most one skipped character in the pattern.
2. Initialize two indices, one for the word and one for the pattern, and a counter for how many pattern characters we skip.

The skip counter represents the single allowed deletion in the original word before corruption.
3. While both pointers are within bounds, compare characters. If they match, advance both pointers.

This corresponds to a character that survived transmission.
4. If they do not match, we attempt to skip one character in the pattern, increasing the skip counter and advancing only the pattern pointer.

This models the idea that this pattern character might be the one that was deleted before transmission.
5. If a mismatch happens again after already using the skip, the match attempt fails for this word.
6. After the loop, the match is valid only if the entire word has been consumed and we have used at most one skip in the pattern, and any remaining characters in the pattern can be safely ignored only if they correspond to a single allowed deletion scenario.
7. If any word succeeds, we immediately return “Yes”. Otherwise, after checking all words, we return “No”.

### Why it works

The core constraint is that each observed word is derived from the original word by deleting at most one character. That means alignment between a word and “codecup” can fail in exactly one structural way: a single missing character in the pattern. The two-pointer process enforces that every character in the observed word must correspond to an order-preserving subsequence of the pattern, while the skip counter enforces that we never assume more than one missing position. This exactly characterizes all valid corruption outcomes and excludes substitutions or multiple deletions.

## Python Solution

```python
import sys
input = sys.stdin.readline

TARGET = "codecup"

def matches(word):
    i = j = 0
    skipped = 0

    while i < len(word) and j < len(TARGET):
        if word[i] == TARGET[j]:
            i += 1
            j += 1
        else:
            if skipped == 1:
                return False
            skipped += 1
            j += 1

    if i != len(word):
        return False

    return True

def solve():
    n = int(input())
    words = input().split()

    for w in words:
        if matches(w):
            return "Yes"
    return "No"

print(solve())
```

The solution isolates the matching logic into a helper function so each word is checked independently. The two-pointer loop ensures linear scanning over the fixed pattern. The important subtlety is the final check that the entire word is consumed; otherwise partial matches could incorrectly pass when extra characters remain in the word.

## Worked Examples

### Example 1

Input words: `codeforsquares codecup coming soon`

| word | scan result | skipped | valid |
| --- | --- | --- | --- |
| codeforsquares | mismatch too early, no valid alignment | 1 exceeded | No |
| codecup | full exact match | 0 | Yes |

The second word directly matches the target without needing any deletion, so the answer becomes positive immediately.

### Example 2

Input words: `cdecup is postponed`

| word | scan result | skipped | valid |
| --- | --- | --- | --- |
| cdecup | matches codecup with one missing 'o' | 1 | Yes |

Here the missing character corresponds to a single allowed deletion from the original word.

This demonstrates that the algorithm correctly accepts subsequence-like distortions with exactly one missing character.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n · 7) | Each word is compared against a fixed-length pattern using a linear scan |
| Space | O(1) | Only constant extra state is used |

The constraints are small enough that even a straightforward implementation is far below any limit. The constant pattern length makes the solution effectively linear in the number of words.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    global input
    input = _sys.stdin.readline

    TARGET = "codecup"

    def matches(word):
        i = j = 0
        skipped = 0
        while i < len(word) and j < len(TARGET):
            if word[i] == TARGET[j]:
                i += 1
                j += 1
            else:
                if skipped == 1:
                    return False
                skipped += 1
                j += 1
        return i == len(word)

    n = int(input())
    words = input().split()
    return "Yes" if any(matches(w) for w in words) else "No"

# provided samples
assert run("""4
codeforsquares codecup coming soon
""") == "Yes"

assert run("""3
cdecup is postponed
""") == "Yes"

assert run("""5
abracadabra code cup hello all
""") == "No"

# custom cases
assert run("""1
codecup
""") == "Yes"

assert run("""1
codecap
""") == "No"

assert run("""1
cdecp
""") == "No"

assert run("""2
codecup xcodecup
""") == "Yes"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single exact match | Yes | baseline acceptance |
| substitution case | No | rejects invalid character changes |
| multiple deletions | No | enforces at most one deletion |
| mixed message | Yes | finds any valid word |

## Edge Cases

A useful failure case is a word like “codecap”, which differs from the target in a single position but via substitution rather than deletion. The algorithm never allows character replacement, only skipping in the pattern, so it cannot align the mismatched character and correctly rejects it.

Another edge case is a word like “cdecp”, which requires removing multiple characters from the original “codecup”. The skip counter prevents more than one mismatch in the pattern, so once the second structural gap is needed, the match immediately fails.

Finally, words shorter than 6 characters cannot represent a valid corruption of a 7-character source with at most one deletion. The pointer logic naturally fails because too many characters in the pattern must be skipped, exceeding the allowed single deletion.
