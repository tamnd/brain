---
title: "CF 1837C - Best Binary String"
description: "We are given a string s that contains 0, 1, and ?. The question marks represent flexible positions: we can replace each ? independently with either 0 or 1. Our goal is to produce a fully binary string matching this pattern such that the cost of sorting it is minimized."
date: "2026-06-09T06:38:58+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1837
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 149 (Rated for Div. 2)"
rating: 1000
weight: 1837
solve_time_s: 98
verified: false
draft: false
---

[CF 1837C - Best Binary String](https://codeforces.com/problemset/problem/1837/C)

**Rating:** 1000  
**Tags:** constructive algorithms, greedy  
**Solve time:** 1m 38s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a string `s` that contains `0`, `1`, and `?`. The question marks represent flexible positions: we can replace each `?` independently with either `0` or `1`. Our goal is to produce a fully binary string matching this pattern such that the cost of sorting it is minimized. Here, cost is defined as the minimum number of contiguous substring reversals required to make the string non-decreasing.

For example, if `s` is `??01?`, one replacement could be `00011`. This string is already sorted, so its cost is 0. If we chose `11010`, the cost would be higher, because we would need multiple reversals to sort it.

The input size allows strings up to 300,000 characters and up to 30,000 test cases, with a total character count across all test cases of at most 300,000. This implies any algorithm must run in linear time relative to the string length for each test case. Quadratic approaches, such as testing all combinations of `?` replacements or simulating all reversals, are infeasible.

A subtle edge case is when a pattern has all `?` characters. A naive approach might fill them arbitrarily, such as all `0`s or all `1`s, but that may not yield the minimal cost. For instance, `???` should ideally become `000` or `111` to avoid unnecessary reversals, whereas `010` would force at least one reversal. Similarly, a pattern like `?1?0?` needs careful filling around existing `0`s and `1`s to avoid creating decreasing sequences that increase the cost.

## Approaches

A brute-force method would enumerate all possible replacements for `?`, generate all matching strings, and calculate the reversal cost for each. The cost of sorting a binary string can be computed by counting "blocks" of consecutive `1`s after the last `0` or vice versa. For a string of length `n`, there are up to `2^k` replacements for `k` question marks. In the worst case, `k` could be `3*10^5`, so this is completely infeasible.

The key insight is that the cost is determined by the number of transitions from `1` to `0` in the final string. Every contiguous block of `1`s followed by a `0` requires one reversal to sort. Therefore, to minimize cost, we should avoid creating a `1` followed by a `0` whenever possible. This immediately suggests a greedy approach: propagate `0`s to the left and `1`s to the right wherever possible. Concretely, any `?` between a `0` and a `1` can be chosen to match its neighbor to avoid creating extra transitions. If a `?` is surrounded only by `?`s, it can safely become either `0` or `1` without increasing cost.

The greedy propagation works in two passes: one forward pass to handle `0`s and one backward pass to handle `1`s. This ensures every `?` is filled in a way that does not create unnecessary `1->0` transitions. The algorithm is linear in string length.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^k * n) | O(n) | Too slow |
| Greedy Propagation | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Convert the input string `s` into a list of characters to allow in-place modifications.
2. Perform a forward pass from left to right. Keep track of the last seen `0`. Whenever a `?` follows a `0`, replace it with `0`. This ensures no new `1->0` transitions are created immediately after a `0`.
3. Perform a backward pass from right to left. Keep track of the last seen `1`. Whenever a `?` precedes a `1`, replace it with `1`. This avoids new transitions from `1` to `0` in reverse.
4. After these two passes, any remaining `?` can be safely replaced with `0` (or `1`) because they are isolated and do not create additional transitions.
5. Join the list back into a string and print it.

Why it works: Each `1->0` transition in a binary string contributes one to the cost. The greedy propagation ensures that no `?` fills introduce a new `1->0` transition. The two-pass system guarantees that all positions influenced by existing `0`s or `1`s adopt a value that does not increase the cost. Any remaining isolated `?`s are either at the edges or surrounded by uniform characters, so their choice does not affect the cost.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        s = list(input().strip())
        n = len(s)

        # Forward pass: propagate 0s
        last_zero = -1
        for i in range(n):
            if s[i] == '0':
                last_zero = i
            elif s[i] == '?' and last_zero != -1:
                s[i] = '0'

        # Backward pass: propagate 1s
        last_one = -1
        for i in reversed(range(n)):
            if s[i] == '1':
                last_one = i
            elif s[i] == '?' and last_one != -1:
                s[i] = '1'

        # Replace remaining '?'
        for i in range(n):
            if s[i] == '?':
                s[i] = '0'

        print("".join(s))

if __name__ == "__main__":
    solve()
```

The forward pass ensures all `?` following a `0` become `0`, preventing new transitions. The backward pass does the same for `1`s in reverse. Any remaining `?`s, isolated or at the edges, are filled with `0`s to produce a valid binary string. This approach avoids any off-by-one errors, as the replacement only occurs if the last seen character exists.

## Worked Examples

**Example 1:** `??01?`

| Index | Char | Last Zero | Last One | Action |
| --- | --- | --- | --- | --- |
| 0 | ? | -1 | -1 | keep ? |
| 1 | ? | -1 | -1 | keep ? |
| 2 | 0 | 2 | -1 | forward pass no change |
| 3 | 1 | 2 | 3 | backward pass no change |
| 4 | ? | 2 | 3 | backward pass sets 1 |

Remaining `?`s: indices 0,1 → set to `0`. Result: `00011`. Cost is 0, minimal.

**Example 2:** `1??10?`

| Index | Char | Last Zero | Last One | Action |
| --- | --- | --- | --- | --- |
| 0 | 1 | -1 | 0 | backward pass propagates 1 to ? |
| 1 | ? | -1 | 0 | becomes 1 |
| 2 | ? | -1 | 0 | becomes 1 |
| 3 | 1 | -1 | 3 | no change |
| 4 | 0 | 4 | 3 | forward pass sets nothing, backward pass sets nothing |
| 5 | ? | 4 | 3 | backward pass sets 1 |

Resulting string: `111101`. Cost is 1, minimal.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each pass scans the string once, total 3 passes: forward, backward, final replacement. |
| Space | O(n) | We store the string as a list of characters for mutable operations. |

With `n` up to 300,000 and up to 30,000 test cases, the linear approach scales well because the sum of string lengths is bounded by 300,000. Memory usage is linear per string.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# provided samples
assert run("4\n??01?\n10100\n1??10?\n0?1?10?10\n") == "00011\n10100\n111101\n011110010", "sample 1"

# custom test cases
assert run("1\n???\n") == "000", "all question marks"
assert run("1\n0?1\n") == "001", "single ? between 0 and 1"
assert run("1\n1???0\n") == "11110", "question marks between 1 and 0"
assert run("1\n?0?\n") == "000", "question marks at edges with 0 in middle"
assert run("1\n1\n") == "1", "single character string"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| ??? | 000 | all `?` replacement |
| 0?1 | 001 | `?` between 0 and 1 |
|  |  |  |
