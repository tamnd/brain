---
title: "CF 50B - Choosing Symbol Pairs"
description: "We are given a string of characters consisting of lowercase letters and digits. The task is to count the number of ordered pairs of positions in the string where the characters at those positions are identical."
date: "2026-05-28T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "strings"]
categories: ["algorithms"]
codeforces_contest: 50
codeforces_index: "B"
codeforces_contest_name: "Codeforces Beta Round 47"
rating: 1500
weight: 50
solve_time_s: 75
verified: true
draft: false
---

[CF 50B - Choosing Symbol Pairs](https://codeforces.com/problemset/problem/50/B)

**Rating:** 1500  
**Tags:** strings  
**Solve time:** 1m 15s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a string of characters consisting of lowercase letters and digits. The task is to count the number of ordered pairs of positions in the string where the characters at those positions are identical. A pair is ordered, so for positions `i` and `j`, both `(i, j)` and `(j, i)` count separately. Self-pairs `(i, i)` are also included since the character trivially matches itself.

The string length can be up to 100,000 characters. A brute-force solution that examines every possible pair would require roughly $10^{10}$ comparisons in the worst case, which exceeds what we can compute in two seconds. This immediately rules out naive nested loops.

Subtle edge cases include very short strings and strings where all characters are identical. For example, a single-character string `"a"` should return 1 because the only pair `(1, 1)` is valid. A string like `"aaaa"` should return 16 because each of the 4 characters matches each of the 4 positions, producing $4 \times 4 = 16$ ordered pairs. A careless approach that only counts distinct pairs without self-pairs or without considering order would yield a wrong answer.

## Approaches

The brute-force approach is straightforward: for each character in the string, check it against every other character, counting matches. This is correct because it examines every valid pair, but it requires $O(n^2)$ operations, which is infeasible for $n = 10^5$. In the worst case, it performs roughly $10^{10}$ comparisons.

The key observation to optimize is that we do not need to compare each character individually. We only need to know how many times each distinct character occurs. If a character appears `k` times, it contributes `k * k` ordered pairs: `k` choices for the first position and `k` for the second. Summing this over all distinct characters gives the final answer. This reduces the problem to counting character frequencies, which can be done in a single pass over the string.

This observation turns the algorithm from quadratic to linear, which is necessary given the constraints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(1) | Too slow |
| Optimal | O(n) | O(1) (fixed-size map for 36 characters) | Accepted |

## Algorithm Walkthrough

1. Initialize a frequency dictionary (or array) for characters. Since the string contains only lowercase letters and digits, we can use an array of size 36 indexed by character.
2. Iterate through each character in the string, incrementing its count in the frequency table. At the end of this step, we know how many times each character appears.
3. Initialize a variable `total_pairs` to zero.
4. Iterate through the frequency table. For each character that appears `count` times, add `count * count` to `total_pairs`. The reasoning is that there are `count` options for the first position and `count` for the second, including self-pairs.
5. Print `total_pairs` as the result.

Why it works: The invariant is that each character's contribution to the total number of ordered pairs is exactly the square of its frequency. Since we consider all characters and include self-pairs, all valid pairs are counted exactly once.

## Python Solution

```python
import sys
input = sys.stdin.readline

s = input().strip()
freq = [0] * 36  # 26 letters + 10 digits

def char_index(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    else:
        return 26 + ord(c) - ord('0')

for ch in s:
    freq[char_index(ch)] += 1

total_pairs = sum(f * f for f in freq)
print(total_pairs)
```

The `char_index` function maps each lowercase letter to 0-25 and digits to 26-35, allowing a fixed-size array instead of a dictionary. We iterate once over the string to populate the frequency array, then sum the squares of counts. Using a fixed array avoids dictionary overhead and ensures O(1) access per character.

A subtle point is handling both letters and digits in a single array. Mistakes often happen if someone assumes ASCII codes are contiguous between letters and digits. Another potential pitfall is forgetting to include self-pairs - the squaring step naturally includes them.

## Worked Examples

**Example 1:** `"great10"`

| Character | Frequency | Contribution |
| --- | --- | --- |
| g | 1 | 1 |
| r | 1 | 1 |
| e | 1 | 1 |
| a | 1 | 1 |
| t | 1 | 1 |
| 1 | 1 | 1 |
| 0 | 1 | 1 |

Total pairs = 7

Each character is unique, so only self-pairs exist. This demonstrates the algorithm correctly handles strings without repeated characters.

**Example 2:** `"aaaa"`

| Character | Frequency | Contribution |
| --- | --- | --- |
| a | 4 | 16 |

Total pairs = 16

All pairs are valid, including self-pairs and pairs in both orders. The algorithm counts them automatically via the `count * count` formula.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass to compute frequencies, then sum over 36 entries |
| Space | O(1) | Fixed array of size 36, independent of input length |

The solution easily fits the time and memory limits for n ≤ 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    s = input().strip()
    freq = [0] * 36
    def char_index(c):
        if 'a' <= c <= 'z':
            return ord(c) - ord('a')
        else:
            return 26 + ord(c) - ord('0')
    for ch in s:
        freq[char_index(ch)] += 1
    return str(sum(f * f for f in freq))

# Provided samples
assert run("great10\n") == "7", "sample 1"

# Custom test cases
assert run("aaaa\n") == "16", "all same characters"
assert run("1\n") == "1", "single character"
assert run("ab1ab\n") == "9", "mixed letters and digits with repeats"
assert run("abc123abc123\n") == "24", "repeated letters and digits"
assert run("z9z9z9\n") == "18", "alternating letters and digits"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `"aaaa"` | 16 | all-equal characters, counting order and self-pairs |
| `"1"` | 1 | minimum-length input |
| `"ab1ab"` | 9 | mix of letters and digits, repeated characters |
| `"abc123abc123"` | 24 | repeated letters and digits, multiple occurrences |
| `"z9z9z9"` | 18 | alternating pattern with multiple occurrences |

## Edge Cases

For the single-character string `"1"`, the frequency of `'1'` is 1. Squaring it yields `1`, which is correct. The algorithm handles this trivially because the formula naturally includes self-pairs.

For a string with all identical characters, `"aaaa"`, the frequency is 4. Squaring gives `16`, accounting for all 16 ordered pairs. There is no need for nested loops, which would otherwise overcomplicate the count and risk off-by-one errors.

For a string mixing letters and digits, `"ab1ab"`, frequencies are `'a':2`, `'b':2`, `'1':1`. Contributions are `4 + 4 + 1 = 9`, which confirms the formula works across character types.

This editorial guides the reader from a naive quadratic approach to a linear-time, fixed-space solution by leveraging character frequencies and ordered-pair counting. Following this reasoning, similar problems involving counting pairs with specific matching criteria can be approached efficiently.
