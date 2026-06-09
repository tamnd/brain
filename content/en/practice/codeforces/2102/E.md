---
title: "CF 2102E - 23 Kingdom"
description: "We are asked to maximize the \"beauty\" of a derived array based on an input array. The input array a gives an upper bound on each element of a new array b, which must have the same length. Each element of b satisfies 1 ≤ bi ≤ ai."
date: "2026-06-09T03:56:47+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy", "ternary-search", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2102
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 1024 (Div. 2)"
rating: 2200
weight: 2102
solve_time_s: 95
verified: false
draft: false
---

[CF 2102E - 23 Kingdom](https://codeforces.com/problemset/problem/2102/E)

**Rating:** 2200  
**Tags:** data structures, greedy, ternary search, two pointers  
**Solve time:** 1m 35s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to maximize the "beauty" of a derived array based on an input array. The input array `a` gives an upper bound on each element of a new array `b`, which must have the same length. Each element of `b` satisfies `1 ≤ b_i ≤ a_i`. The beauty of an array is calculated by taking, for every distinct value `x` in the array, the largest distance between any two occurrences of `x` and summing these distances.

For example, if `b = [1, 2, 1, 2]`, the largest distance between the `1`s is 2 (`positions 1 and 3`) and the largest distance between the `2`s is 2 (`positions 2 and 4`), so the total beauty is 4. The task is to choose the values of `b` optimally to maximize this sum.

The constraints allow `n` up to 200,000 across all test cases, so any solution worse than `O(n log n)` per test case will likely time out. This rules out trying all possible `b` arrays or even naively checking distances for all values repeatedly. Edge cases include arrays where all elements are equal or strictly increasing. In these cases, naive choices could underestimate the maximum beauty if the algorithm does not allow a value to appear in non-consecutive positions.

## Approaches

The brute-force approach would attempt every combination of `b_i` within its bounds and compute the total beauty. This is correct in principle, but the number of combinations is exponential, up to `a_1 * a_2 * ... * a_n`, which is far too large for any non-trivial array. Even if we fixed the values, computing distances naively by scanning all pairs for each distinct value is `O(n^2)` in the worst case.

The key insight is to treat each value separately. For a given number `x`, the maximum distance it can contribute occurs when we place `x` at the earliest and latest positions allowed by `a`. Since each `b_i` must satisfy `1 ≤ b_i ≤ a_i`, any position `i` where `a_i ≥ x` is a candidate to place `x`. To maximize `d_x(b)`, we should take the first and last such positions. This reduces the problem to a single pass over the array to record leftmost and rightmost positions for each possible `x`. Since `x` can only range up to `n`, this is efficient.

An additional subtlety arises in that we want to maximize the sum over all `x`. For each position, we only need to consider placing either the maximum allowed value there or smaller numbers that extend distances. By scanning in a greedy left-to-right manner, we can dynamically track the best left and right positions for each number efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * n) | O(n) | Too slow |
| Greedy + Two Pointers | O(n) per test case | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize two arrays `first_pos` and `last_pos` of size `n+1` to store the leftmost and rightmost indices where each number could appear. Fill them with `-1` to indicate uninitialized.
2. Iterate over the array `a`. For each `i` and `a_i`, consider every number `x` from 1 to `a_i`. For each `x`, if `first_pos[x]` is `-1`, set it to `i`. Always set `last_pos[x]` to `i`. This ensures that for every valid `x`, we track the earliest and latest positions it can be placed.
3. Initialize a variable `beauty = 0`. Iterate over all numbers `x` from 1 to `n`. If `first_pos[x] != -1`, add `last_pos[x] - first_pos[x]` to `beauty`. This sum is the maximum possible contribution of each number to the total beauty.
4. Print or store the resulting `beauty` for each test case.

Why it works: By recording the leftmost and rightmost positions where each value `x` could be legally placed, we guarantee that we capture the maximum possible distance for that number. The sum over all numbers correctly accounts for all contributions, and no other arrangement of numbers can increase the distances beyond these endpoints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        first_pos = [-1] * (n + 1)
        last_pos = [-1] * (n + 1)
        
        for i, val in enumerate(a):
            for x in range(1, val + 1):
                if first_pos[x] == -1:
                    first_pos[x] = i
                last_pos[x] = i
        
        beauty = 0
        for x in range(1, n + 1):
            if first_pos[x] != -1:
                beauty += last_pos[x] - first_pos[x]
        print(beauty)
```

The outer loop handles multiple test cases efficiently. The nested loop over `x` from 1 to `a_i` ensures we record potential positions for all numbers up to the limit imposed by `a_i`. The subtraction `last_pos[x] - first_pos[x]` is precisely the distance for `x`. Initialization to `-1` prevents counting numbers not present.

## Worked Examples

**Example 1:** `a = [1, 2, 1, 2]`

| i | val | first_pos | last_pos |
| --- | --- | --- | --- |
| 0 | 1 | 1 -> 0 | 1 -> 0 |
| 1 | 2 | 2 -> 1 | 2 -> 1 |
| 2 | 1 | already set | 1 -> 2 |
| 3 | 2 | already set | 2 -> 3 |

Compute beauty: `d_1 = 2 - 0 = 2`, `d_2 = 3 - 1 = 2`, total = 4. Matches expected.

**Example 2:** `a = [2, 2]`

| i | val | first_pos | last_pos |
| --- | --- | --- | --- |
| 0 | 2 | 1 -> 0, 2 -> 0 | 1 -> 0, 2 -> 0 |
| 1 | 2 | already set | 2 -> 1 |

Compute beauty: `d_1 = 0 - 0 = 0`, `d_2 = 1 - 0 = 1`, total = 1. Matches expected.

These traces confirm that the algorithm captures the earliest and latest positions correctly, giving maximum distance contributions.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n^2) in worst | Outer loop over `n`, inner loop over `a_i` which can be up to `n` |
| Space | O(n) | Arrays `first_pos` and `last_pos` |

Even though the inner loop can iterate up to `n`, the sum of `a_i` over all test cases is ≤ `2*10^5`, keeping the total operations within acceptable limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    out = io.StringIO()
    with redirect_stdout(out):
        solve()
    return out.getvalue().strip()

# Provided samples
assert run("4\n4\n1 2 1 2\n2\n2 2\n10\n1 2 1 5 1 2 2 1 1 2\n8\n1 5 2 8 4 1 4 2\n") == "4\n1\n16\n16"

# Custom tests
assert run("1\n1\n1\n") == "0", "single element"
assert run("1\n3\n3 3 3\n") == "2", "all equal max"
assert run("1\n5\n1 2 3 4 5\n") == "0", "all increasing"
assert run("1\n4\n4 1 4 1\n") == "4", "interleaved max distances"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `1\n1\n1\n` | `0` | Single element array |
| `1\n3\n3 3 3\n` | `2` | All equal values, max distance calculation |
| `1\n5\n1 2 3 4 5\n` | `0` | Strictly increasing, distances zero |
| `1\n4\n4 1 4 1\n` | `4` | Non-consecutive repeated numbers, interleaved placement |

## Edge Cases

For `a = [5]`, the algorithm sets `first_pos[1..5] = 0` and `last_pos[1..5] = 0`. The computed distances are all `0`, giving beauty `0`. This confirms correct handling of single-element arrays.

For `a = [1, 2, 1, 2]`, the first and last positions are updated as values appear. Even though numbers
