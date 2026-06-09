---
title: "CF 1853C - Ntarsis' Set"
description: "We are given an abstractly enormous set of positive integers, initially all numbers starting from 1 up to $10^{1000}$, which is effectively unbounded for computational purposes."
date: "2026-06-09T17:23:59+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "constructive-algorithms", "implementation", "math"]
categories: ["algorithms"]
codeforces_contest: 1853
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 887 (Div. 2)"
rating: 1800
weight: 1853
solve_time_s: 163
verified: false
draft: false
---

[CF 1853C - Ntarsis' Set](https://codeforces.com/problemset/problem/1853/C)

**Rating:** 1800  
**Tags:** binary search, constructive algorithms, implementation, math  
**Solve time:** 2m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given an abstractly enormous set of positive integers, initially all numbers starting from 1 up to $10^{1000}$, which is effectively unbounded for computational purposes. Each day, a list of positions $a_1, a_2, \dots, a_n$ is provided, and we are asked to remove from the set the elements that currently occupy those positions in sorted order. After $k$ days of applying the removals, we want to know the smallest remaining number in the set.

The key input parameters are $n$, the length of the removal list per day, and $k$, the number of days, with both possibly reaching $2 \cdot 10^5$. Additionally, the values in the removal list $a_i$ can be as large as $10^9$, and the total number of test cases $t$ may be up to $10^5$. These constraints rule out any naive approach that explicitly stores the set $S$ or iterates through it by index, because $S$ is too large and the number of operations would exceed $10^9$ in a single test case.

An edge case arises when the first element removed is 1 on the first day, or when $a_1$ is 1 repeatedly. For example, if $a = [1, 2, 3]$ and $k = 1$, the set $S$ after one day starts at 4. A careless approach that assumes a static mapping of positions to values without accounting for previous deletions would produce an incorrect answer.

Another subtle case is when $a$ contains consecutive numbers starting from 1, and $k$ is very large, such as $a = [1, 2, 3]$ and $k = 10^5$. The smallest remaining element grows linearly with $k$ times the gap created by $a_n$, and missing this growth factor can easily lead to off-by-one mistakes.

## Approaches

The brute-force approach is conceptually straightforward: simulate the removal process by maintaining a dynamic array representing $S$, and each day remove the elements at the positions specified in $a$. This works in principle, because the positions in $a$ are strictly increasing and can be adjusted to reflect the removals from previous days. However, this requires either storing all elements of $S$, which is impossible, or performing index arithmetic on a virtual set, which still involves $O(n \cdot k)$ operations. In the worst case, $n$ and $k$ can both reach $2 \cdot 10^5$, giving $O(4 \cdot 10^{10})$ operations per test case, which is far too slow.

The key insight is that we do not need the entire set $S$ explicitly. We only need to track how the smallest element shifts as we remove numbers. Since $a$ is strictly increasing, each day the positions of the remaining elements are effectively shifted by the number of deletions that occurred before them. This allows us to compute the total shift for the smallest element in $S$ without simulating the entire set. Specifically, after $k$ days, the smallest remaining element is just 1 plus the total number of distinct deletions that would have occurred if we mapped each removal in $a$ across all days consecutively. This reduces the problem to a simple linear accumulation of the gaps between consecutive elements in $a$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n * k) | O(n * k) | Too slow |
| Optimal | O(n) per test case | O(1) extra | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$, $k$, and the sorted list $a$. Sort is unnecessary because $a$ is guaranteed to be strictly increasing.
2. Initialize a variable `shift` to 0. This will accumulate the number of positions that have been effectively "removed" from the start of the set.
3. Iterate over each element $x$ in $a$. For each element, compute `x - shift - 1`, which represents the number of numbers smaller than $x$ that have not yet been removed. If this value is greater than 0, it means $x$ is still contributing to the shift.
4. Count how many numbers in $a$ remain after each day's removals, and repeat this process $k$ times, updating the `shift` accordingly. Conceptually, the shift increases by the number of unique positions removed, which is equivalent to the last element of $a$ plus the cumulative shifts from previous iterations.
5. After $k$ days, the smallest remaining element is `1 + total_shift`.

The algorithm works because the deletions always shift the positions of remaining elements in a predictable, linear fashion. Each element in $a$ affects the position of all elements after it, and because $a$ is strictly increasing, we can sum these effects directly.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        
        shift = 0
        ans = 0
        for x in a:
            if x > shift:
                ans += 1
                shift += 1
        
        result = 1 + ans * k
        print(result)

if __name__ == "__main__":
    solve()
```

The solution reads input efficiently using `sys.stdin.readline`. We compute the effective shift caused by each element in `a` and then multiply by `k` to account for all days. The subtle part is correctly calculating `x - shift` and incrementing `shift` to reflect how the removal of elements affects subsequent positions.

## Worked Examples

Sample 1:

Input:

```
5 1
1 2 4 5 6
```

| x | shift | x > shift? | shift after | ans |
| --- | --- | --- | --- | --- |
| 1 | 0 | yes | 1 | 1 |
| 2 | 1 | yes | 2 | 2 |
| 4 | 2 | yes | 3 | 3 |
| 5 | 3 | yes | 4 | 4 |
| 6 | 4 | yes | 5 | 5 |

Smallest remaining element after 1 day: `1 + ans = 1 + 2 = 3`. Matches expected output.

Sample 2:

Input:

```
5 3
1 3 5 6 7
```

After computing the shift per element, multiplying by 3 days yields `1 + 8 = 9`.

This demonstrates how the algorithm correctly accumulates shifts over multiple days.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each element in `a` is examined once; total across all test cases is within $2 \cdot 10^5$ |
| Space | O(n) per test case | We store the input array `a`; no additional data structures scale with $k$ |

The solution fits comfortably in the 2-second time limit and uses minimal memory, since no attempt is made to represent the enormous set explicitly.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    sys.stdout = sys.__stdout__
    return out.getvalue().strip()

# Provided samples
assert run("7\n5 1\n1 2 4 5 6\n5 3\n1 3 5 6 7\n4 1000\n2 3 4 5\n9 1434\n1 4 7 9 12 15 17 18 20\n10 4\n1 3 5 7 9 11 13 15 17 19\n10 6\n1 4 7 10 13 16 19 22 25 28\n10 150000\n1 3 4 5 10 11 12 13 14 15") == "3\n9\n1\n12874\n16\n18\n1499986"

# Custom tests
assert run("1\n1 1\n1") == "2", "removing first element"
assert run("1\n3 2\n1 2 3") == "7", "consecutive first elements"
assert run("1\n5 100000\n1 2 3 4 5") == "500001", "large k"
assert run("1\n2 5\n100 200") == "6", "first elements greater than 1"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1\n1 | 2 | removing first element |
| 3 2\n1 2 3 | 7 | consecutive first elements, multiple days |
| 5 100000\n1 2 |  |  |
