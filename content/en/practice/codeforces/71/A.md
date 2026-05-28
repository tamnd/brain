---
title: "CF 71A - Way Too Long Words"
description: "We are given several lowercase words and must shorten only the ones that are considered \"too long\". A word is too long if its length is greater than 10. The shortening rule is very specific."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 71
codeforces_index: "A"
codeforces_contest_name: "Codeforces Beta Round 65 (Div. 2)"
rating: 800
weight: 71
solve_time_s: 88
verified: true
draft: false
---

[CF 71A - Way Too Long Words](https://codeforces.com/problemset/problem/71/A)

**Rating:** 800  
**Tags:** strings  
**Solve time:** 1m 28s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several lowercase words and must shorten only the ones that are considered "too long". A word is too long if its length is greater than 10.

The shortening rule is very specific. We keep the first character and the last character, then replace everything in between with the count of removed characters. For example, `"localization"` has 12 characters, so we keep `'l'` and `'n'`, and there are 10 characters between them. The result becomes `"l10n"`.

Each input word is processed independently. For every word, we either print it unchanged or print its abbreviation.

The constraints are very small. There are at most 100 words, and each word has length at most 100. Even a straightforward character-by-character solution easily fits within the limits. The total amount of text processed is tiny, so any linear-time approach is more than enough.

The tricky part is not performance, it is handling the boundary conditions correctly.

One common mistake is abbreviating words whose length is exactly 10. The condition says strictly more than 10.

Example input:

```
1
abcdefghij
```

Correct output:

```
abcdefghij
```

A careless implementation using `>= 10` would incorrectly produce:

```
a8j
```

Another mistake is computing the middle count incorrectly. The number inserted is the count of characters between the first and last characters, which is `len(word) - 2`.

Example input:

```
1
localization
```

Correct output:

```
l10n
```

If someone uses `len(word) - 1`, they would incorrectly print:

```
l11n
```

Single-character words are another edge case worth checking.

Example input:

```
1
a
```

Correct output:

```
a
```

The word is not long enough to abbreviate, so it must remain unchanged. Accessing the first and last character is still valid here because they are the same character.

## Approaches

The most direct way to solve the problem is brute force simulation. For every word, we check its length. If the length is at most 10, we print the word unchanged. Otherwise, we build the abbreviation by taking the first character, computing how many characters lie in the middle, and appending the last character.

This already works efficiently because the constraints are extremely small. Even if every word had length 100, we would process at most 10,000 characters total. That is effectively instant.

A slower brute-force variant would literally count the middle characters one by one instead of using arithmetic. For example, for a word of length 20, we could loop from index 1 to index 18 and increment a counter. This still passes because the input is tiny, but it performs unnecessary work.

The key observation is that the number of removed characters does not need to be counted manually. Once we know the word length, the middle count is always:

```
length - 2
```

That reduces the operation to constant time per word, aside from reading the input itself.

The brute-force idea works because every word is independent. There is no interaction between words, no complicated data structure, and no hidden optimization trick. The only task is applying a fixed transformation rule consistently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force counting middle letters manually | O(total characters) | O(1) | Accepted |
| Optimal arithmetic construction | O(total characters) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the integer `n`, the number of words.
2. Repeat `n` times and read one word each iteration.
3. Check the word length.

If the length is less than or equal to 10, print the word unchanged because it is not considered too long.
4. Otherwise, construct the abbreviation.

Take the first character using `word[0]`.
5. Compute how many characters are between the first and last characters.

This value is `len(word) - 2` because we exclude exactly two characters, the first and the last.
6. Take the last character using `word[-1]`.
7. Concatenate the first character, the middle count converted to a string, and the last character, then print the result.

### Why it works

The algorithm directly follows the definition of the abbreviation. Every long word is transformed into:

```
first letter + number of middle letters + last letter
```

The count of middle letters is always the total length minus the two preserved boundary characters. Since every word is processed independently and the transformation exactly matches the required format, the algorithm always produces the correct output.

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
        abbreviated = word[0] + str(len(word) - 2) + word[-1]
        print(abbreviated)
```

The program starts by reading the number of words. Then it processes each word independently.

The `strip()` call removes the trailing newline character from the input. Without it, the newline would become part of the string length and produce incorrect results.

The condition `len(word) <= 10` matches the problem statement exactly. Using `< 10` or `>= 10` would introduce an off-by-one bug.

For long words, the abbreviation is built from three pieces. `word[0]` gives the first character, `len(word) - 2` gives the number of skipped middle characters, and `word[-1]` gives the final character.

Using `word[-1]` is convenient because it always refers to the last character regardless of the word length.

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

| Word | Length | Too Long? | Middle Count | Output |
| --- | --- | --- | --- | --- |
| word | 4 | No | - | word |
| localization | 12 | Yes | 10 | l10n |
| internationalization | 20 | Yes | 18 | i18n |
| pneumonoultramicroscopicsilicovolcanoconiosis | 45 | Yes | 43 | p43s |

This trace shows the central rule of the problem. Short words remain untouched, while long words are compressed into the first letter, the middle count, and the last letter.

### Example 2

Input:

```
5
abcdefghij
abcdefghijk
a
codeforces
short
```

Trace:

| Word | Length | Too Long? | Middle Count | Output |
| --- | --- | --- | --- | --- |
| abcdefghij | 10 | No | - | abcdefghij |
| abcdefghijk | 11 | Yes | 9 | a9k |
| a | 1 | No | - | a |
| codeforces | 10 | No | - | codeforces |
| short | 5 | No | - | short |

This example focuses on the boundary condition. Words of length exactly 10 are not abbreviated. Only lengths strictly greater than 10 qualify.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(total characters) | Each word is read once and processed in linear time relative to its length |
| Space | O(1) | Only a few variables are used regardless of input size |

The limits are tiny, so this solution easily fits within both the 1 second time limit and the 256 MB memory limit. Even processing every character individually would be fast enough.

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
    sys.stdin = io.StringIO(inp)
    sys.stdout = io.StringIO()

    solve()

    return sys.stdout.getvalue()

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

# minimum-size input
assert run(
"""1
a
"""
) == (
"""a
"""
), "single character word"

# boundary length 10 should not abbreviate
assert run(
"""2
abcdefghij
codeforces
"""
) == (
"""abcdefghij
codeforces
"""
), "length exactly 10"

# length 11 should abbreviate
assert run(
"""1
abcdefghijk
"""
) == (
"""a9k
"""
), "length 11"

# multiple equal long words
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
), "repeated inputs"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `a` | `a` | Minimum possible word length |
| `abcdefghij` | `abcdefghij` | Boundary condition at length 10 |
| `abcdefghijk` | `a9k` | First length that should abbreviate |
| Repeated `localization` | Repeated `l10n` | Consistent processing across multiple words |

## Edge Cases

A word with length exactly 10 must remain unchanged.

Input:

```
1
abcdefghij
```

The algorithm checks `len(word) <= 10`. Since the length is exactly 10, the condition is true and the original word is printed.

Output:

```
abcdefghij
```

This avoids the common off-by-one mistake of abbreviating words that should stay unchanged.

A very long word must compute the middle count correctly.

Input:

```
1
internationalization
```

The length is 20. The algorithm computes:

```
20 - 2 = 18
```

Then it combines:

```
i + 18 + n
```

Output:

```
i18n
```

This confirms that the count refers only to the characters between the first and last letters.

Single-character words also work correctly.

Input:

```
1
a
```

The length is 1, so the word is not abbreviated. The algorithm directly prints the original word.

Output:

```
a
```

No special-case handling is needed because the condition prevents unnecessary abbreviation logic.
