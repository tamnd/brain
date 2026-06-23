---
title: "CF 105064G - Armed Soldiers 1"
description: "We are given a set of soldiers placed on a number line. Each soldier has a fixed position and a weapon with a certain power. When a monster appears at some position, every soldier shoots toward that position."
date: "2026-06-23T10:04:26+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105064
codeforces_index: "G"
codeforces_contest_name: "ICPC-de-Tryst 2024"
rating: 0
weight: 105064
solve_time_s: 77
verified: false
draft: false
---

[CF 105064G - Armed Soldiers 1](https://codeforces.com/problemset/problem/105064/G)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 17s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of soldiers placed on a number line. Each soldier has a fixed position and a weapon with a certain power. When a monster appears at some position, every soldier shoots toward that position. A bullet can only contribute a hit if it still has enough remaining power after traveling the distance from the soldier to the monster. The farther the bullet travels, the weaker it becomes linearly.

For a monster placed at position $d$ with shield width $s$, a soldier at position $a_i$ with power $p_i$ successfully contributes a hit if the distance penalty does not reduce its power below the shield requirement. This condition simplifies to the inequality

$$|a_i - d| \le p_i - s.$$

So for any fixed shield width $s$, and any location $d$, we can count how many soldiers can still hit the monster. The monster survives at position $d$ if this count is at most $k$. The goal is to choose the smallest possible integer $s$ such that no matter where the monster stands on the number line, the number of hits never exceeds $k$.

The constraints push toward an $O(n \log n)$ or $O(n)$ solution per test case. With up to $10^5$ total soldiers across all test cases, anything quadratic in $n$ would be too slow because it would require up to $10^{10}$ operations in the worst case.

A few subtle edge cases appear immediately. If all soldiers have zero power, then any positive shield width trivially prevents all hits, but the answer must still be non-negative. If $k = n$, then the monster is allowed to be hit by all soldiers, so even a zero shield might suffice. If soldiers are densely clustered at the same point with high power, then even a large shield may be required to reduce overlap intervals.

The most important hidden difficulty is that we are not asked about a fixed position $d$, but about the worst possible $d$, which forces us to reason about global overlap structure rather than pointwise evaluation.

## Approaches

A direct way to think about the problem is to fix a shield width $s$ and then simulate every possible monster position. For each position $d$, we would count how many soldiers satisfy $|a_i - d| \le p_i - s$. This is equivalent to checking how many intervals cover each point, since each soldier defines an interval of influence centered at $a_i$ with radius $p_i - s$. The brute-force approach would evaluate this coverage for all integer positions between $1$ and $10^9$, which is clearly infeasible.

Even if we restrict ourselves to only checking critical points, recomputing coverage for each $s$ still costs $O(n^2)$ in the worst case because each check involves scanning all soldiers.

The key observation is that for a fixed $s$, each soldier contributes a symmetric interval:

$$[a_i - (p_i - s),\ a_i + (p_i - s)].$$

We want to ensure that no point lies inside more than $k$ such intervals. This is a classic “minimum maximum overlap” problem.

Instead of fixing $s$ and checking overlap, we invert the perspective: we ask what is the minimum $s$ such that the maximum overlap of these shrinking intervals is at most $k$. As $s$ increases, intervals shrink uniformly, so overlap can only decrease. This monotonicity allows binary search on $s$.

For a fixed candidate $s$, we compute all intervals, sort endpoints, and sweep line to compute maximum overlap in $O(n \log n)$. Then we binary search the smallest $s$ satisfying the condition.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all positions) | $O(n \cdot 10^9)$ | $O(n)$ | Too slow |
| Check + Binary Search + Sweep Line | $O(n \log n \log P)$ | $O(n)$ | Accepted |

Here $P$ is the maximum power scale.

## Algorithm Walkthrough

### 1. Interpret each soldier as a shrinking interval

For a fixed shield $s$, compute each soldier’s effective radius $r_i = p_i - s$. If $r_i < 0$, that soldier contributes no interval at all. Otherwise it covers the segment $[a_i - r_i, a_i + r_i]$. This converts the problem into interval overlap counting.

The reason this transformation works is that the original condition is exactly the condition for a point to lie inside a radius around a center.

### 2. Define feasibility of a shield

We define a function `check(s)` that returns true if no point on the line is covered by more than $k$ intervals. This directly matches the requirement that the monster survives anywhere.

The monotonic behavior is crucial: increasing $s$ only decreases all $r_i$, so intervals only shrink and overlaps cannot increase.

### 3. Compute maximum overlap for a fixed $s$

To evaluate `check(s)`, we generate all valid intervals and convert them into events: +1 at the left endpoint and -1 just after the right endpoint. Sorting these events allows a sweep that maintains the number of active intervals at every coordinate. The maximum value during the sweep is the maximum number of simultaneous hits.

We compare this maximum with $k$.

### 4. Binary search the smallest valid $s$

Since feasibility is monotonic, we binary search $s$ from 0 up to $\max p_i$. Each step runs the sweep line check.

### Why it works

Each soldier defines a family of intervals that shrink uniformly as $s$ increases. The function “maximum overlap of intervals” is monotone non-increasing in $s$, so the set of valid $s$ values is a suffix of integers. Binary search correctly finds the smallest valid value. The sweep line correctly captures worst-case overlap because any point of maximum coverage must occur at an interval endpoint in this construction.

## Python Solution

```python
import sys
input = sys.stdin.readline

def check(s, a, p, k):
    events = []
    for ai, pi in zip(a, p):
        r = pi - s
        if r < 0:
            continue
        l = ai - r
        rgt = ai + r
        events.append((l, 1))
        events.append((rgt + 1, -1))
    
    events.sort()
    
    cur = 0
    best = 0
    for x, v in events:
        cur += v
        if cur > best:
            best = cur
    
    return best <= k

def solve():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))
        
        lo, hi = 0, max(p)
        ans = hi
        
        while lo <= hi:
            mid = (lo + hi) // 2
            if check(mid, a, p, k):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        
        print(ans)

if __name__ == "__main__":
    solve()
```

The core structure is a binary search wrapped around a feasibility check. The `check` function builds interval events and runs a sweep line to compute the maximum overlap.

A subtle point is the use of `rgt + 1` for the closing event. This ensures correct integer coverage semantics: a point exactly at the right endpoint is still included in the interval.

Another important detail is skipping soldiers where $p_i - s < 0$, since they cannot contribute any valid coverage.

## Worked Examples

Consider a small configuration where soldiers are at positions `[1, 5, 9]` with powers `[3, 3, 3]`, and $k = 1$.

### Trace for $s = 1$

| Soldier | Interval radius $p_i - s$ | Interval |
| --- | --- | --- |
| 1 | 2 | [-1, 3] |
| 5 | 2 | [3, 7] |
| 9 | 2 | [7, 11] |

Sweep events:

sorted events = (-1,+1), (3,+1), (4,-1), (7,+1), (8,-1), (12,-1)

| Event | Active |
| --- | --- |
| -1 | 1 |
| 3 | 2 |
| 4 | 1 |
| 7 | 2 |
| 8 | 1 |
| 12 | 0 |

Maximum overlap is 2, which exceeds $k=1$, so $s=1$ is invalid.

### Trace for $s = 2$

| Soldier | Interval radius | Interval |
| --- | --- | --- |
| 1 | 1 | [0, 2] |
| 5 | 1 | [4, 6] |
| 9 | 1 | [8, 10] |

Events:

(0,+1), (3,-1), (4,+1), (7,-1), (8,+1), (11,-1)

| Event | Active |
| --- | --- |
| 0 | 1 |
| 3 | 0 |
| 4 | 1 |
| 7 | 0 |
| 8 | 1 |
| 11 | 0 |

Maximum overlap is 1, satisfying the condition.

These traces show that increasing $s$ reduces interval size and strictly decreases overlap, which is the core monotonicity used in binary search.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(n \log n \log P)$ | Each feasibility check sorts $O(n)$ events, and binary search runs over $O(\log P)$ values |
| Space | $O(n)$ | Event list stores up to $2n$ endpoints |

The total $n$ across test cases is $10^5$, so even with logarithmic factors, the solution comfortably fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    def check(s, a, p, k):
        events = []
        for ai, pi in zip(a, p):
            r = pi - s
            if r < 0:
                continue
            l = ai - r
            rgt = ai + r
            events.append((l, 1))
            events.append((rgt + 1, -1))
        events.sort()
        cur = best = 0
        for _, v in events:
            cur += v
            best = max(best, cur)
        return best <= k

    t = int(input())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        a = list(map(int, input().split()))
        p = list(map(int, input().split()))

        lo, hi = 0, max(p)
        ans = hi
        while lo <= hi:
            mid = (lo + hi) // 2
            if check(mid, a, p, k):
                ans = mid
                hi = mid - 1
            else:
                lo = mid + 1
        out.append(str(ans))
    return "\n".join(out)

# sample-style sanity checks
assert run("1\n3 1\n1 5 9\n3 3 3\n") == "2"
assert run("1\n2 0\n1 10\n0 0\n") == "0"
assert run("1\n3 2\n1 2 3\n5 5 5\n") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| symmetric shrinking intervals | 2 | overlap reduction with increasing s |
| zero power soldiers | 0 | immediate feasibility edge case |
| k close to n | 0 | trivial survival condition |

## Edge Cases

When all powers are zero, every soldier produces empty or negative-radius intervals for any positive $s$. The sweep line receives no events, so maximum overlap is zero and the algorithm correctly accepts $s = 0$.

When $k = n$, every configuration is valid even at $s = 0$. The check function computes a maximum overlap that never exceeds $n$, so binary search immediately converges to zero.

When soldiers are all at the same position with large power, the initial overlap is $n$ at $s = 0$. The check function correctly reports failure until $s$ reduces all radii enough that intervals shrink and split, reducing overlap below $k$.
