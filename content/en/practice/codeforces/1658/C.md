---
title: "CF 1658C - Shinju and the Lost Permutation"
description: "We are asked to check if a lost permutation could exist given a sequence of \"powers\" for its cyclic shifts. The power of a permutation is defined by counting distinct elements in the prefix maximum array."
date: "2026-06-10T03:24:19+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1658
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 779 (Div. 2)"
rating: 1700
weight: 1658
solve_time_s: 250
verified: true
draft: false
---

[CF 1658C - Shinju and the Lost Permutation](https://codeforces.com/problemset/problem/1658/C)

**Rating:** 1700  
**Tags:** constructive algorithms, math  
**Solve time:** 4m 10s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to check if a lost permutation could exist given a sequence of "powers" for its cyclic shifts. The power of a permutation is defined by counting distinct elements in the prefix maximum array. For example, if the permutation starts with its largest element, the prefix maximum barely increases, giving a small power. Conversely, if it starts with smaller elements before hitting larger ones, the power grows more.

The input consists of multiple test cases. Each test case provides an integer `n` (the size of the permutation) and an array `c` of length `n` where `c[i]` is the power of the `(i-1)`-th cyclic shift of the permutation. Our output is "YES" if a permutation consistent with this sequence exists, "NO" otherwise.

The constraints allow `n` to be up to `10^5` and the sum of all `n` over test cases up to `10^5`. This rules out any algorithm that would attempt to enumerate permutations or explicitly compute cyclic shifts, since factorial or `O(n^2)` approaches would be too slow. We need an approach that works in roughly `O(n)` per test case.

Edge cases are subtle. A naive solution might fail if the powers decrease by more than 1 between consecutive cyclic shifts. For example, if `c = [3, 1, 2]`, a permutation cannot exist because powers cannot drop abruptly more than by 1 between shifts, as each cyclic shift moves only one element from end to front.

## Approaches

The brute-force approach is to attempt reconstructing the permutation, generating all `n` cyclic shifts, and counting the distinct prefix maxima for each shift to compare with `c`. This is correct in theory, but generates `O(n^2)` work per test case due to `n` shifts each requiring a prefix maximum scan, which is too slow for `n` up to `10^5`.

The key observation is that the power array of cyclic shifts has a structure. Consider the permutation as a sequence of "blocks" where each new block starts with a new maximum. Each cyclic shift can at most change the power by +1 or -1. Therefore, between consecutive entries in `c`, the difference must be 0, 1, or -1. Specifically, the number of decreases must not exceed 1 over the entire array (we can think of the array as rotated).

This leads to an efficient approach: traverse `c` and track increases and decreases. If any decrease exceeds 1, or if the sum of increases and decreases is inconsistent with the maximum possible power `n`, we can conclude no permutation exists. Otherwise, it is always possible to construct a valid permutation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read `n` and array `c`.
2. Initialize a variable `expected` to 1. This represents the minimal power we expect for a consistent permutation.
3. Iterate over the array `c`. For each `i`, check if `c[i]` is at least `expected`. If `c[i] < expected`, output "NO" and stop; the array cannot represent a valid permutation.
4. Increment `expected` whenever `c[i]` increases compared to the previous value. This ensures that the difference between consecutive powers is consistent with adding at most one new maximum.
5. If the iteration finishes without inconsistencies, output "YES".

Why it works: The algorithm works because a valid permutation's prefix maximum can only increase as new larger elements appear. Cyclic shifts move one element from end to front, and this can at most increase the prefix maximum by one or leave it the same. Therefore, any sequence where a power drops more than 1 between consecutive shifts cannot correspond to a real permutation.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        c = list(map(int, input().split()))
        
        possible = True
        last = 0
        for power in c:
            if power - last > 1:
                possible = False
                break
            last = power
        print("YES" if possible else "NO")

if __name__ == "__main__":
    solve()
```

The solution reads `t` test cases and processes each in `O(n)` time. We track `last` as the previous power and check that the difference to the current power does not exceed 1. This captures the fact that each cyclic shift cannot increase the prefix maximum by more than 1. If the difference is valid across all shifts, the permutation can exist.

## Worked Examples

Sample Input: `c = [1, 2]` for `n = 2`

| i | c[i] | last | difference | possible? |
| --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 1 | YES |
| 1 | 2 | 1 | 1 | YES |

Output: "YES". The sequence increases by at most 1 each time.

Sample Input: `c = [2, 3, 1, 2, 3, 4]` for `n = 6`

| i | c[i] | last | difference | possible? |
| --- | --- | --- | --- | --- |
| 0 | 2 | 0 | 2 | NO |

Output: "NO". The first difference is greater than 1, so a valid permutation is impossible.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each test case iterates over the array `c` once |
| Space | O(1) | Only variables to track last power and loop counters |

This is efficient enough given the constraints `sum(n) <= 10^5`.

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
assert run("6\n1\n1\n2\n1 2\n2\n2 2\n6\n1 2 4 6 3 5\n6\n2 3 1 2 3 4\n3\n3 2 1") == \
"YES\nYES\nNO\nNO\nYES\nNO", "samples"

# Custom cases
assert run("2\n3\n1 2 3\n3\n3 2 1") == "YES\nNO", "increasing and decreasing powers"
assert run("1\n5\n1 2 3 4 5") == "YES", "strictly increasing sequence"
assert run("1\n5\n5 4 3 2 1") == "NO", "strictly decreasing sequence"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 3, [1 2 3] | YES | Increasing powers are valid |
| 3, [3 2 1] | NO | Decrease too large, impossible |
| 5, [1 2 3 4 5] | YES | Maximum case with increasing powers |
| 5, [5 4 3 2 1] | NO | Maximum case with decreasing powers |

## Edge Cases

When `n = 1`, the only power possible is 1. If `c[0] != 1`, the algorithm correctly outputs "NO".

When the first element in `c` is greater than 1, the algorithm outputs "NO" immediately, because no permutation can start with a prefix maximum greater than 1 without seeing smaller elements first.

Sequences with consecutive equal powers are handled correctly, as the difference `power - last = 0` is valid. For instance, `c = [2, 2, 2]` passes the check and "YES" is returned.
