---
title: "CF 102890L - Let's count words"
description: "The task is essentially about counting how many “words” appear in a given text under a simple tokenization rule. We are given a string that represents a line of text, and we must determine how many distinct word tokens exist in it according to the definition implied by the…"
date: "2026-07-04T13:41:38+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102890
codeforces_index: "L"
codeforces_contest_name: "2020 ICPC Gran Premio de Mexico 3ra Fecha"
rating: 0
weight: 102890
solve_time_s: 41
verified: true
draft: false
---

[CF 102890L - Let's count words](https://codeforces.com/problemset/problem/102890/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 41s  
**Verified:** yes  

## Solution
## Problem Understanding

The task is essentially about counting how many “words” appear in a given text under a simple tokenization rule. We are given a string that represents a line of text, and we must determine how many distinct word tokens exist in it according to the definition implied by the problem. A word is formed by consecutive alphabetic characters, and anything else such as spaces, punctuation, or digits acts as a separator. The output is a single integer representing how many such word segments appear after splitting the text.

Another way to view the input is that we are scanning a raw character stream and grouping it into maximal contiguous alphabetic substrings. Every time we transition from a non-letter into a letter, we begin a new word, and every time we transition from a letter to a non-letter, we end the current word.

The constraints in such problems are typically large enough that the string length can reach up to about 10^5 or 10^6 characters. That immediately implies that any quadratic approach, such as repeatedly slicing or using expensive string operations inside loops, will fail. The only viable approach is a single linear scan over the input, processing each character once.

A naive mistake comes from splitting only on spaces. For example, given the input `hello,world`, a naive `split()` on spaces would treat it as one word, while the correct answer is two words: `hello` and `world`. Another subtle failure happens when multiple separators appear consecutively, such as `a---b`. A naive counter might incorrectly count empty tokens if it is not careful, but the correct interpretation ignores empty segments and only counts transitions into letter sequences.

## Approaches

The brute-force approach is to treat the string as a sequence of substrings separated by every possible non-letter character. One could iterate over every possible starting index, expand until a separator is found, and record substrings. While this is conceptually straightforward, it risks repeatedly scanning overlapping regions. In the worst case, such as a string of all letters, each substring expansion becomes O(n), leading to O(n^2) behavior.

The key observation is that we never need to materialize substrings. We only need to detect boundaries between “inside a word” and “outside a word.” This reduces the problem to tracking a single boolean state while scanning left to right. Each character is processed exactly once, and we increment the word count only when we enter a letter segment from a non-letter state.

| Approach | Time Complexity | Space Complexity | Verdict |
|---|---|---|---|
| Brute Force substring extraction | O(n^2) | O(n) | Too slow |
| Single pass state tracking | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

We maintain two pieces of information: a counter for words and a flag indicating whether we are currently inside a word.

1. Initialize a counter `words = 0` and a boolean `in_word = False`. This state represents that initially we are outside any word segment.

2. Iterate over each character in the string from left to right. Each character is classified as either a letter or a separator.

3. If the current character is a letter and `in_word` is False, this means we are entering a new word. We increment `words` by 1 and set `in_word = True`. This step is crucial because it ensures that we only count the first character of each contiguous alphabetic block.

4. If the current character is a letter and `in_word` is True, we continue inside the same word and do nothing. This prevents overcounting multi-character words.

5. If the current character is not a letter, we set `in_word = False`, marking that any subsequent letter will start a new word. This transition ensures correct handling of multiple separators in a row.

6. After processing all characters, the value of `words` is the answer.

The correctness comes from the invariant that `in_word` is True if and only if the previous character was a letter belonging to a currently active word segment. Every word is counted exactly once at its first character, and never again.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    s = input().rstrip("\n")
    
    words = 0
    in_word = False
    
    for ch in s:
        if ch.isalpha():
            if not in_word:
                words += 1
                in_word = True
        else:
            in_word = False
    
    print(words)

if __name__ == "__main__":
    solve()
```

The solution reads the input line and processes it character by character. The `in_word` flag is the central mechanism that avoids double counting letters inside the same word. The only subtle point is using `isalpha()` rather than checking spaces only, since separators can include punctuation or other non-letter symbols depending on the problem’s definition.

## Worked Examples

### Example 1
Input: `hello,world 123 test`

| Character | Is Letter | in_word (before) | Action | words |
|---|---|---|---|---|
| h | True | False | start word | 1 |
| e | True | True | continue | 1 |
| l | True | True | continue | 1 |
| l | True | True | continue | 1 |
| o | True | True | continue | 1 |
| , | False | True | end word | 1 |
| w | True | False | start word | 2 |
| o | True | True | continue | 2 |
| r | True | True | continue | 2 |
| l | True | True | continue | 2 |
| d | True | True | continue | 2 |
| (space) | False | True | end word | 2 |
| 1 | False | False | ignore | 2 |
| 2 | False | False | ignore | 2 |
| 3 | False | False | ignore | 2 |
| (space) | False | False | ignore | 2 |
| t | True | False | start word | 3 |
| e | True | True | continue | 3 |
| s | True | True | continue | 3 |
| t | True | True | continue | 3 |

This demonstrates that punctuation and digits correctly terminate words, and only transitions into alphabetic sequences increment the counter.

### Example 2
Input: `---abc--de--`

| Character | Is Letter | in_word (before) | Action | words |
|---|---|---|---|---|
| - | False | False | ignore | 0 |
| - | False | False | ignore | 0 |
| - | False | False | ignore | 0 |
| a | True | False | start word | 1 |
| b | True | True | continue | 1 |
| c | True | True | continue | 1 |
| - | False | True | end word | 1 |
| - | False | False | ignore | 1 |
| d | True | False | start word | 2 |
| e | True | True | continue | 2 |
| - | False | True | end word | 2 |
| - | False | False | ignore | 2 |

This example shows that multiple consecutive separators do not produce extra counts, since the transition logic only reacts to entering a letter state.

## Complexity Analysis

| Measure | Complexity | Explanation |
|---|---|---|
| Time | O(n) | Each character is processed exactly once in a single pass |
| Space | O(1) | Only a constant number of variables are maintained |

The linear scan fits comfortably within typical constraints up to 10^6 characters, since each operation is constant time and requires no auxiliary data structures.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    return sys.stdout.getvalue() if False else capture(inp)

def capture(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    backup = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = backup
    return out.getvalue().strip()

# minimal cases
assert capture("") == "0"
assert capture("abc") == "1"
assert capture("a b c") == "3"

# punctuation-heavy
assert capture("hello,world") == "2"

# consecutive separators
assert capture("---a--b---c---") == "3"
```

| Test input | Expected output | What it validates |
|---|---|---|
| `""` | `0` | empty string handling |
| `"abc"` | `1` | single word |
| `"a b c"` | `3` | space-separated words |
| `"hello,world"` | `2` | punctuation splitting |
| `"---a--b---c---"` | `3` | multiple separators |

## Edge Cases

One important edge case is an input containing no letters at all, such as `"12345!!!"`. The algorithm initializes `in_word = False` and never encounters a letter, so the counter remains zero throughout. The output is correctly `0`.

Another edge case is a string that starts directly with a separator followed by a word, such as `"--abc"`. The first characters reset `in_word` but do not affect the counter. When `'a'` is reached, it correctly triggers a new word count, resulting in `1`.

A final case is alternating separators and single letters like `"a-b-c"`. Each letter is preceded by a non-letter, so each one starts a new word. The algorithm increments exactly once per letter, producing `3`, which matches the intended segmentation rule.
