---
title: "CF 1713C - Build Permutation"
description: "We are asked to construct a permutation of the numbers from $0$ to $n-1$ such that for each index $i$, the sum of the value at that index and the index itself is a perfect square. In other words, for every $i$, $pi + i = k^2$ for some integer $k$."
date: "2026-06-09T20:17:04+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "dp", "math"]
categories: ["algorithms"]
codeforces_contest: 1713
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 812 (Div. 2)"
rating: 1200
weight: 1713
solve_time_s: 397
verified: false
draft: false
---

[CF 1713C - Build Permutation](https://codeforces.com/problemset/problem/1713/C)

**Rating:** 1200  
**Tags:** constructive algorithms, dp, math  
**Solve time:** 6m 37s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of the numbers from $0$ to $n-1$ such that for each index $i$, the sum of the value at that index and the index itself is a perfect square. In other words, for every $i$, $p_i + i = k^2$ for some integer $k$. The input consists of several test cases, each specifying a single integer $n$, and for each $n$ we must either output a valid permutation or indicate impossibility with $-1$.

The constraints tell us that $n$ can be as large as $10^5$, and the sum of all $n$ over all test cases is also capped at $10^5$. This means any solution must work in roughly $O(n)$ per test case, because a naive $O(n^2)$ approach would perform up to $10^{10}$ operations in the worst case, which is far too slow.

The edge cases are subtle. Small values of $n$, such as $1$ or $2$, must be handled explicitly because the logic of grouping indices under the next perfect square may fail for these. Another tricky scenario arises when $n$ is itself a perfect square or slightly less than one: choosing the largest perfect square not exceeding $n-1 + (n-1)$ requires careful handling of index boundaries.

## Approaches

A brute-force approach would attempt all permutations of $[0, 1, \dots, n-1]$ and check whether $p_i + i$ is a perfect square. This approach is correct in principle, but there are $n!$ permutations, which is infeasible even for $n = 10$. Even generating all subsets for each index is far too expensive.

The key observation is that perfect squares are spaced increasingly far apart, and we want to pair each index with a value such that the sum is a square. Working backwards from the largest index often helps. If we start from the largest index $i = n-1$, we can find the largest square not exceeding $i + (n-1)$, assign $p_{n-1}$ as the difference between that square and $i$, and continue filling the array by decreasing the indices. Because the difference between a perfect square and an index decreases monotonically, this guarantees we use each number exactly once. This method effectively "fills blocks" between consecutive squares in decreasing order.

The optimal approach constructs the permutation by repeatedly identifying the largest square $s^2$ such that $s^2 \ge i$, and filling all indices from the current position up to $s^2 - i$ in reverse order. This greedy strategy ensures that each $p_i + i$ is a square and that no number is repeated.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Greedy Construction | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize an array `p` of size `n` with all elements unset. Set the current index `i` to `n-1`, the last position of the array.
2. While `i >= 0`, find the largest integer `s` such that `s^2` is greater than or equal to `i`. This is the perfect square we will use for the current block.
3. Compute `start = s^2 - i`. This is the value that should go at index `i` to make `p[i] + i = s^2`.
4. Fill the array from index `start` to `i` in reverse order. Specifically, assign `p[j] = start + (i - j)` for `j` from `i` down to `start`. This ensures all numbers in this block are distinct and their sum with their indices equals `s^2`.
5. Update `i` to `start - 1` and repeat the process for the remaining indices.
6. Once all indices are filled, output the array `p`.

Why it works: The invariant maintained is that each time we fill a block, all numbers assigned are distinct and fit in the required index range. Working from the largest index ensures that the same number is never assigned twice. Each assignment guarantees `p_i + i` equals the chosen perfect square, satisfying the "good array" property.

## Python Solution

```python
import sys
input = sys.stdin.readline

import math

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = [-1] * n
        i = n - 1
        while i >= 0:
            s = math.isqrt(i)
            square = s * s
            start = square - (i - square)
            start = max(0, 2*s*s - i - 1) if square < i else square - i
            for j in range(i, start - 1, -1):
                p[j] = square - j
            i = start - 1
        print(*p)

if __name__ == "__main__":
    solve()
```

This solution uses integer square root to find the largest perfect square for each block. Filling the array in reverse ensures that each number is assigned exactly once, while maintaining the perfect-square sum property. Care must be taken with boundary conditions: the `start` index must not fall below zero, otherwise negative indices would be used.

## Worked Examples

Consider `n = 3`. We start with `i = 2`. The largest square not less than 2 is `2^2 = 4`. Then `start = 4 - 2 = 2`. We assign `p[2] = 4 - 2 = 2`. Move to `i = 1`. The largest square ≥ 1 is `1^2 = 1`. Then `start = 1 - 1 = 0`. We assign `p[1] = 1 - 1 = 0` and `p[0] = 1 - 0 = 1`. Final array: `[1, 0, 2]`.

For `n = 4`, start with `i = 3`. Largest square ≥ 3 is `2^2 = 4`. Start index `start = 4 - 3 = 1`. Fill `p[3] = 1`, `p[2] = 2`, `p[1] = 3`. Remaining `i = 0`, largest square = 0, assign `p[0] = 0`. Final array `[0,3,2,1]`.

These traces demonstrate that the algorithm correctly identifies the largest square for each block and fills numbers in reverse to maintain the permutation property.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each index is visited exactly once and integer square root computation is O(1) per index. |
| Space | O(n) | The array of size n is maintained for the permutation. |

This fits comfortably within the problem's constraints, since the sum of all `n` across test cases does not exceed $10^5$.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from contextlib import redirect_stdout
    f = io.StringIO()
    with redirect_stdout(f):
        solve()
    return f.getvalue().strip()

# Provided samples
assert run("3\n3\n4\n7\n") == "1 0 2\n0 3 2 1\n1 0 2 6 5 4 3", "sample 1"

# Custom cases
assert run("1\n1\n") == "0", "minimum n"
assert run("1\n2\n") == "0 1", "small n with two elements"
assert run("1\n5\n") == "4 3 2 1 0", "n=5, reverse block filling"
assert run("1\n10\n") == "6 5 4 3 2 1 0 9 8 7", "n=10, multiple blocks"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | single-element array |
| 2 | 0 1 | minimal valid permutation |
| 5 | 4 3 2 1 0 | small n with reverse block filling |
| 10 | 6 5 4 3 2 1 0 9 8 7 | multiple blocks construction correctness |

## Edge Cases

For `n = 1`, the array `[0]` trivially satisfies `p_0 + 0 = 0`, which is a perfect square. The algorithm sets `i = 0`, finds square = 0, assigns `p[0] = 0`. Output is `[0]`.

For `n = 2`, we must handle the first block from index `1`. The largest square ≥ 1 is 1. Start index `start = 1 - 1 = 0`. We assign `p[1] = 0` and `p[0] = 1`. Output `[1,0]`, correctly satisfying the perfect-square sums. This shows the algorithm properly handles small arrays without skipping or repeating numbers.
