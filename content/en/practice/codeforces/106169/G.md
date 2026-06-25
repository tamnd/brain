---
title: "CF 106169G - Secret Words"
description: "We are given a dictionary of secret words and a text string. The text contains lowercase letters and the special character ?. A ? can stand for any single lowercase letter. The task is to count how many different ways the entire text can be split into dictionary words."
date: "2026-06-25T11:09:02+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106169
codeforces_index: "G"
codeforces_contest_name: "2025-2026 ICPC NERC, Kyrgyzstan Regional Contest"
rating: 0
weight: 106169
solve_time_s: 45
verified: true
draft: false
---

[CF 106169G - Secret Words](https://codeforces.com/problemset/problem/106169/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 45s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a dictionary of secret words and a text string. The text contains lowercase letters and the special character `?`.

A `?` can stand for any single lowercase letter. The task is to count how many different ways the entire text can be split into dictionary words.

A dictionary word matches a segment of the text if they have the same length and every position satisfies one of the following conditions:

- the text character equals the word character;
- the text character is `?`, meaning it can represent that word character.

Each dictionary word may be used any number of times. Every character of the text must belong to exactly one chosen word. We need the number of valid decompositions modulo `10^9 + 7`.

The constraints are small but very suggestive. There are at most 100 words, each word has length at most 10, and the text length is at most 100. A solution around `O(|T| * n * maxLen)` is completely safe. Even `100 * 100 * 10 = 100000` character comparisons is tiny.

The main subtlety is that a `?` does not create just one matching word. It may match several different dictionary words, and every matching choice contributes separately to the answer.

Consider the first sample:

```
Words: a, b, c, d, ab, bc, cd
Text: ab?d
```

The third character can behave as `a`, `b`, `c`, or `d`, producing several distinct decompositions. The answer is 11, not 4.

Another easy mistake is forgetting that different words of the same length can match the same substring.

Example:

```
Words:
ab
ac

Text:
a?
```

Both words match. The answer is:

```
2
```

A boolean DP that only records whether a position is reachable would incorrectly return 1.

A third edge case is when the whole text consists of question marks.

Example:

```
Words:
a
b

Text:
??
```

The first position has 2 choices and the second position has 2 choices, so the answer is:

```
4
```

This is one of the official samples.

## Approaches

The most direct idea is recursive backtracking. Starting from the beginning of the text, try every dictionary word that matches the current position and recursively process the remainder of the string. Every successful completion contributes one to the answer.

This approach is correct because every valid decomposition corresponds to exactly one path in the recursion tree. The problem is that the same suffix is recomputed many times. In the worst case, such as a text full of `?` characters and many matching words, the number of recursive states grows exponentially.

The repeated work suggests dynamic programming.

Let `dp[i]` denote the number of ways to decompose the prefix ending before position `i`. Then every matching word gives a transition from an earlier position into a later position.

Suppose a word of length `L` matches the substring ending at position `i`. Then every valid decomposition of the prefix before that word can be extended by this word. This gives:

```
dp[i] += dp[i - L]
```

The only remaining task is efficiently checking whether a word matches a text segment. Since word lengths are at most 10, a simple character-by-character comparison is already fast enough.

The brute force explores decompositions directly. The dynamic programming solution counts all decompositions of every prefix once and reuses those results.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | Exponential | O( | T |
| Optimal DP | O( | T | × n × maxLen) |

## Algorithm Walkthrough

1. Read all dictionary words.
2. Let `m` be the length of the text and create an array `dp` of length `m + 1`.
3. Set `dp[0] = 1`.

This represents the empty prefix. There is exactly one way to decompose nothing.
4. For every position `i` from `0` to `m - 1`, examine every dictionary word.
5. Let the current word have length `L`.

If `i + L > m`, the word cannot start at position `i`, so skip it.
6. Compare the word with the text segment `T[i : i + L]`.

For every position `j`, the match succeeds if either `T[i + j] == '?'` or `T[i + j] == word[j]`.
7. If the entire word matches, add:

```
dp[i + L] += dp[i]
```

and take the result modulo `10^9 + 7`.

Every decomposition reaching position `i` can be extended with this matching word.
8. After processing all positions and words, output `dp[m]`.

### Why it works

The invariant is that `dp[i]` always equals the number of valid decompositions of the first `i` characters of the text.

Initially this is true because the empty prefix has exactly one decomposition.

Whenever a word matches starting at position `i`, every decomposition counted by `dp[i]` can be extended by that word, producing a decomposition of length `i + L`. The transition adds exactly those new decompositions and nothing else.

Every valid decomposition has a unique last word. When that last word is processed, the decomposition is counted exactly once through its preceding prefix. Because every decomposition is generated once and every generated decomposition is valid, `dp[m]` equals the desired answer.

## Python Solution

```python
import sys
input = sys.stdin.readline

MOD = 10 ** 9 + 7

n = int(input())
words = [input().strip() for _ in range(n)]
text = input().strip()

m = len(text)

dp = [0] * (m + 1)
dp[0] = 1

for i in range(m):
    if dp[i] == 0:
        continue

    for word in words:
        L = len(word)

        if i + L > m:
            continue

        ok = True
        for j in range(L):
            if text[i + j] != '?' and text[i + j] != word[j]:
                ok = False
                break

        if ok:
            dp[i + L] = (dp[i + L] + dp[i]) % MOD

print(dp[m])
```

The DP array stores counts for prefixes. Position `i` represents the first `i` characters of the text, which makes the transitions clean and avoids off-by-one errors.

The matching test is performed directly. Since every word length is at most 10, there is no need for hashing, tries, or string preprocessing.

The `if dp[i] == 0` check is not required for correctness, but it avoids unnecessary matching attempts from unreachable states.

The modulo operation is applied after every addition because the number of decompositions can grow very quickly when many `?` characters are present.

## Worked Examples

### Example 1

Input:

```
7
a
b
c
d
ab
bc
cd
ab?d
```

Let `dp[i]` represent the number of ways for the first `i` characters.

| Position | Matching words starting here | DP updates |
| --- | --- | --- |
| 0 | a, ab | dp[1]+=1, dp[2]+=1 |
| 1 | b, bc | dp[2]+=1, dp[3]+=1 |
| 2 | a, b, c, d, cd | dp[3]+=2, dp[4]+=2, dp[4]+=2, dp[4]+=2, dp[4]+=2 |
| 3 | d | dp[4]+=5 |

Final DP:

| i | 0 | 1 | 2 | 3 | 4 |
| --- | --- | --- | --- | --- | --- |
| dp[i] | 1 | 1 | 2 | 3 | 11 |

Answer:

```
11
```

This example shows how a single `?` can simultaneously match many different words, each contributing additional decompositions.

### Example 2

Input:

```
2
a
b
??
```

| Position | Matching words | DP updates |
| --- | --- | --- |
| 0 | a, b | dp[1]=2 |
| 1 | a, b | dp[2]=4 |

Final DP:

| i | 0 | 1 | 2 |
| --- | --- | --- | --- |
| dp[i] | 1 | 2 | 4 |

Answer:

```
4
```

This demonstrates that every `?` independently branches into multiple valid choices.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O( | T |
| Space | O( | T |

With `|T| ≤ 100`, `n ≤ 100`, and `maxLen ≤ 10`, the worst-case work is roughly 100,000 character comparisons, which is easily within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    MOD = 10 ** 9 + 7

    n = int(input())
    words = [input().strip() for _ in range(n)]
    text = input().strip()

    m = len(text)
    dp = [0] * (m + 1)
    dp[0] = 1

    for i in range(m):
        if dp[i] == 0:
            continue

        for word in words:
            L = len(word)

            if i + L > m:
                continue

            ok = True
            for j in range(L):
                if text[i + j] != '?' and text[i + j] != word[j]:
                    ok = False
                    break

            if ok:
                dp[i + L] = (dp[i + L] + dp[i]) % MOD

    return str(dp[m]) + "\n"

# provided samples
assert run(
"""7
a
b
c
d
ab
bc
cd
ab?d
"""
) == "11\n", "sample 1"

assert run(
"""2
a
b
??
"""
) == "4\n", "sample 2"

# minimum size
assert run(
"""1
a
a
"""
) == "1\n", "single exact match"

# impossible decomposition
assert run(
"""1
ab
a
"""
) == "0\n", "cannot cover whole text"

# multiple words match same segment
assert run(
"""2
ab
ac
a?
"""
) == "2\n", "two matching words"

# overlapping decomposition choices
assert run(
"""3
a
aa
aaa
aaa
"""
) == "4\n", "different partition lengths"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| One word `a`, text `a` | 1 | Smallest valid instance |
| One word `ab`, text `a` | 0 | Impossible coverage |
| Words `ab`, `ac`, text `a?` | 2 | Multiple words matching same segment |
| Words `a`, `aa`, `aaa`, text `aaa` | 4 | Multiple partition structures |

## Edge Cases

Consider:

```
2
ab
ac
a?
```

At position 0, both words match because `?` can represent either `b` or `c`.

The algorithm performs both transitions:

```
dp[2] += dp[0]
dp[2] += dp[0]
```

giving `dp[2] = 2`. A solution that only checked whether some word matched would incorrectly produce 1.

Consider:

```
2
a
b
??
```

At the first character, both words match. The same happens at the second character.

The DP evolves as:

```
dp = [1, 2, 4]
```

and returns 4. This correctly counts every assignment of letters implied by the chosen words.

Consider:

```
1
ab
a
```

The word is longer than the remaining text. The transition is skipped because `i + L > m`. No state reaches the end, so `dp[m]` remains 0, correctly indicating that the text cannot be decomposed into dictionary words.
