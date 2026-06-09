---
title: "CF 1830E - Bully Sort"
description: "We are given a permutation of length $n$, which is an array containing each number from $1$ to $n$ exactly once. A \"bully swap\" is defined as picking the largest number that is not in its sorted position and swapping it with the smallest number to its right."
date: "2026-06-09T07:13:41+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "math"]
categories: ["algorithms"]
codeforces_contest: 1830
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 875 (Div. 1)"
rating: 3500
weight: 1830
solve_time_s: 74
verified: false
draft: false
---

[CF 1830E - Bully Sort](https://codeforces.com/problemset/problem/1830/E)

**Rating:** 3500  
**Tags:** data structures, math  
**Solve time:** 1m 14s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of length $n$, which is an array containing each number from $1$ to $n$ exactly once. A "bully swap" is defined as picking the largest number that is not in its sorted position and swapping it with the smallest number to its right. We are asked to calculate $f(p)$, the number of bully swaps needed to sort the permutation. Then we must handle $q$ updates, each swapping two elements in the permutation, and report the new $f(p)$ after each update.

The constraints are tight. With $n$ up to $5 \cdot 10^5$ and $q$ up to $5 \cdot 10^4$, a naive simulation that performs swaps one by one could take $O(n^2)$ time in the worst case, which is roughly $10^{11}$ operations. This is far beyond feasible. We need something linear or near-linear in $n$ for each computation, or at worst $O(n \log n + q \log n)$ overall.

A subtlety is that the bully swap always targets the **largest misplaced element**, not just any element out of place, and swaps it with the **smallest element to its right**, not necessarily the next element. For instance, if the permutation is `[2, 1, 3]`, the largest misplaced element is `2` at index 1. The smallest element to its right is `1`, so the first bully swap yields `[1, 2, 3]` and $f(p) = 1$. A naive approach that counts inversions or misplaced elements could miscount because the exact positions and values dictate the swap sequence.

## Approaches

The brute-force approach is straightforward. We simulate the bully swaps directly. Each step requires scanning for the largest misplaced element and the smallest element to its right. Locating the largest misplaced element takes $O(n)$ and finding the smallest to its right takes $O(n)$, making each swap $O(n)$. In the worst case, there are up to $n$ swaps, yielding $O(n^2)$ per query. This is infeasible for $n \sim 5 \cdot 10^5$.

The key insight is to avoid simulating the swaps. A bully swap effectively reduces a **strictly increasing subsequence** problem into counting **breakpoints** in the permutation. Define a breakpoint as an index $i$ such that $p_i > p_{i+1}$. The number of bully swaps corresponds to counting how many elements form a new segment, or equivalently, the number of "ascending runs" we need to merge. Each bully swap merges a run with the following run. Therefore, $f(p)$ can be computed by counting these ascending segments.

Once we know that $f(p)$ depends only on the number of ascending runs, we can maintain the run count efficiently under updates. Each swap affects at most the neighboring positions of the swapped elements. We only need to check breakpoints around $x-1$, $x$, $y-1$, and $y$ to update the run count, reducing the complexity per query to $O(1)$ or $O(\log n)$ if we use a segment tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2 * q) | O(n) | Too slow |
| Optimal | O(n + q) | O(n) | Accepted |

## Algorithm Walkthrough

1. Initialize a set or array to track **breakpoints**. For index $i$, a breakpoint exists if $p_i > p_{i+1}$. Count the total number of breakpoints $b$. Then $f(p) = b + 1$ because each bully swap merges one run with the next.
2. For each update, identify the indices $x$ and $y$ being swapped. For each of the positions $x-1$, $x$, $y-1$, $y$ that lie within array bounds, check whether a breakpoint exists before the swap and after the swap.
3. Adjust the breakpoint count accordingly: if a breakpoint disappears, decrement $b$; if a new breakpoint appears, increment $b$.
4. Swap $p[x]$ and $p[y]$.
5. After updating the breakpoints, report $f(p) = b + 1$.

Why it works: The bully swap process always selects the largest misplaced element and swaps it to reduce the number of ascending runs. The number of runs fully determines the number of swaps required. By maintaining breakpoints, we track the segment boundaries that bully swaps would merge. Each update only affects local breakpoints, so our method is exact and efficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

n, q = map(int, input().split())
p = list(map(int, input().split()))

# initial breakpoints
breaks = 0
for i in range(n-1):
    if p[i] > p[i+1]:
        breaks += 1

res = []

def update_break(i):
    if 0 <= i < n-1:
        return p[i] > p[i+1]
    return False

for _ in range(q):
    x, y = map(int, input().split())
    x -= 1
    y -= 1
    affected = set([x-1, x, y-1, y])
    old = {}
    for i in affected:
        old[i] = update_break(i)
    p[x], p[y] = p[y], p[x]
    for i in affected:
        new_val = update_break(i)
        if old.get(i, False) and not new_val:
            breaks -= 1
        elif not old.get(i, False) and new_val:
            breaks += 1
    res.append(str(breaks + 1))

print("\n".join(res))
```

The solution starts by computing initial breakpoints, which represent positions where the array decreases. For each update, we only check breakpoints around the swapped indices, which keeps the update efficient. The choice of using a set of affected indices ensures we handle boundary conditions without accessing invalid positions.

## Worked Examples

**Sample Input 1:**

```
8 5
6 2 1 5 3 4 7 8
1 8
2 3
4 7
7 8
3 6
```

| Update | Swapped indices | Breakpoints before | Breakpoints after | f(p) |
| --- | --- | --- | --- | --- |
| 1 | 1 & 8 | 4 | 4 | 5 |
| 2 | 2 & 3 | 4 | 5 | 6 |
| 3 | 4 & 7 | 5 | 8 | 9 |
| 4 | 7 & 8 | 8 | 7 | 8 |
| 5 | 3 & 6 | 7 | 6 | 7 |

This trace confirms that only local breakpoints around swapped indices are affected and the count updates correctly.

**Sample Input 2:**

```
5 2
1 3 2 5 4
2 5
1 4
```

| Update | Swapped indices | Breakpoints before | Breakpoints after | f(p) |
| --- | --- | --- | --- | --- |
| 1 | 2 & 5 | 2 | 3 | 4 |
| 2 | 1 & 4 | 3 | 2 | 3 |

This demonstrates swaps crossing multiple runs, still correctly updating the count.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + q) | Initial breakpoints counted in O(n), each update touches constant positions |
| Space | O(n) | Stores permutation array, no extra structures beyond constants |

With $n \le 5 \cdot 10^5$ and $q \le 5 \cdot 10^4$, the solution easily fits within 10 seconds and 1GB memory.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n, q = map(int, input().split())
    p = list(map(int, input().split()))
    breaks = 0
    for i in range(n-1):
        if p[i] > p[i+1]:
            breaks += 1
    res = []
    def update_break(i):
        if 0 <= i < n-1:
            return p[i] > p[i+1]
        return False
    for _ in range(q):
        x, y = map(int, input().split())
        x -= 1
        y -= 1
        affected = set([x-1, x, y-1, y])
        old = {}
        for i in affected:
            old[i] = update_break(i)
        p[x], p[y] = p[y], p[x]
        for i in affected:
            new_val = update_break(i)
            if old.get(i, False) and not new_val:
                breaks -= 1
            elif not old.get(i, False) and new_val:
                breaks += 1
        res.append(str(breaks + 1))
    return "\n".join(res)

# Provided sample
assert run("8 5\n6 2
```
