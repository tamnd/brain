---
title: "CF 71A - Way Too Long Words"
description: "We are given several lowercase English words. For each word, we must decide whether it is “too long”. A word is considered too long if its length is greater than 10. Short words stay unchanged. Long words are compressed into a shorter form built from three pieces: 1."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 800
weight: 71
solve_time_s: 89
verified: true
draft: false
---

[CF 71A - Way Too Long Words](https://codeforces.com/problemset/problem/71/A)

**Rating:** 800  
**Tags:** strings  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several lowercase English words. For each word, we must decide whether it is “too long”. A word is considered too long if its length is greater than 10.

Short words stay unchanged. Long words are compressed into a shorter form built from three pieces:

1. The first character.
2. The number of characters between the first and last character.
3. The last character.

For example, `"localization"` has 12 characters. The first letter is `'l'`, the last letter is `'n'`, and there are 10 characters between them, so the result becomes `"l10n"`.

The input begins with an integer `n`, followed by `n` words. We process each word independently and print the transformed version.

The constraints are extremely small. There are at most 100 words, and each word has length at most 100. Even a simple character-by-character solution runs comfortably within the limits. A solution with linear complexity in the total input size is more than enough.

The tricky part is not performance, it is handling boundary conditions correctly.

One easy mistake is using `>= 10` instead of `> 10`. Words of exactly length 10 must remain unchanged.

Consider this input:

```
1
abcdefghij
```

The correct output is:

```
abcdefghij
```

A careless implementation might produce `"a8j"` because it abbreviates words with length at least 10 instead of strictly greater than 10.

Another common mistake is computing the middle count incorrectly. The number written in the abbreviation is not the total length, it is the number of characters strictly between the first and last.

For example:

```
1
localization
```

The word length is 12. The correct abbreviation is:

```
l10n
```

Using `len(word) - 1` instead of `len(word) - 2` would incorrectly produce `"l11n"`.

A third subtle issue is indexing the last character. Python allows negative indexing, but using the wrong position can silently produce incorrect output.

Example:

```
1
abcdefghijk
```

Correct output:

```
a9k
```

If someone accidentally uses `word[len(word) - 2]`, the output becomes `"a9j"`.

## Approaches

The most direct approach is to process every word separately and explicitly build its abbreviation when needed.

For each word, we first check its length. If the length is at most 10, we print the original word. Otherwise, we take the first character, compute how many characters lie in the middle, append the last character, and print the result.

This already solves the problem efficiently because the input is tiny. If there are at most 100 words and each has length at most 100, then even scanning every character multiple times costs only around 10,000 operations.

A more “brute-force” interpretation would be constructing the middle portion explicitly and counting it manually. For example, for `"localization"` we could slice `"ocalizatio"` and count its characters one by one before forming the abbreviation. This works correctly but performs unnecessary work.

The key observation is that the middle count is always:

```
length - 2
```

We never need to inspect the middle characters themselves. Only the first and last characters matter. Once we realize this, the solution becomes a constant amount of work per word aside from reading the input.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(total characters) | O(word length) | Accepted |
| Optimal | O(total characters) | O(1) extra | Accepted |

Even though both versions have the same asymptotic complexity under these constraints, the optimal version is cleaner and avoids unnecessary temporary work.

## Algorithm Walkthrough

1. Read the integer `n`, the number of words to process.
2. Repeat `n` times and read one word each iteration.
3. Check the length of the current word.
4. If the length is less than or equal to 10, print the word unchanged.

Words of length exactly 10 are not abbreviated, so the condition must be `<= 10`.
5. Otherwise, build the abbreviation:

- Take the first character with `word[0]`.
- Compute the number of middle characters as `len(word) - 2`.
- Take the last character with `word[-1]`.
6. Concatenate these three parts and print the result.

### Why it works

For every long word, the required abbreviation format is uniquely defined by the problem: first letter, count of internal letters, last letter.

If a word has length `L`, then removing the first and last characters leaves exactly `L - 2` middle characters. The algorithm computes exactly this value and preserves the required boundary characters, so every produced abbreviation matches the specification.

For short words, the algorithm prints the original word unchanged, which is also exactly what the problem asks for.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())

for _ in range(n):
    word = input().strip()

    if len(word) <= 10:
        print(word)
    else:
        print(word[0] + str(len(word) - 2) + word[-1])
```

The program starts by reading the number of words.

For each word, `strip()` removes the trailing newline character from the input. Without this step, the newline would incorrectly affect the length calculation.

The condition `len(word) <= 10` handles the boundary correctly. Only words with strictly greater length are abbreviated.

The abbreviation construction is compact but important to understand carefully:

```
word[0]
```

extracts the first character.

```
len(word) - 2
```

counts how many characters remain after excluding the first and last positions.

```
word[-1]
```

extracts the final character safely using Python’s negative indexing.

The count must be converted to a string before concatenation:

```
str(len(word) - 2)
```

Otherwise Python would raise a type error when combining strings and integers.

## Worked Examples

### Example 1

Input:

```
4
word
localization
internationalization
pneumonoultramicroscopicsilicovolcanoconiosis
```

Trace:

| Word | Length | Too Long? | Abbreviation | Output |
| --- | --- | --- | --- | --- |
| word | 4 | No | - | word |
| localization | 12 | Yes | l10n | l10n |
| internationalization | 20 | Yes | i18n | i18n |
| pneumonoultramicroscopicsilicovolcanoconiosis | 45 | Yes | p43s | p43s |

This example shows both branches of the algorithm. Short words pass through unchanged, while long words are compressed using the exact middle-character count.

### Example 2

Input:

```
3
abcdefghij
abcdefghijk
hi
```

Trace:

| Word | Length | Too Long? | Abbreviation | Output |
| --- | --- | --- | --- | --- |
| abcdefghij | 10 | No | - | abcdefghij |
| abcdefghijk | 11 | Yes | a9k | a9k |
| hi | 2 | No | - | hi |

This trace focuses on the boundary at length 10. The first word must remain unchanged, while the second word, with length 11, is abbreviated.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total characters) | Each word is read once and processed in constant additional work |
| Space | O(1) extra | Only a few variables are used |

The total input size is tiny, at most 10,000 characters. A linear scan over the input easily fits within the 1 second time limit and the 256 MB memory limit.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def solve():
    input = sys.stdin.readline

    n = int(input())
    out = []

    for _ in range(n):
        word = input().strip()

        if len(word) <= 10:
            out.append(word)
        else:
            out.append(word[0] + str(len(word) - 2) + word[-1])

    print("\n".join(out))

def run(inp: str) -> str:
    backup_stdin = sys.stdin
    backup_stdout = sys.stdout

    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    output = sys.stdout.getvalue()

    sys.stdin = backup_stdin
    sys.stdout = backup_stdout

    return output

# provided sample
assert run(
"""4
word
localization
internationalization
pneumonoultramicroscopicsilicovolcanoconiosis
"""
) == (
"""word
l10n
i18n
p43s
"""
), "sample 1"

# minimum size input
assert run(
"""1
a
"""
) == (
"""a
"""
), "single character word"

# boundary length exactly 10
assert run(
"""1
abcdefghij
"""
) == (
"""abcdefghij
"""
), "length 10 should not abbreviate"

# boundary length 11
assert run(
"""1
abcdefghijk
"""
) == (
"""a9k
"""
), "length 11 should abbreviate"

# multiple identical long words
assert run(
"""3
localization
localization
localization
"""
) == (
"""l10n
l10n
l10n
"""
), "repeated words"

print("All tests passed!")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum possible word length |
| `abcdefghij` | `abcdefghij` | Length exactly 10 stays unchanged |
| `abcdefghijk` | `a9k` | First abbreviation boundary |
| Three copies of `localization` | Three copies of `l10n` | Repeated processing consistency |

## Edge Cases

A word with exactly 10 characters is the most important boundary case.

Input:

```
1
abcdefghij
```

The algorithm computes `len(word) == 10`. Since the condition is `<= 10`, it prints the word unchanged:

```
abcdefghij
```

This avoids the common mistake of abbreviating length-10 words.

Another subtle case is verifying the middle count.

Input:

```
1
localization
```

The length is 12. The algorithm computes:

```
12 - 2 = 10
```

Then it combines:

```
'l' + '10' + 'n'
```

which produces:

```
l10n
```

This confirms the algorithm counts only the characters strictly between the endpoints.

A final edge case checks correct last-character access.

Input:

```
1
abcdefghijk
```

The algorithm uses:

```
word[-1]
```

which correctly selects `'k'`. The result becomes:

```
a9k
```

Using the wrong index would silently produce the wrong abbreviation, so this confirms the indexing logic is correct.
