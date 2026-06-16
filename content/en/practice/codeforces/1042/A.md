---
title: "CF 1042A - Benches"
description: "We are given several benches, each already occupied by some number of people. Then a group of new people arrives, and each of them must choose a bench and sit there."
date: "2026-06-16T17:51:42+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "implementation"]
categories: ["algorithms"]
codeforces_contest: 1042
codeforces_index: "A"
codeforces_contest_name: "Codeforces Round 510 (Div. 2)"
rating: 1100
weight: 1042
solve_time_s: 136
verified: true
draft: false
---

[CF 1042A - Benches](https://codeforces.com/problemset/problem/1042/A)

**Rating:** 1100  
**Tags:** binary search, implementation  
**Solve time:** 2m 16s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given several benches, each already occupied by some number of people. Then a group of new people arrives, and each of them must choose a bench and sit there. After everyone is seated, one bench will have the largest number of people among all benches, and that value is called $k$.

The task is to compute two extremes of this final maximum load. First, we want the smallest possible value of $k$, assuming we distribute newcomers as evenly as possible to avoid overloading any single bench. Second, we want the largest possible value of $k$, assuming we intentionally concentrate people to make one bench as crowded as possible.

The constraints are small enough that any solution up to roughly $O(n \log(\max a_i + m))$ or even $O(n \cdot m)$ might pass, since $n \le 100$ and $m \le 10000$. This means we can afford either a greedy simulation or a binary search over the answer space without worrying about performance issues.

A subtle failure case appears when trying to greedily distribute people without reasoning about future consequences. For example, always putting a newcomer on the currently least loaded bench can look reasonable but does not directly guarantee optimality unless we formalize it as a capacity problem. Another edge case is when all benches are identical, where both minimum and maximum answers collapse to the same value, and naive uneven distribution thinking can still produce incorrect reasoning if not carefully handled.

## Approaches

The maximum possible value of $k$ is straightforward. Since we want one bench to become as large as possible, we simply take the bench that already has the most people and assign all $m$ newcomers there. No other distribution can increase the maximum further, because spreading people elsewhere only reduces the number added to the target bench. Thus, the maximum case is entirely determined by the initial maximum.

The minimum possible value of $k$ is more structured. We are trying to distribute $m$ people so that no bench becomes too large. This is equivalent to asking for the smallest number $k$ such that we can "cap" all benches at height $k$ by placing newcomers appropriately.

If we fix a candidate value $k$, each bench $i$ can accept at most $k - a_i$ additional people before it reaches $k$. If we sum this capacity over all benches, we get the total number of people we can accommodate without exceeding $k$. If this total is at least $m$, then it is possible to distribute everyone while keeping the maximum at most $k$. Otherwise, it is impossible.

This transforms the problem into a monotonic condition over $k$, which naturally leads to binary search.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Greedy + Binary Search feasibility | $O(n \log(m + \max a_i))$ | $O(1)$ | Accepted |
| Simulation or naive placement | $O(n \cdot m)$ | $O(1)$ | Accepted but unnecessary |

## Algorithm Walkthrough

We separate the computation into two independent parts: maximum and minimum.

### Maximum $k$

1. Compute the maximum initial occupancy among all benches.
2. Add all $m$ newcomers to that same bench.
3. Return the resulting value.

This works because concentrating all additions on one bench can only increase the global maximum, and no other arrangement can exceed this construction.

### Minimum $k$

1. Set a search range for $k$ from $\max(a_i)$ to $\max(a_i) + m$. The lower bound is the current maximum, since we cannot reduce existing loads. The upper bound is when all newcomers go to one bench.
2. For a fixed candidate $k$, compute how many additional people each bench can still accept without exceeding $k$, which is $\max(0, k - a_i)$.
3. Sum these capacities across all benches.
4. If the total capacity is at least $m$, it means we can distribute all newcomers without exceeding $k$, so $k$ is feasible.
5. Otherwise, $k$ is too small.
6. Use binary search to find the smallest feasible $k$.

### Why it works

The key invariant is that feasibility is monotonic in $k$. If a certain $k$ allows all $m$ people to be placed, then any larger value of $k$ also allows placement because every bench only gains more capacity. This monotonicity guarantees that binary search converges to the smallest valid threshold without missing any edge cases.

## Python Solution

```python
import sys
input = sys.stdin.readline

def can(k, a, m):
    total = 0
    for x in a:
        if k > x:
            total += k - x
    return total >= m

n = int(input())
m = int(input())
a = [int(input()) for _ in range(n)]

mx = max(a)

# maximum k
max_k = mx + m

# minimum k via binary search
lo, hi = mx, mx + m
while lo < hi:
    mid = (lo + hi) // 2
    if can(mid, a, m):
        hi = mid
    else:
        lo = mid + 1

min_k = lo

print(min_k, max_k)
```

The code splits the problem cleanly into two independent computations. The helper function `can(k, a, m)` encodes the feasibility condition derived earlier. The binary search runs over the answer space rather than over indices, which is safe because the condition is monotonic in $k$.

A common mistake is forgetting to include the `max(0, k - a_i)` logic and instead summing raw differences, which would incorrectly allow negative contributions from already-overfull benches.

## Worked Examples

### Example 1

Input:

```
4
6
1
1
1
1
```

| Step | k (mid) | Capacity sum | Feasible |
| --- | --- | --- | --- |
| 1 | 3 | (2+2+2+2)=8 | Yes |
| 2 | 2 | (1+1+1+1)=4 | No |
| 3 | 3 | confirmed | Yes |

Minimum $k = 3$, maximum $k = 7$.

This shows how capacity grows with $k$, and the binary search identifies the smallest point where total capacity meets demand.

### Example 2

Input:

```
1
10
5
```

| Step | k | Capacity | Feasible |
| --- | --- | --- | --- |
| 1 | 5 | 0 | No |
| 2 | 15 | 10 | Yes |

Minimum and maximum both equal 15, showing the degenerate case where there is only one bench and all distribution choices collapse.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log(m + \max a_i))$ | Binary search over possible maximum values, each check scans all benches |
| Space | $O(1)$ | Only a few counters are used aside from input storage |

The constraints $n \le 100$ and $m \le 10000$ make this comfortably fast, since at most a few thousand feasibility checks are performed.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys as _sys
    from math import *
    
    n = int(input())
    m = int(input())
    a = [int(input()) for _ in range(n)]

    mx = max(a)
    max_k = mx + m

    def can(k):
        total = 0
        for x in a:
            if k > x:
                total += k - x
        return total >= m

    lo, hi = mx, mx + m
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1

    min_k = lo
    return f"{min_k} {max_k}"

# provided sample
assert run("4\n6\n1\n1\n1\n1\n") == "3 7"

# all same, single bench
assert run("1\n10\n5\n") == "15 15"

# already large spread
assert run("3\n0\n5\n2\n8\n") == "8 8"

# skewed distribution
assert run("3\n5\n10\n1\n1\n") == "10 15"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| all equal benches | symmetric result | uniform distribution handling |
| single bench | identical min/max | degenerate structure |
| zero additions | unchanged max | baseline correctness |
| skewed large max | correct binary behavior | uneven capacity handling |

## Edge Cases

A key edge case is when there is only one bench. In that case, every newcomer must go there, so both minimum and maximum outcomes collapse to the same value. The algorithm handles this naturally because the capacity function reduces to a single term, and binary search immediately converges to $a_1 + m$.

Another edge case is when all benches already have large values and $m$ is small. The binary search still works because feasibility depends only on whether even a slightly increased threshold can absorb all newcomers, and the search range starts at the current maximum, ensuring no invalid lower guesses are considered.

Finally, when all benches are equal, distribution symmetry means that spreading is always optimal for minimizing the maximum. The feasibility check captures this automatically by treating every bench as contributing identical capacity, so the search converges exactly at the balanced threshold.
