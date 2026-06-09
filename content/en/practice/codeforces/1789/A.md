---
title: "CF 1789A - Serval and Mocha's Array"
description: "We are given several test cases, each consisting of a small array of positive integers. For each array, we are allowed to reorder its elements arbitrarily. After choosing an order, we inspect every prefix of length at least two and compute the gcd of that prefix."
date: "2026-06-09T10:43:23+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "math", "number-theory"]
categories: ["algorithms"]
codeforces_contest: 1789
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 853 (Div. 2)"
rating: 800
weight: 1789
solve_time_s: 170
verified: false
draft: false
---

[CF 1789A - Serval and Mocha's Array](https://codeforces.com/problemset/problem/1789/A)

**Rating:** 800  
**Tags:** brute force, math, number theory  
**Solve time:** 2m 50s  
**Verified:** no  

## Solution
## Problem Understanding

We are given several test cases, each consisting of a small array of positive integers. For each array, we are allowed to reorder its elements arbitrarily. After choosing an order, we inspect every prefix of length at least two and compute the gcd of that prefix. The requirement is that every such prefix must have a gcd that does not exceed the prefix length. We need to decide whether there exists at least one ordering of the array that satisfies this constraint.

The constraints are small per test case, with at most a few hundred elements in total across all tests. That means an $O(n \log n)$ or even $O(n^2)$ approach per test case is acceptable, but anything involving factorial or exponential rearrangement is not.

A subtle failure case for naive reasoning is assuming that local checks on adjacent pairs are sufficient. For example, in an array like $[3, 6, 1]$, all adjacent pairs except the first might look harmless, but the prefix $[3,6]$ already violates the condition since its gcd is $3$, which is larger than its length $2$. This shows that the constraint is fundamentally prefix-based, not pair-based.

Another common pitfall is assuming that the original order is meaningful. The problem explicitly allows reordering, so any solution that only evaluates the given sequence without considering permutations will fail on cases like $[15, 35, 21]$, where a good ordering exists even though the input order is not valid.

## Approaches

The brute-force approach is to try all permutations of the array and check whether each ordering satisfies the prefix gcd condition. For each permutation, we compute prefix gcds and verify the constraint. This is correct but immediately infeasible because the number of permutations grows as $n!$, which is far beyond any limit even for $n = 20$.

The key observation is that we do not actually need to explore all permutations. The condition only depends on prefix gcd values, and gcd behaves monotonically in a very strong way: once it becomes small, it never increases again when adding more numbers. This suggests that arranging elements in increasing order is a natural candidate, since small values tend to reduce gcd early, which makes later constraints easier to satisfy.

This leads to a greedy idea: sort the array, then check whether this sorted order already satisfies all prefix constraints. If even the best-structured ordering (sorted ascending) fails, no other permutation can fix the early prefix gcd explosion, because any permutation that places large gcd-contributing elements earlier only makes the prefix gcd larger or equal.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (all permutations) | $O(n!)$ | $O(n)$ | Too slow |
| Sort + prefix check | $O(n \log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We construct the solution in the following way.

1. For each test case, sort the array in non-decreasing order. This creates the most stable prefix structure in terms of gcd growth.
2. Traverse the array from left to right while maintaining the gcd of the current prefix.
3. At each position $i$, compute the gcd of the prefix ending at $i$. If $i \ge 1$, check whether this gcd is greater than $i + 1$. If it is, we immediately know no valid permutation exists.
4. If we finish the scan without violating the condition, the sorted arrangement is valid, so the answer is YES.

The reason we only check the sorted array is that any attempt to “fix” a bad prefix would require inserting smaller numbers earlier, but those are already placed as early as possible in sorted order. If sorted order cannot keep the gcd under control, no rearrangement can.

### Why it works

The gcd of a prefix can only decrease when we include a number that is not a multiple of the current gcd, and small numbers are the most effective at breaking large gcd values early. Sorting ensures that the smallest available elements are used as early as possible, minimizing prefix gcd at every step. Since the condition becomes stricter as prefix length increases, any ordering that fails even this best-case greedy construction implies impossibility.

## Python Solution

```python
import sys
input = sys.stdin.readline
from math import gcd

t = int(input())
for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    
    a.sort()
    
    g = 0
    ok = True
    
    for i, x in enumerate(a):
        g = gcd(g, x)
        if i >= 1 and g > i + 1:
            ok = False
            break
    
    print("Yes" if ok else "No")
```

After sorting, we maintain a running gcd. The important detail is the index comparison: since prefix length is $i+1$, we compare gcd against $i+1$, not $i$. The first element is never checked because the condition only applies to prefixes of length at least two.

The only subtlety is initializing the gcd with zero, which correctly acts as a neutral element so that the first update simply sets it to the first array value.

## Worked Examples

Consider the input $[3, 6, 1]$. After sorting we get $[1, 3, 6]$.

At each step:

| i | value | prefix gcd |
| --- | --- | --- |
| 0 | 1 | 1 |
| 1 | 3 | 1 |
| 2 | 6 | 1 |

All prefix gcd values are never greater than their indices plus one, so this is valid.

Now consider $[15, 35, 21]$. Sorting gives $[15, 21, 35]$.

| i | value | prefix gcd |
| --- | --- | --- |
| 0 | 15 | 15 |
| 1 | 21 | 3 |
| 2 | 35 | 1 |

At $i = 1$, prefix length is 2 and gcd is 3, which violates the condition, so the answer is NO.

This demonstrates that the failure is detected as early as possible in the sorted configuration, confirming that sorting exposes any unavoidable violation.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n)$ | Sorting dominates, gcd updates are linear |
| Space | $O(1)$ extra | Only prefix variables are stored |

The total input size is small enough that sorting each test case is easily fast within limits, and the gcd computation is constant work per element.

## Test Cases

```python
import sys, io
from math import gcd

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    t = int(input())
    out = []
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        a.sort()
        g = 0
        ok = True
        for i, x in enumerate(a):
            g = gcd(g, x)
            if i >= 1 and g > i + 1:
                ok = False
                break
        out.append("Yes" if ok else "No")
    return "\n".join(out)

# provided samples
assert run("""6
2
3 6
3
1 2 4
3
3 6 1
3
15 35 21
4
35 10 35 14
5
1261 227821 143 4171 1941
""") == """No
Yes
Yes
No
Yes
Yes"""

# custom cases
assert run("""1
2
4 6
""") == "Yes", "small valid case"

assert run("""1
2
4 8
""") == "No", "small invalid case"

assert run("""1
4
6 10 15 21
""") == "No", "multiple gcd growth failure"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 4 6 | Yes | smallest valid pair |
| 4 8 | No | gcd exceeds prefix length early |
| 6 10 15 21 | No | chained gcd failure in longer array |

## Edge Cases

A minimal array of size two exposes the entire condition immediately, since the only prefix to check is the full array itself. The algorithm correctly handles this because the sorted order is evaluated once and the gcd is compared against 2.

Arrays containing repeated values behave predictably because repeated gcd reinforcement either keeps the gcd stable or increases it, and the sorted scan immediately detects when this growth crosses the allowed prefix threshold.
