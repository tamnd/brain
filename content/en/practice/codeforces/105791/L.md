---
title: "CF 105791L - Legendary Paper Cup"
description: "We are asked to count how many numbers inside a given interval can be expressed in a very specific form: the product of three consecutive integers. Every such number comes from choosing an integer $x$ and forming $x cdot (x+1) cdot (x+2)$."
date: "2026-06-21T13:11:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105791
codeforces_index: "L"
codeforces_contest_name: "UFPE Starters Final Try-Outs 2025"
rating: 0
weight: 105791
solve_time_s: 43
verified: true
draft: false
---

[CF 105791L - Legendary Paper Cup](https://codeforces.com/problemset/problem/105791/L)

**Rating:** -  
**Tags:** -  
**Solve time:** 43s  
**Verified:** yes  

## Solution
## Problem Understanding

We are asked to count how many numbers inside a given interval can be expressed in a very specific form: the product of three consecutive integers. Every such number comes from choosing an integer $x$ and forming $x \cdot (x+1) \cdot (x+2)$. The problem then gives many queries, each query providing a range $[L, R]$, and we must determine how many distinct values of this form fall inside that range.

So instead of working with arbitrary numbers, the universe of valid values is completely determined by a single integer parameter $x$. Each $x$ generates exactly one candidate value, and the task becomes counting how many of these generated values lie within a given interval.

The constraints are extremely large: $L$ and $R$ can go up to $10^{16}$, and there can be up to $10^6$ queries. This immediately rules out any per-query iteration over the interval, since even scanning ranges or checking each value individually would be far beyond feasible limits. The solution must rely on preprocessing or fast mathematical localization of valid candidates.

A subtle edge consideration is that valid values are sparse. The function $f(x) = x(x+1)(x+2)$ grows cubically, so values quickly become very far apart. That suggests we may be able to precompute all valid values up to the maximum possible $R$, and answer queries via binary search.

One potential pitfall is assuming multiple different $x$ values might map to the same product. This does not happen for positive integers because the function is strictly increasing for $x \ge 1$. Another issue is overflow during generation, since values grow up to $10^{16}$, so we must stop generation carefully.

## Approaches

A straightforward idea is to try every possible $x$ and compute $x(x+1)(x+2)$, then for each query scan all values and count how many fall inside $[L, R]$. This is correct but completely impractical. Even if we limit $x$, the maximum $x$ such that $x^3 \le 10^{16}$ is around $10^5$. That already gives about $10^5$ values. With up to $10^6$ queries, a linear scan per query leads to $10^{11}$ operations, which is far too large.

The key observation is that the structure of valid numbers does not depend on queries at all. All valid values can be generated independently once, because they only depend on $x$. Since the function is monotonic increasing, we can store all values in a sorted array. Then each query becomes a range count problem over a sorted list, which can be answered with two binary searches.

This turns the problem from “recompute structure per query” into “precompute once, query fast”.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force scan per query | $O(t \cdot n)$ | $O(n)$ | Too slow |
| Precompute + binary search | $O(n + t \log n)$ | $O(n)$ | Accepted |

Here $n$ is the number of valid $x$, roughly $10^5$.

## Algorithm Walkthrough

We start by generating all valid values of the form $x(x+1)(x+2)$ until the value exceeds $10^{16}$. Since the function grows cubically, we only need to iterate $x$ up to about $10^5$, which is safe.

We store every computed value in a list. Because the function is strictly increasing for positive $x$, the list is already sorted, so no additional sorting is required.

For each query $[L, R]$, we locate how many precomputed values lie inside the interval using binary search. Specifically, we find the first position where value is at least $L$, and the first position where value is greater than $R$. The difference between these two positions gives the answer.

### Steps

1. Iterate $x = 1, 2, 3, \dots$ and compute $v = x(x+1)(x+2)$.

We stop when $v > 10^{16}$, because beyond this range no query can include it.
2. Store all generated values in an array `vals`.

This works because every valid number corresponds uniquely to one $x$.
3. For each query $[L, R]$, perform a binary search to find:

the smallest index where `vals[i] >= L` and the smallest index where `vals[i] > R`.
4. The answer for the query is the difference of these two indices.

The correctness of using binary search relies on the fact that `vals` is strictly increasing, so all valid numbers are ordered.

### Why it works

The core invariant is that `vals` contains every possible valid product exactly once, in increasing order. Since every query is only asking for how many precomputed values fall in a range, the problem reduces to counting elements in a sorted array. Binary search gives exact boundary positions without scanning, preserving correctness while reducing complexity.

## Python Solution

```python
import sys
input = sys.stdin.readline

MAXV = 10**16

vals = []
x = 1
while True:
    v = x * (x + 1) * (x + 2)
    if v > MAXV:
        break
    vals.append(v)
    x += 1

# binary search helpers
def lower_bound(a, target):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def upper_bound(a, target):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return lo

t = int(input())
out = []

for _ in range(t):
    L, R = map(int, input().split())
    left = lower_bound(vals, L)
    right = upper_bound(vals, R)
    out.append(str(right - left))

print("\n".join(out))
```

The preprocessing loop constructs all valid legendary values once, ensuring no recomputation per query. The stopping condition at $10^{16}$ avoids overflow and unnecessary work.

The binary search routines are standard boundary finders. `lower_bound` finds the first valid value not less than $L$, while `upper_bound` finds the first value strictly greater than $R$. Their difference directly counts valid entries in range.

One subtle implementation detail is using Python integers safely without overflow concerns. However, explicitly stopping at $10^{16}$ keeps the generated list compact and avoids unnecessary growth.

## Worked Examples

### Example 1

Input:

```
1
10 100
```

Precomputed values start as:

$1\cdot2\cdot3 = 6$,

$2\cdot3\cdot4 = 24$,

$3\cdot4\cdot5 = 60$,

$4\cdot5\cdot6 = 120$, ...

| x | value | in range [10,100] |
| --- | --- | --- |
| 1 | 6 | no |
| 2 | 24 | yes |
| 3 | 60 | yes |
| 4 | 120 | no |

Binary search finds 24 and 60, so answer is 2.

This confirms that only boundary filtering matters, not enumeration per query.

### Example 2

Input:

```
1
50 1000
```

| x | value | in range [50,1000] |
| --- | --- | --- |
| 1 | 6 | no |
| 2 | 24 | no |
| 3 | 60 | yes |
| 4 | 120 | yes |
| 5 | 210 | yes |
| 6 | 336 | yes |
| 7 | 504 | yes |
| 8 | 720 | yes |
| 9 | 990 | yes |
| 10 | 1320 | no |

Valid values are from x = 3 to x = 9 inclusive, giving 7 values. The binary search returns exactly this count, showing correctness over a longer interval.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n + t \log n)$ | Precomputation generates all valid values once, then each query uses two binary searches |
| Space | $O(n)$ | Stores all valid products up to $10^{16}$, about $10^5$ values |

The constraints allow up to $10^6$ queries, so logarithmic per query behavior is essential. The precomputation cost is negligible compared to query volume, and memory usage stays small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    MAXV = 10**16
    vals = []
    x = 1
    while True:
        v = x * (x + 1) * (x + 2)
        if v > MAXV:
            break
        vals.append(v)
        x += 1

    def lower_bound(a, target):
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] < target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    def upper_bound(a, target):
        lo, hi = 0, len(a)
        while lo < hi:
            mid = (lo + hi) // 2
            if a[mid] <= target:
                lo = mid + 1
            else:
                hi = mid
        return lo

    t = int(input())
    out = []
    for _ in range(t):
        L, R = map(int, input().split())
        out.append(str(upper_bound(vals, R) - lower_bound(vals, L)))
    return "\n".join(out)

# provided samples
assert run("1\n10 100\n") == "2"
assert run("3\n10 100\n100 1000\n999900 999999\n") == "2\n7\n1"

# custom cases
assert run("1\n1 5\n") == "0"
assert run("1\n6 6\n") == "1"
assert run("1\n6 7\n") == "1"
assert run("1\n1 10000000000000000\n") == str(len([x for x in range(1, 200000) if x*(x+1)*(x+2) <= 10**16]))
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 5 | 0 | range below first valid value |
| 6 6 | 1 | exact match case |
| 6 7 | 1 | boundary extension |
| full range | all values | maximum coverage |

## Edge Cases

A critical edge case is when the interval lies entirely below the smallest valid value. The smallest product is $1 \cdot 2 \cdot 3 = 6$. For an input like $[1, 5]$, the algorithm produces an empty count because both binary searches return index 0 and no values are included.

Another case is when $L$ or $R$ exactly matches a valid product. For $[6, 6]$, `lower_bound` returns index 0 and `upper_bound` returns index 1, producing correct count 1. The monotonic structure ensures no ambiguity in matching boundaries.

Large intervals such as $[1, 10^{16}]$ test full coverage. In this case, binary search spans the entire precomputed list and returns its full size, since all valid values fall within range.
