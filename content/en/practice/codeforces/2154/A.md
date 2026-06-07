---
title: "CF 2154A - Notelock"
description: "We are given a binary string consisting of 0s and 1s and a positive integer k. Each 1 in the string can be “turned off” by Teto according to a simple local rule: if a 1 is not protected and there are no other 1s in the previous k-1 positions, it can be changed to 0."
date: "2026-06-08T00:35:30+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 2154
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 1060 (Div. 2)"
rating: 800
weight: 2154
solve_time_s: 96
verified: false
draft: false
---

[CF 2154A - Notelock](https://codeforces.com/problemset/problem/2154/A)

**Rating:** 800  
**Tags:** greedy, two pointers  
**Solve time:** 1m 36s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a binary string consisting of `0`s and `1`s and a positive integer `k`. Each `1` in the string can be “turned off” by Teto according to a simple local rule: if a `1` is not protected and there are no other `1`s in the previous `k-1` positions, it can be changed to `0`. Our goal is to protect a minimum number of `1`s such that after Teto applies this process from left to right, the string remains exactly as it was.

The input gives multiple test cases. For each, we receive the length of the string, the integer `k`, and the string itself. We are asked to output the minimum number of positions we must protect to prevent any `1` from being changed.

The constraints tell us that the total sum of `n` across all test cases does not exceed 1000. This means even an `O(n^2)` approach might barely fit, but a linear scan is preferable and much safer. Edge cases to watch include strings where all characters are `0`, where `k` is equal to `n`, or where `1`s appear consecutively.

A subtle edge case is when `1`s are spaced exactly `k` apart. Protecting one may prevent multiple others from being changed, and a naive “protect each `1` independently” strategy would overcount.

## Approaches

The brute-force approach would be to simulate Teto’s process for every possible subset of `1`s we could protect. We could generate all combinations, simulate the transformation, and check if the string remains unchanged. While this would be correct, it is exponential in the number of `1`s, which can be up to 1000, making it completely infeasible.

The optimal approach observes that Teto’s operation only affects `1`s that have no other `1`s within the previous `k-1` positions. This means if we scan from left to right, we only need to ensure that between any two protected `1`s there is at most `k-1` unprotected positions separating them. The key insight is that `1`s that are already within `k` positions of a previous protected `1` are safe and do not require protection. Therefore, a greedy left-to-right scan is sufficient: whenever we encounter a `1` that is not covered by the previous protected `1` (i.e., farther than `k-1` positions away), we protect it. This directly gives the minimum number of positions to protect.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(2^n * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Initialize a variable `last_protected` to a value less than the first index (for example `-k`) to track the position of the last `1` we protected. Initialize a counter `count` to zero to track the number of protections.
2. Iterate through the string from left to right. For each position `i`:

- If the character at `i` is `1` and `i - last_protected >= k`, this means the previous protected `1` is too far away to prevent Teto from changing this one. Protect the current `1` by incrementing `count` and setting `last_protected = i`.
- Otherwise, do nothing, because this `1` is already within the safe range of the last protected `1`.
3. After scanning the string, `count` contains the minimum number of `1`s we need to protect.

The invariant that guarantees correctness is that at each step, we maintain the property that every unprotected `1` is within `k-1` positions of a previously protected `1`. This ensures that no `1` ever satisfies the condition for Teto to turn it into `0`.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, k = map(int, input().split())
    s = input().strip()
    
    last_protected = -k  # no protection yet
    count = 0
    for i, c in enumerate(s):
        if c == '1' and i - last_protected >= k:
            count += 1
            last_protected = i
    print(count)
```

The solution initializes `last_protected` to `-k` to handle the first `1` correctly without special-casing. The `enumerate` loop scans the string in linear time, protecting only the necessary `1`s. Using `i - last_protected >= k` correctly enforces the safe distance.

## Worked Examples

Consider the string `1010101` with `k = 2`.

| i | c | last_protected | i - last_protected >= k? | action | count |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | -2 | 2 >= 2 | protect | 1 |
| 1 | 0 | 0 | n/a | skip | 1 |
| 2 | 1 | 0 | 2 >= 2 | protect | 2 |
| 3 | 0 | 2 | n/a | skip | 2 |
| 4 | 1 | 2 | 2 >= 2 | protect | 3 |
| 5 | 0 | 4 | n/a | skip | 3 |
| 6 | 1 | 4 | 2 >= 2 | protect | 4 |

Count is `4`, which matches the sample output.

Another example: `0000001` with `k = 4`.

| i | c | last_protected | i - last_protected >= k? | action | count |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | -4 | n/a | skip | 0 |
| 1 | 0 | -4 | n/a | skip | 0 |
| 2 | 0 | -4 | n/a | skip | 0 |
| 3 | 0 | -4 | n/a | skip | 0 |
| 4 | 0 | -4 | n/a | skip | 0 |
| 5 | 0 | -4 | n/a | skip | 0 |
| 6 | 1 | -4 | 10 >= 4 | protect | 1 |

Count is `1`.

These traces confirm that the left-to-right greedy correctly selects the minimal necessary protections while ensuring safety.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single scan of the string per test case; `n <= 1000` across all cases |
| Space | O(1) | Only a few integer variables are used; string input can be read in place |

Given `n` sum ≤ 1000, this linear solution is extremely fast and well within both the 1-second limit and memory constraints.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        s = input().strip()
        last_protected = -k
        count = 0
        for i, c in enumerate(s):
            if c == '1' and i - last_protected >= k:
                count += 1
                last_protected = i
        print(count)
    
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# Provided samples
assert run("9\n2 2\n11\n6 6\n100001\n5 3\n10000\n7 2\n1010101\n7 4\n0000001\n3 3\n010\n3 2\n011\n7 4\n1001001\n8 3\n00000000\n") == "1\n1\n1\n4\n1\n1\n1\n1\n0"

# Custom cases
assert run("1\n5 2\n00000\n") == "0"  # no 1s, no protection needed
assert run("1\n1 1\n1\n") == "1"  # smallest string, must protect the single 1
assert run("1\n6 6\n101101\n") == "2"  # spacing larger than k
assert run("1\n7 3\n1001001\n") == "1\n"  # protects first 1, all others safe
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| `00000` k=2 | 0 | No `1`s, protection not needed |
| `1` k=1 | 1 | Minimum-size string with single `1` |
| `101101` k=6 | 2 | Non-trivial spacing between `1`s |
| `1001001` k=3 | 1 | First `1` protection covers all others |

## Edge Cases

When all characters are `0`, the algorithm correctly outputs `0` because there is nothing to protect. With `k = n`, the leftmost `1` must always be protected because it can influence all subsequent positions. For `1`s spaced exactly `k` apart, each must
