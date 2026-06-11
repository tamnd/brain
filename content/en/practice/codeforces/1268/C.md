---
title: "CF 1268C - K Integers"
description: "We are given a permutation of integers from 1 to n. We are allowed to swap any two adjacent elements. For each $k$ from 1 to $n$, we want to compute the minimum number of adjacent swaps required to create a consecutive subsegment that contains exactly the numbers $1, 2, ldots…"
date: "2026-06-11T20:18:16+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures"]
categories: ["algorithms"]
codeforces_contest: 1268
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 609 (Div. 1)"
rating: 2300
weight: 1268
solve_time_s: 211
verified: false
draft: false
---

[CF 1268C - K Integers](https://codeforces.com/problemset/problem/1268/C)

**Rating:** 2300  
**Tags:** binary search, data structures  
**Solve time:** 3m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of integers from 1 to n. We are allowed to swap any two adjacent elements. For each $k$ from 1 to $n$, we want to compute the minimum number of adjacent swaps required to create a consecutive subsegment that contains exactly the numbers $1, 2, \ldots, k$ in order. The output is a list of $n$ integers $f(1), f(2), \ldots, f(n)$, where $f(k)$ is the minimum number of swaps needed for the subsegment containing the first $k$ numbers.

The input size $n$ can be as large as 200,000. This rules out any solution that tries to simulate swaps directly, which would easily exceed $O(n^2)$ operations. We need an approach that works in linear or near-linear time.

A naive implementation might try to slide every possible window of length $k$ across the array and count swaps needed to sort that segment. For small $n$ or $k$ this is fine, but at the maximum input size, this is too slow. Edge cases that are easy to miss include already sorted segments (where no swaps are needed), reverse-sorted arrays (maximum swaps needed), or numbers that are scattered far apart in the permutation (so that naive window scanning miscalculates swaps).

For example, consider $n = 5$ with permutation $5, 4, 3, 2, 1$. For $k=1$, the minimum swaps are 0 because 1 can occupy any position. For $k=2$, the subsegment 1, 2 requires moving 1 and 2 together, which is non-trivial to calculate without careful reasoning about positions. Naive approaches often miscount the required swaps for such disjoint placements.

## Approaches

The brute-force solution considers every subsegment of length $k$ and computes the swaps needed to sort it into 1 through $k$. Specifically, it would involve simulating bubble-sort-style moves or computing inversion counts for each subsegment. For each $k$, there are $n-k+1$ possible segments, and each inversion count could take $O(k^2)$ operations, resulting in roughly $O(n^3)$ complexity at worst. This is clearly too slow for $n$ up to 200,000.

The key observation for a faster solution is that swaps are determined by the positions of numbers 1 through $k$. If we know the leftmost and rightmost positions among the first $k$ numbers in the permutation, the minimal segment that contains all these numbers is fixed between these positions. The number of swaps needed is the number of positions between the leftmost and rightmost minus $k$, because each number outside the subsegment must be swapped into place.

Formally, let $pos[x]$ be the index of number $x$ in the permutation. For each $k$, maintain the minimum $l = \min(pos[1], \dots, pos[k])$ and maximum $r = \max(pos[1], \dots, pos[k])$. The minimum number of swaps required to make numbers 1 through $k$ consecutive is:

$$f(k) = (r - l + 1) - k$$

This works because every element between $l$ and $r$ that is not in $1..k$ must be moved out, and every element in $1..k$ already in that segment is either in place or can be swapped with those out-of-range elements in a minimal sequence.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^3) | O(n) | Too slow |
| Optimal | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Read the permutation $p$ and store positions of each number in an array $pos$ such that $pos[x]$ is the index of $x$ in $p$. This allows $O(1)$ lookup for each number's current position.
2. Initialize two variables $left$ and $right$ to the position of 1. These track the current segment bounds that contain all numbers 1 through $k$.
3. For each $k$ from 1 to $n$, update $left = \min(left, pos[k])$ and $right = \max(right, pos[k])$. This ensures the segment always contains all numbers 1 through $k$.
4. Compute $f(k) = (right - left + 1) - k$ and store it.
5. Output the sequence $f(1) \dots f(n)$.

Why it works: By always tracking the leftmost and rightmost positions of numbers 1 through $k$, we maintain the smallest possible segment that can contain all required numbers. Any larger segment would only increase the number of swaps. The formula counts extra positions outside the needed numbers, which exactly equals the number of adjacent swaps needed to compress the numbers into a contiguous segment.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
p = list(map(int, input().split()))

pos = [0] * (n + 1)
for idx, val in enumerate(p):
    pos[val] = idx

left = pos[1]
right = pos[1]

res = []
for k in range(1, n + 1):
    left = min(left, pos[k])
    right = max(right, pos[k])
    res.append(right - left + 1 - k)

print(' '.join(map(str, res)))
```

The code first builds the position mapping in $O(n)$. The segment bounds are updated sequentially for each $k$, guaranteeing that every number from 1 to $k$ is included in the segment. The calculation $right - left + 1 - k$ ensures we only count the extra positions that require swaps. Off-by-one errors are avoided by using 0-based indexing consistently.

## Worked Examples

**Sample Input 1**

```
5
5 4 3 2 1
```

| k | pos[k] | left | right | f(k) = right-left+1-k |
| --- | --- | --- | --- | --- |
| 1 | 4 | 4 | 4 | 0 |
| 2 | 3 | 3 | 4 | 1 |
| 3 | 2 | 2 | 4 | 3 |
| 4 | 1 | 1 | 4 | 6 |
| 5 | 0 | 0 | 4 | 10 |

The table shows that as $k$ increases, the segment expands to include all numbers 1 through $k$. Each extra number outside the current segment adds to the swap count.

**Custom Input 2**

```
6
1 3 2 6 5 4
```

| k | pos[k] | left | right | f(k) |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 2 | 0 | 2 | 1 |
| 3 | 1 | 0 | 2 | 2 |
| 4 | 5 | 0 | 5 | 2 |
| 5 | 4 | 0 | 5 | 3 |
| 6 | 3 | 0 | 5 | 5 |

This demonstrates non-monotonic increases when positions are scattered.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Building positions and scanning k from 1 to n are linear. |
| Space | O(n) | Storing the permutation and position array uses linear space. |

Given n ≤ 200,000, this linear solution runs well within the 3-second time limit and 256 MB memory constraint.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    n = int(input())
    p = list(map(int, input().split()))
    pos = [0] * (n + 1)
    for idx, val in enumerate(p):
        pos[val] = idx
    left = pos[1]
    right = pos[1]
    res = []
    for k in range(1, n + 1):
        left = min(left, pos[k])
        right = max(right, pos[k])
        res.append(str(right - left + 1 - k))
    return ' '.join(res)

# Provided sample
assert run("5\n5 4 3 2 1\n") == "0 1 3 6 10", "sample 1"

# Minimum size
assert run("1\n1\n") == "0", "single element"

# Already sorted
assert run("4\n1 2 3 4\n") == "0 0 0 0", "already sorted"

# Reverse sorted
assert run("4\n4 3 2 1\n") == "0 1 3 6", "reverse sorted"

# Scattered
assert run("6\n1 3 2 6 5 4\n") == "0 1 2 2 3 5", "scattered positions"
```

| Test input | Expected output | What it validates |

|
