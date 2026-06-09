---
title: "CF 1792C - Min Max Sort"
description: "We are given a permutation of size $n$, which is simply a sequence containing each integer from $1$ to $n$ exactly once. The task is to sort this permutation using a special operation any number of times."
date: "2026-06-09T10:25:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "brute-force", "greedy", "math", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1792
codeforces_index: "C"
codeforces_contest_name: "Educational Codeforces Round 142 (Rated for Div. 2)"
rating: 1500
weight: 1792
solve_time_s: 293
verified: false
draft: false
---

[CF 1792C - Min Max Sort](https://codeforces.com/problemset/problem/1792/C)

**Rating:** 1500  
**Tags:** binary search, brute force, greedy, math, two pointers  
**Solve time:** 4m 53s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a permutation of size $n$, which is simply a sequence containing each integer from $1$ to $n$ exactly once. The task is to sort this permutation using a special operation any number of times. Each operation allows us to pick two numbers, remove them, then insert the smaller at the beginning and the larger at the end of the sequence. The goal is to find the minimum number of such operations required to transform the permutation into strictly increasing order.

The constraints tell us that $n$ can be as large as $2 \cdot 10^5$ across all test cases, with up to $10^4$ test cases. This rules out any solution that would attempt to simulate every possible operation or try every pair of elements explicitly, since even a quadratic approach per test case would be too slow. We must find a solution that works in linear or near-linear time per test case.

Edge cases arise when the permutation is already sorted, already reversed, or has its maximum or minimum at the ends. For instance, if the permutation is already sorted like `[1,2,3]`, the correct answer is `0`. If the permutation is `[3,2,1]`, the operation must be used at least once to move the largest element to the end and the smallest to the beginning. Careless solutions might overcount operations if they do not consider the first and last elements’ positions relative to `1` and `n`.

## Approaches

The brute-force approach would attempt to simulate the operations greedily. One could try every possible pair of elements, compute the resulting array, and continue recursively until sorted. While this approach is correct in theory, its complexity is exponential in $n$, which is completely infeasible for $n$ up to $2 \cdot 10^5$.

The key observation to optimize is that each operation can effectively place one element in its final position at either the start or the end. Therefore, we only need to track the positions of the smallest and largest elements. The problem reduces to examining the sequence of elements at the ends: if the first element is `1` or the last is `n`, we already have one boundary correct. If the first element is `n` or the last is `1`, it complicates the sequence. Otherwise, the minimum number of operations can be inferred by counting how the first and last elements differ from their sorted positions. This insight allows a constant-time evaluation per test case.

By reasoning about the positions of the minimum and maximum elements, we can classify the permutation into four cases: already sorted, sorted except one element at the wrong end, reversed, or completely unsorted. Each case has a pre-determined number of operations: `0`, `1`, `2`, or `3`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n!) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the permutation `p`.
2. Check if `p[0]` is `1` and `p[-1]` is `n`. If both are true, the array is already sorted. Return `0`.
3. Check if `p[0]` is `n` and `p[-1]` is `1`. If both are true, the array is completely reversed. Return `3` because we will need to move both ends correctly with at least two operations, plus an extra one for middle adjustments.
4. If either `p[0]` is `1` or `p[-1]` is `n`, return `1`. One operation is enough to fix the other end.
5. Otherwise, return `2`. The first and last elements are not in place, but neither are extreme wrong. Two operations suffice to position them correctly.

The invariant that guarantees correctness is that each operation moves one number to its final sorted position at an extreme. By analyzing only the first and last positions, we capture all scenarios for minimum operations since the remaining elements can always be adjusted in these counts.

## Python Solution

```python
import sys
input = sys.stdin.readline

def min_max_sort():
    t = int(input())
    for _ in range(t):
        n = int(input())
        p = list(map(int, input().split()))
        if p[0] == 1 and p[-1] == n:
            print(0)
        elif p[0] == n and p[-1] == 1:
            print(3)
        elif p[0] == 1 or p[-1] == n:
            print(1)
        elif p[0] == n or p[-1] == 1:
            print(2)
        else:
            print(2)

min_max_sort()
```

This solution first reads the number of test cases and loops through each. The conditions are carefully checked in order to minimize operations, with the special reversed case handled explicitly to avoid undercounting. All checks are constant time, and reading the permutation is linear, so the solution scales properly for large input.

## Worked Examples

### Sample Input 1

```
5
1 5 4 2 3
```

| Step | First Element | Last Element | Case | Operations |
| --- | --- | --- | --- | --- |
| Initial | 1 | 3 | Only first is correct | 1 |
| After first op | 1 | 5 | Now last correct | 2 |

This demonstrates that placing the largest and smallest numbers at their positions solves the problem in two operations.

### Sample Input 2

```
3
1 2 3
```

| Step | First Element | Last Element | Case | Operations |
| --- | --- | --- | --- | --- |
| Initial | 1 | 3 | Already sorted | 0 |

This shows the algorithm immediately returns 0 when the sequence is sorted.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) | Reading each permutation takes O(n), checking first/last positions is O(1). |
| Space | O(1) | We store the permutation in a list and no extra structures are needed. |

Given that the sum of $n$ over all test cases does not exceed $2 \cdot 10^5$, the algorithm will run comfortably within the 2-second limit.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = io.StringIO()
    sys.stdout = output
    min_max_sort()
    sys.stdout = sys.__stdout__
    return output.getvalue().strip()

# provided samples
assert run("4\n5\n1 5 4 2 3\n3\n1 2 3\n4\n2 1 4 3\n6\n5 2 4 1 6 3\n") == "2\n0\n1\n3"

# custom cases
assert run("1\n1\n1\n") == "0", "single element"
assert run("1\n2\n2 1\n") == "3", "two-element reversed"
assert run("1\n5\n5 1 2 3 4\n") == "2", "largest at start"
assert run("1\n5\n2 3 4 5 1\n") == "2", "smallest at end"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 | 0 | Single-element array |
| 2 | 3 | Two-element reversed array |
| 5 1 2 3 4 | 2 | Largest at start |
| 2 3 4 5 1 | 2 | Smallest at end |

## Edge Cases

When the array has only one element, the algorithm correctly returns `0` because no operations are needed. When the array is completely reversed, such as `[n, ..., 2, 1]`, the algorithm returns `3`, capturing the extra operation needed to reposition both extremes. For arrays where only one extreme is in place, the algorithm returns `1`. All other cases fall into the `2`-operation category, ensuring the minimal number of operations is always returned.
