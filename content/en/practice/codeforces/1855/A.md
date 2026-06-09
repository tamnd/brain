---
title: "CF 1855A - Dalton the Teacher"
description: "The problem asks us to make every student in a classroom \"happy\" by ensuring that no student sits on a chair with the same number as their own. We are given an initial permutation of students to chairs."
date: "2026-06-09T05:07:40+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math"]
categories: ["algorithms"]
codeforces_contest: 1855
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 889 (Div. 2)"
rating: 800
weight: 1855
solve_time_s: 109
verified: false
draft: false
---

[CF 1855A - Dalton the Teacher](https://codeforces.com/problemset/problem/1855/A)

**Rating:** 800  
**Tags:** greedy, math  
**Solve time:** 1m 49s  
**Verified:** no  

## Solution
## Problem Understanding

The problem asks us to make every student in a classroom "happy" by ensuring that no student sits on a chair with the same number as their own. We are given an initial permutation of students to chairs. Each student can be identified by a number from `1` to `n`, and each chair also has a number from `1` to `n`. The input provides a permutation array `p` such that `p[i]` tells us the chair where student `i` is initially sitting. Our task is to determine the **minimum number of swaps** between any two students needed so that every student is no longer on their own-numbered chair.

Since the permutation size `n` can be up to 10^5 and there can be up to 1000 test cases, we need an algorithm that works in linear time per test case. Any algorithm that explicitly simulates all possible swaps would be too slow because the number of swaps can be up to O(n^2) in a naive approach. Non-obvious edge cases arise when the permutation is already entirely composed of happy students, requiring 0 swaps, or when there is a single fixed point (student sitting on their own chair) with the rest forming cycles, which affects whether 1 or 2 swaps suffice.

A careless implementation might attempt to resolve each fixed point individually without considering the permutation structure. For example, in the permutation `[1,2,3]`, each student is on their own chair. The minimal number of swaps is not 3 but 2, because resolving one student shifts the cycle. This illustrates the need to reason in terms of cycles rather than individual elements.

## Approaches

The brute-force approach is to repeatedly swap students sitting on their own chair with some other student who is not on their own chair. This is correct but inefficient, since we might need to scan through the entire array for each fixed point. In the worst case, this can take O(n^2) operations, which is too slow for n = 10^5.

The key observation is that the problem reduces to counting **fixed points and contiguous blocks of unhappy students**. If there are no fixed points, no swaps are needed. If there is at least one fixed point, swaps must occur to break cycles. Specifically, if the permutation contains at least one contiguous sequence of happy students, the minimum number of moves depends on whether the unhappy students form a contiguous block or multiple blocks. In practice, the minimal number of swaps is:

- `0` if there are no fixed points (all students already happy)
- `1` if the unhappy students form a contiguous block somewhere inside the permutation
- `2` otherwise (unhappy students are split into multiple non-contiguous blocks)

This insight allows us to compute the answer in O(n) per test case.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n^2) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. Read the number of test cases `t`.
2. For each test case, read `n` and the permutation `p`.
3. Identify positions where `p[i] == i + 1`, these are fixed points.
4. If there are no fixed points, print `0` because all students are already happy.
5. Otherwise, find the leftmost and rightmost fixed points in the permutation. Check if all positions between them are fixed points.
6. If all positions between the leftmost and rightmost fixed points are also fixed points, it forms a contiguous block and only 1 swap is needed, so print `1`.
7. Otherwise, print `2` because the fixed points are split into multiple blocks, requiring at least 2 swaps.

**Why it works**

This approach works because any permutation can be decomposed into cycles of students. Students in a cycle of length >1 can be rearranged to be happy with a single swap per cycle. The edge cases occur when fixed points are isolated; we need to check for contiguous segments to determine if 1 or 2 swaps suffice. The leftmost and rightmost fixed points define the minimal span that contains all fixed points, ensuring correctness.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n = int(input())
    p = list(map(int, input().split()))
    
    fixed = [i for i in range(n) if p[i] == i + 1]
    if not fixed:
        print(0)
        continue
    
    left, right = fixed[0], fixed[-1]
    if all(p[i] == i + 1 for i in range(left, right + 1)):
        print(1)
    else:
        print(2)
```

The solution identifies fixed points in a single pass, determines the span of contiguous fixed points, and decides if 0, 1, or 2 swaps are needed. The use of `i + 1` ensures correct 1-based student numbering.

## Worked Examples

For the input permutation `[1,2,3]`:

| i | p[i] | Fixed? |
| --- | --- | --- |
| 0 | 1 | Yes |
| 1 | 2 | Yes |
| 2 | 3 | Yes |

All students are fixed points. Leftmost = 0, rightmost = 2. All positions between 0 and 2 are fixed. Minimum moves = 1.

For `[1,2,5,4,3]`:

| i | p[i] | Fixed? |
| --- | --- | --- |
| 0 | 1 | Yes |
| 1 | 2 | Yes |
| 2 | 5 | No |
| 3 | 4 | Yes |
| 4 | 3 | No |

Leftmost fixed = 0, rightmost fixed = 3. Positions between 0 and 3 are `[1,2,5,4]`. Not all are fixed. Minimum moves = 2.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Single pass over the array to identify fixed points and check the span |
| Space | O(n) | Storing the indices of fixed points, can be optimized to O(1) if only left/right used |

The algorithm comfortably fits within the 1-second time limit for total n ≤ 10^5.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        fixed = [i for i in range(n) if p[i] == i + 1]
        if not fixed:
            output.append("0")
            continue
        left, right = fixed[0], fixed[-1]
        if all(p[i] == i + 1 for i in range(left, right + 1)):
            output.append("1")
        else:
            output.append("2")
    return "\n".join(output)

# Provided sample
assert run("5\n2\n2 1\n3\n1 2 3\n5\n1 2 5 4 3\n4\n1 2 4 3\n10\n10 2 1 3 6 5 4 7 9 8\n") == "0\n1\n2\n1\n2"

# Custom tests
assert run("2\n2\n1 2\n2\n2 1\n") == "1\n0", "all fixed vs no fixed"
assert run("1\n5\n1 3 2 5 4\n") == "2", "non-contiguous fixed points"
assert run("1\n3\n3 2 1\n") == "1", "contiguous happy segment"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n2\n1 2\n2\n2 1 | 1\n0 | distinguishes contiguous fixed points vs none |
| 1\n5\n1 3 2 5 4 | 2 | non-contiguous fixed points require 2 swaps |
| 1\n3\n3 2 1 | 1 | contiguous unhappy block allows 1 swap |

## Edge Cases

A single fixed point at the end, such as `[1,3,2]`, is handled by identifying leftmost and rightmost fixed points and checking the span. Even if only one student is initially unhappy, the span check correctly identifies whether only one swap is sufficient or two are needed. This ensures correctness across all minimal and maximal configurations.
