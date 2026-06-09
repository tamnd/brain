---
title: "CF 2008C - Longest Good Array"
description: "We are asked to construct an array of integers between two given bounds, l and r, such that the array is strictly increasing and the differences between consecutive elements are also strictly increasing. Our goal is to find the maximum possible length of such an array."
date: "2026-06-08T13:22:51+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "math"]
categories: ["algorithms"]
codeforces_contest: 2008
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 970 (Div. 3)"
rating: 800
weight: 2008
solve_time_s: 84
verified: true
draft: false
---

[CF 2008C - Longest Good Array](https://codeforces.com/problemset/problem/2008/C)

**Rating:** 800  
**Tags:** binary search, brute force, math  
**Solve time:** 1m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to construct an array of integers between two given bounds, `l` and `r`, such that the array is strictly increasing and the differences between consecutive elements are also strictly increasing. Our goal is to find the maximum possible length of such an array. Each test case gives us a pair `(l, r)`, and we must output a single integer for that case: the length of the longest "good array" that fits within the bounds.

The problem constraints allow `l` and `r` to be as large as $10^9$, and there can be up to $10^4$ test cases. This rules out any solution that iteratively builds all possible arrays or checks all combinations between `l` and `r`. Even $O((r-l)^2)$ approaches would be too slow, because `r-l` could be up to $10^9$. We need a method that computes the maximum length using arithmetic properties, not enumeration.

A subtle edge case arises when `l` equals `r`. In that situation, the only possible array is `[l]`, so the answer is `1`. Another tricky scenario is when `r - l` is very small, allowing only arrays of length `2` at most. Careless algorithms that assume the array can always grow beyond two elements would fail here. For example, `(l=1, r=2)` only allows `[1,2]` even though the pattern might suggest longer arrays.

## Approaches

The brute-force approach would be to start from `l`, try all increasing differences, and continue adding elements until reaching `r`. This works because we could simulate the "good array" rules directly, but it becomes impractical when `r-l` is large, as the number of potential sequences grows combinatorially. In the worst case, iterating through all possibilities would take time proportional to the number of subsets of `[l..r]`, which is astronomical.

The key insight for an optimal solution comes from observing the nature of the differences. Suppose the first element is `x_1 = l`. To maximize the array length, the differences should grow minimally at each step: start with `1` for the first difference, then `2` for the next, and so on. This gives a sequence of the form `l, l+1, l+1+2, l+1+2+3, ...` or in general `l + 1 + 2 + ... + k`. The sum of the first `k` natural numbers is `k*(k+1)/2`. Thus, the maximal `k` we can fit within `[l, r]` satisfies `l + k*(k+1)/2 - 1 ≤ r`.

This reduces the problem to solving a quadratic inequality for each test case. The approach is fast because computing the largest `k` that satisfies the inequality can be done in constant time using the formula for triangular numbers or via binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O((r-l)^2) | O(r-l) | Too slow |
| Optimal | O(1) per test case | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read the bounds `l` and `r`. The first element of our array will be `l`.
2. Initialize a variable `length` to `1` to account for the first element.
3. Compute the remaining range available: `remaining = r - l`.
4. The sum of differences to extend the array by `k` additional elements is `1 + 2 + ... + k = k*(k+1)/2`. We need the largest integer `k` such that `k*(k+1)/2 ≤ remaining`.
5. Solve for `k` using integer arithmetic. One way is binary search between `0` and `√(2*remaining)`. Another is the quadratic formula `k = floor((-1 + sqrt(1 + 8*remaining))/2)`.
6. Add `k` to `length`. Output `length`.

Why it works: at each step, choosing the smallest possible next difference guarantees we can extend the array as far as possible before exceeding `r`. Increasing the first difference or skipping numbers would reduce the maximum length. The formula `k*(k+1)/2 ≤ remaining` captures exactly how many steps fit in the allowed range.

## Python Solution

```python
import sys, math
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    l, r = map(int, input().split())
    remaining = r - l
    # Solve k*(k+1)/2 <= remaining
    k = int((-1 + math.isqrt(1 + 8*remaining)) // 2)
    print(k + 1)
```

The solution reads multiple test cases, computes the remaining range after placing the first element, and solves the triangular number inequality. `math.isqrt` ensures exact integer square roots without floating-point rounding errors. Adding `1` accounts for the initial element `l`.

## Worked Examples

### Example 1

Input: `l=1, r=5`

| Step | Remaining | k*(k+1)/2 ≤ Remaining | k | Length |
| --- | --- | --- | --- | --- |
| 1 | 4 | 1+2=3 ≤ 4 | 2 | 3 |

Sequence: `[1, 2, 4]` or `[1,2,5]`. Max length is `3`.

### Example 2

Input: `l=10, r=20`

| Step | Remaining | k*(k+1)/2 ≤ Remaining | k | Length |
| --- | --- | --- | --- | --- |
| 1 | 10 | 1+2+3+4=10 ≤ 10 | 4 | 5 |

Sequence: `[10,11,13,16,20]`. Max length is `5`.

These traces confirm that the formula captures the maximal number of steps without violating the upper bound.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(1) per test case | Calculating integer square root and simple arithmetic takes constant time. |
| Space | O(1) | No arrays or extra storage are needed; only a few integers per test case. |

Even for `t = 10^4` and `r-l = 10^9`, the algorithm runs comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        l, r = map(int, input().split())
        remaining = r - l
        k = int((-1 + math.isqrt(1 + 8*remaining)) // 2)
        output.append(str(k+1))
    return "\n".join(output)

# Provided samples
assert run("5\n1 2\n1 5\n2 2\n10 20\n1 1000000000\n") == "2\n3\n1\n5\n44721", "samples"

# Custom test cases
assert run("1\n1 1\n") == "1", "single element array"
assert run("1\n100 101\n") == "2", "minimum extension"
assert run("1\n1 3\n") == "2", "small range"
assert run("1\n1 10\n") == "4", "medium range"
assert run("1\n1 15\n") == "5", "exact triangular number"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 | 1 | handles `l=r` |
| 100 101 | 2 | minimal possible extension |
| 1 3 | 2 | small range with max length 2 |
| 1 10 | 4 | medium range, ensures formula computes k correctly |
| 1 15 | 5 | triangular number exact fit |

## Edge Cases

When `l=r`, the algorithm sets `remaining = 0` and computes `k=0`, yielding length `1`. For `r-l=1`, the formula gives `k=1`, resulting in length `2`. The integer square root ensures we never overshoot `k*(k+1)/2 > remaining`. In all cases, the algorithm produces the correct maximal length, confirmed by tracing both minimal and maximal ranges.
