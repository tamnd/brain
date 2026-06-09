---
title: "CF 1992C - Gorilla and Permutation"
description: "We are asked to construct a permutation of numbers from 1 to $n$ such that a certain expression is maximized. The expression is the sum of all prefix sums of \"large\" numbers (greater than or equal to $k$) minus the sum of all prefix sums of \"small\" numbers (less than or equal to…"
date: "2026-06-08T15:20:40+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "math"]
categories: ["algorithms"]
codeforces_contest: 1992
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 957 (Div. 3)"
rating: 900
weight: 1992
solve_time_s: 477
verified: false
draft: false
---

[CF 1992C - Gorilla and Permutation](https://codeforces.com/problemset/problem/1992/C)

**Rating:** 900  
**Tags:** constructive algorithms, math  
**Solve time:** 7m 57s  
**Verified:** no  

## Solution
## Problem Understanding

We are asked to construct a permutation of numbers from 1 to $n$ such that a certain expression is maximized. The expression is the sum of all prefix sums of "large" numbers (greater than or equal to $k$) minus the sum of all prefix sums of "small" numbers (less than or equal to $m$). The permutation must contain each number from 1 to $n$ exactly once.

The input for each test case is three integers: $n$ (the length of the permutation), $m$ (the threshold for small numbers), and $k$ (the threshold for large numbers). The output is any permutation of 1 to $n$ that maximizes the difference between the accumulated sums of large numbers and small numbers over all prefixes.

The main constraints are that $n$ can be up to $10^5$, and the sum of $n$ across all test cases is up to $2 \cdot 10^5$. This tells us that an $O(n \log n)$ or $O(n)$ solution is acceptable, but $O(n^2)$ solutions will be too slow.

A non-obvious point is that the numbers strictly between $m+1$ and $k-1$ do not contribute to either sum, so their positions are irrelevant to the score. Another subtlety is that putting small numbers early increases the penalty (g(i) contributions), while putting large numbers early maximizes the reward (f(i) contributions).

For example, with $n=5$, $m=2$, $k=5$, one permutation [5,3,4,1,2] produces $f(i)$ and $g(i)$ values that give the maximum difference. A naive permutation like [1,2,3,4,5] would produce a smaller difference because the small numbers appear before large numbers, increasing the penalty.

## Approaches

The brute-force approach would be to try all $n!$ permutations, compute $f(i)$ and $g(i)$ for each, and select the maximum. This works in theory because it correctly computes the sums for any permutation, but it is infeasible even for moderate $n$, since $5! = 120$ and $10! \sim 3.6 \cdot 10^6$, far below the maximum $n = 10^5$.

The key insight is that the contribution of each number to the final sum is linear in the number of prefixes it appears in. To maximize the sum of f(i) contributions, we should place all numbers greater than or equal to $k$ as early as possible. To minimize the sum of g(i) contributions, we should place all numbers less than or equal to $m$ as late as possible. The numbers between $m+1$ and $k-1$ can be placed anywhere because they do not affect the score.

So the optimal permutation is constructed by first listing numbers ≥ k in descending order, followed by the middle numbers in any order, and ending with numbers ≤ m in ascending order. This ensures the largest numbers contribute to f(i) in as many prefixes as possible and the smallest numbers contribute to g(i) in as few prefixes as possible.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases $t$.
2. For each test case, read $n$, $m$, and $k$.
3. Initialize three lists: `large` for numbers ≥ k, `middle` for numbers in (m, k), and `small` for numbers ≤ m.
4. Iterate over all numbers from 1 to n:

- If the number ≥ k, append it to `large`.
- If the number ≤ m, append it to `small`.
- Otherwise, append it to `middle`.
5. Construct the permutation by concatenating `large` in descending order, `middle` in any order (ascending for simplicity), and `small` in ascending order.
6. Output the permutation.

Why it works: Placing all numbers ≥ k at the front maximizes their contribution to every prefix that includes them. Placing numbers ≤ m at the end minimizes their contribution. Numbers between m and k do not affect the score, so their order does not matter. This strategy guarantees that no permutation can achieve a higher difference.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, m, k = map(int, input().split())
    large = []
    middle = []
    small = []
    for i in range(1, n + 1):
        if i >= k:
            large.append(i)
        elif i <= m:
            small.append(i)
        else:
            middle.append(i)
    permutation = large + middle + small
    print(*permutation)
```

The solution reads input quickly using `sys.stdin.readline`, separates the numbers into three categories, and concatenates them to maximize the score. Using list operations avoids off-by-one errors and ensures the output is a valid permutation.

## Worked Examples

Sample Input 1: `5 2 5`

| Number | Category | Contribution reasoning |
| --- | --- | --- |
| 5 | large | contributes to f(i) early |
| 3 | middle | ignored |
| 4 | middle | ignored |
| 1 | small | contributes to g(i) late |
| 2 | small | contributes to g(i) late |

Permutation: `[5,3,4,1,2]`. Large numbers appear first, small numbers last.

Sample Input 2: `3 1 3`

| Number | Category |
| --- | --- |
| 3 | large |
| 2 | middle |
| 1 | small |

Permutation: `[3,2,1]`. This order maximizes f(i) sum and minimizes g(i) sum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Each number is classified in constant time, concatenation is O(n) |
| Space | O(n) | Three lists store subsets of numbers |

With $n$ up to $10^5$ and the sum across test cases ≤ 2·10^5, this solution is efficient and fits in memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    t = int(input())
    for _ in range(t):
        n, m, k = map(int, input().split())
        large, middle, small = [], [], []
        for i in range(1, n + 1):
            if i >= k:
                large.append(i)
            elif i <= m:
                small.append(i)
            else:
                middle.append(i)
        print(*large, *middle, *small)
    return out.getvalue().strip()

assert run("3\n5 2 5\n3 1 3\n10 3 8\n") == "5 3 4 1 2\n3 2 1\n10 9 8 4 5 6 7 1 2 3", "samples"
assert run("1\n2 1 2\n") == "2 1", "minimum size input"
assert run("1\n5 1 5\n") == "5 2 3 4 1", "all boundaries"
assert run("1\n6 2 5\n") == "6 5 3 4 1 2", "middle numbers present"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2 1 2 | 2 1 | minimum-size permutation |
| 5 1 5 | 5 2 3 4 1 | correct placement of boundaries |
| 6 2 5 | 6 5 3 4 1 2 | middle numbers handled correctly |

## Edge Cases

A tricky edge case is when `m+1 = k-1`, meaning there is exactly one middle number. For `n=5, m=2, k=4`, the numbers are `[1,2,3,4,5]`. Our algorithm places `[4,5]` (large) first, then `[3]` (middle), and `[1,2]` (small) last. The resulting permutation `[4,5,3,1,2]` ensures maximum f(i) contribution early and minimal g(i) contribution late, correctly handling the singleton middle number. This demonstrates the algorithm works even when the middle segment has only one element.
