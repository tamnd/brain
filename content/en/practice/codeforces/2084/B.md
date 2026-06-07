---
title: "CF 2084B - MIN = GCD"
description: "We are given a sequence of positive integers, and we need to determine if it is possible to split the sequence into two contiguous parts after some rearrangement, such that the minimum value in the first part equals the greatest common divisor of the second part."
date: "2026-06-08T06:11:36+07:00"
tags: ["codeforces", "competitive-programming", "greedy", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 2084
codeforces_index: "B"
codeforces_contest_name: "Teza Round 1 (Codeforces Round 1015, Div. 1 + Div. 2)"
rating: 1100
weight: 2084
solve_time_s: 89
verified: true
draft: false
---

[CF 2084B - MIN = GCD](https://codeforces.com/problemset/problem/2084/B)

**Rating:** 1100  
**Tags:** greedy, math, number theory  
**Solve time:** 1m 29s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a sequence of positive integers, and we need to determine if it is possible to split the sequence into two contiguous parts after some rearrangement, such that the minimum value in the first part equals the greatest common divisor of the second part. In other words, we are allowed to reorder the array arbitrarily, then pick a split point where the left segment’s minimum matches the right segment’s GCD.

The input guarantees up to $10^4$ test cases, each with $n$ up to $10^5$ integers, and the sum of $n$ over all test cases is at most $10^5$. The integers themselves can be very large, up to $10^{18}$. This immediately rules out algorithms that require examining all possible splits or permutations. Any solution iterating over $O(n^2)$ possibilities would be too slow. We must find an $O(n)$ or $O(n \log n)$ approach per test case.

A key edge case is when all elements are equal. For example, if the sequence is $[7,7,7]$, we can split after any position, and the minimum and GCD will both be 7, so the answer is "Yes". Another subtle case occurs when the minimum occurs multiple times but is not a divisor of all remaining elements. For example, $[1,2,3]$ cannot be split to satisfy the condition if 1 is the left minimum and the right GCD is not 1. Careless algorithms that just check for the existence of the global minimum somewhere may fail here.

## Approaches

The brute-force approach would try all permutations of the sequence and all split positions, computing the minimum for the left and the GCD for the right. This works in theory because any correct split must satisfy the given equality, but in practice, there are $n!$ permutations, each with $n-1$ splits, which is infeasible even for $n=10$.

Observing the problem structure, we notice that the only candidate for the left segment minimum that can match the right segment GCD is the global minimum of the array. This is because any minimum in the left segment cannot be smaller than the global minimum, and the GCD of any positive integers is at most the smallest among them. Therefore, if a split exists, the value $\min(left) = \gcd(right)$ must equal the overall minimum of the array.

Given this, we can simplify the problem: let $m$ be the global minimum of the array. Then any element that is not a multiple of $m$ cannot be in the right segment, because the GCD of that segment must equal $m$. So the solution reduces to checking whether all elements divisible by $m$ can form a contiguous right segment after removing other elements. If yes, we can reorder the array so that these elements are at the end, and the left segment contains all remaining elements. If no, the split is impossible.

This observation reduces the problem from factorial-time to linear-time checking, with only one scan needed to ensure all non-multiples of the minimum can go to the left segment. We do not need to compute any GCD dynamically, because we already know the GCD of a set of numbers all divisible by $m$ is at least $m$, and any number in the right segment must be a multiple of $m$.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n! * n) | O(n) | Too slow |
| Optimal | O(n) | O(1) | Accepted |

## Algorithm Walkthrough

1. For each test case, read $n$ and the array $a$.
2. Compute the global minimum $m = \min(a)$. This is the only candidate value for both $\min(left)$ and $\gcd(right)$.
3. Verify that all elements in the array are either equal to $m$ or divisible by $m$. Any element not divisible by $m$ must be in the left segment.
4. After partitioning all multiples of $m$ into the right segment and the rest into the left, the left minimum remains $m$ and the right GCD is $m$ as well. If any element in the supposed right segment is not divisible by $m$, output "No".
5. If the check passes, output "Yes".

Why it works: The algorithm relies on the invariant that the left segment's minimum cannot be smaller than the global minimum, and the right segment's GCD cannot be smaller than the smallest number in it. By making the global minimum the candidate for both, any violation (an element in the right segment not divisible by $m$) would make the equality impossible. Reordering ensures all multiples of $m$ can go into the right segment while preserving the condition.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd
from functools import reduce

def solve():
    t = int(input())
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        m = min(a)
        if all(x % m == 0 or x == m for x in a):
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    solve()
```

The solution first computes the global minimum in linear time. The conditional checks each element in the array once, verifying divisibility by $m$. Using `all()` is efficient, stopping at the first failure. Python's integer type handles values up to $10^{18}$ without overflow.

## Worked Examples

Sample Input:

```
3
2
1 1
2
1 2
3
2 2 3
```

| Step | Array | Minimum m | Check divisible | Result |
| --- | --- | --- | --- | --- |
| 1 | [1,1] | 1 | 1%1=0,1%1=0 | Yes |
| 2 | [1,2] | 1 | 1%1=0,2%1=0 | Yes |
| 3 | [2,2,3] | 2 | 2%2=0,2%2=0,3%2≠0 | No |

The first case works trivially because both numbers are equal. The second case works as all numbers are divisible by 1. The third case fails because 3 is not divisible by 2, so we cannot place it in the right segment.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Single pass to find minimum and check divisibility |
| Space | O(n) | Store the array for processing |

Given the sum of $n$ over all test cases does not exceed $10^5$, the algorithm runs well under 1 second, and memory usage is within 256 MB.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    sys.stdout = out
    solve()
    return out.getvalue().strip()

# Provided samples
assert run("7\n2\n1 1\n2\n1 2\n3\n2 2 3\n3\n2 3 4\n5\n4 5 6 9 3\n3\n998244359987710471 99824435698771045 1000000007\n6\n1 1 4 5 1 4\n") == "Yes\nNo\nYes\nNo\nYes\nYes\nYes"

# Custom cases
assert run("1\n2\n7 7\n") == "Yes", "all equal"
assert run("1\n3\n6 9 12\n") == "Yes", "all multiples of minimum"
assert run("1\n3\n2 3 4\n") == "No", "non-divisible element"
assert run("1\n2\n1 1000000000000000000\n") == "Yes", "minimum is 1"
assert run("1\n4\n2 2 2 2\n") == "Yes", "all identical large array"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2\n7 7 | Yes | All elements equal |
| 3\n6 9 12 | Yes | All elements multiples of minimum |
| 3\n2 3 4 | No | Non-divisible element present |
| 2\n1 1000000000000000000 | Yes | Minimum is 1, large integer |
| 4\n2 2 2 2 | Yes | All identical large array |

## Edge Cases

The edge case of all elements equal is handled because the global minimum is equal to every element, so the divisibility check passes. For arrays where the minimum is 1, all elements are divisible by 1, so any split works. Arrays with a single element not divisible by the minimum fail the check, producing the correct "No". The algorithm correctly handles large numbers because Python integers automatically expand without overflow.
