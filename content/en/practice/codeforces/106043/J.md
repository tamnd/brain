---
title: "CF 106043J - Stones"
description: "We are given a row of stones where each stone has a color, represented by a character string. The goal is to transform the row so that no two adjacent stones share the same color. We are not allowed to rearrange stones; instead, we can remove stones."
date: "2026-06-25T12:50:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106043
codeforces_index: "J"
codeforces_contest_name: "Teamscode Summer 2025 Advanced Division"
rating: 0
weight: 106043
solve_time_s: 49
verified: true
draft: false
---

[CF 106043J - Stones](https://codeforces.com/problemset/problem/106043/J)

**Rating:** -  
**Tags:** -  
**Solve time:** 49s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a row of stones where each stone has a color, represented by a character string. The goal is to transform the row so that no two adjacent stones share the same color. We are not allowed to rearrange stones; instead, we can remove stones. The task is to determine the minimum number of removals needed so that the remaining sequence has no consecutive equal characters.

In other words, we want to compress the string into a “strictly alternating adjacency” sequence by deleting as few characters as possible. The final sequence must preserve original order, but any number of deletions is allowed.

The input size is small in this problem (typical Codeforces version has n up to 50), which immediately suggests that even quadratic or linear scans with small constants are sufficient. Anything beyond O(n²) is unnecessary, and even O(n²) is overkill.

The key edge cases appear when the string is already valid, or when all characters are identical.

For example, if the input is `BRBG`, no two neighbors are equal, so the answer is 0. If the input is `RRRRR`, we must keep only one character, so we remove 4.

A subtle failure mode for naive approaches is trying to “simulate removals” while iterating forward without carefully handling shifting indices. For instance, in `RBBR`, if you remove greedily without re-checking newly adjacent pairs, you might incorrectly delete more than necessary or miss that after one deletion the structure changes.

A correct solution avoids simulation entirely and instead counts structure directly.

## Approaches

The brute-force idea is to explicitly try deleting subsets of characters and check whether the resulting string has no equal adjacent pairs. For each subset, we reconstruct the string and validate it in O(n). Since there are 2ⁿ subsets, this quickly becomes infeasible even for modest n; at n = 50, this is astronomically large and completely unusable.

The key observation is that we do not actually need to decide which characters remain, only how many consecutive equal pairs exist in the original string. Every time we see two identical adjacent characters, at least one of them must be removed. If we scan left to right and count how many positions i satisfy s[i] == s[i−1], each such occurrence represents one required deletion in an optimal strategy.

This works because any maximal block of identical characters of length k can be reduced to a single character, requiring exactly k−1 deletions. Summing this over all runs gives the answer.

This turns the problem from a combinatorial selection problem into a linear pass over runs of equal characters.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force subsets | O(2ⁿ · n) | O(n) | Too slow |
| Scan runs of equal chars | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Start scanning the string from left to right, maintaining a counter of deletions.
2. For each position i starting from 1, compare the current character with the previous one.
3. If they are equal, increment the deletion counter because one of them must be removed to break the adjacency.
4. Continue through the string without modifying it.
5. Output the total number of increments after the scan finishes.

Each increment corresponds exactly to one “extra” character inside a contiguous block of identical letters, which cannot remain in the final valid sequence.

### Why it works

The string can be decomposed uniquely into maximal segments of equal characters. In a segment of length k, any valid final sequence can keep at most one character from that segment because keeping two would immediately violate the adjacency rule. Therefore the minimum deletions for that segment is k−1. Summing k−1 over all segments is equivalent to counting transitions where s[i] == s[i−1], which is exactly what the algorithm does.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n = int(input().strip())
    s = input().strip()

    deletions = 0

    for i in range(1, n):
        if s[i] == s[i - 1]:
            deletions += 1

    print(deletions)

if __name__ == "__main__":
    solve()
```

The solution relies on a single linear scan. The variable `deletions` tracks exactly how many adjacent equal pairs exist in the original string. We never modify the string, which avoids index-shifting bugs common in greedy simulation approaches.

The loop starts at index 1 because each comparison is against the previous character. This avoids out-of-bounds checks and cleanly captures every adjacency once.

## Worked Examples

### Example 1: `RRG`

| i | s[i-1] | s[i] | Equal? | deletions |
| --- | --- | --- | --- | --- |
| 1 | R | R | yes | 1 |
| 2 | R | G | no | 1 |

Final output is 1, meaning we remove one of the consecutive R’s.

This confirms that a single run of length 2 contributes exactly one deletion.

### Example 2: `RRRRR`

| i | s[i-1] | s[i] | Equal? | deletions |
| --- | --- | --- | --- | --- |
| 1 | R | R | yes | 1 |
| 2 | R | R | yes | 2 |
| 3 | R | R | yes | 3 |
| 4 | R | R | yes | 4 |

Final output is 4, matching the idea that a block of length 5 needs 4 removals.

This example shows how long uniform segments accumulate deletions linearly.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | single pass over the string |
| Space | O(1) | only a counter is stored |

The constraints are small, but the linear solution is still the cleanest and avoids unnecessary simulation logic. Even for much larger n, this remains optimal and easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from sys import stdout
    out = io.StringIO()
    sys.stdout = out

    # solution
    n = int(input().strip())
    s = input().strip()

    deletions = 0
    for i in range(1, n):
        if s[i] == s[i - 1]:
            deletions += 1

    print(deletions)

    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# provided samples
assert run("3\nRRG\n") == "1", "sample 1"
assert run("5\nRRRRR\n") == "4", "sample 2"
assert run("4\nBRBG\n") == "0", "sample 3"

# custom cases
assert run("1\nR\n") == "0", "single element"
assert run("2\nRR\n") == "1", "minimal duplicate"
assert run("6\nRBBBRG\n") == "2", "mixed blocks"
assert run("7\nRGBRGBG\n") == "0", "already valid alternating"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1 R` | 0 | single element edge case |
| `RR` | 1 | smallest removal case |
| `RBBBRG` | 2 | multiple blocks of duplicates |
| `RGBRGBG` | 0 | already valid alternating structure |

## Edge Cases

A single-character string contains no adjacent pairs, so the scan never increments the counter and the output is correctly 0. The algorithm handles this naturally because the loop starts at index 1 and never executes.

A fully uniform string such as `RRRRR` produces an increment at every step, accumulating exactly n−1 deletions. This matches the requirement that only one character can remain.

Strings with alternating structure like `RGBRGB` produce no equal adjacent pairs, so the deletion count remains zero, confirming that no unnecessary removals are triggered.

Strings with mixed blocks such as `RBBR` show that only internal duplicates matter. The two consecutive B’s contribute exactly one deletion, and no other positions affect the result.
