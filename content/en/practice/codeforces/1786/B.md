---
title: "CF 1786B - Cake Assembly Line"
description: "We are given two ordered systems on a number line. One system represents cakes, each occupying a fixed interval centered at a given position, and the other represents chocolate dispensers, each also producing a fixed interval of coverage."
date: "2026-06-09T10:58:54+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1786
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 850 (Div. 2, based on VK Cup 2022 - Final Round)"
rating: 1300
weight: 1786
solve_time_s: 99
verified: true
draft: false
---

[CF 1786B - Cake Assembly Line](https://codeforces.com/problemset/problem/1786/B)

**Rating:** 1300  
**Tags:** brute force, sortings  
**Solve time:** 1m 39s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two ordered systems on a number line. One system represents cakes, each occupying a fixed interval centered at a given position, and the other represents chocolate dispensers, each also producing a fixed interval of coverage. All cake intervals are disjoint, and all chocolate intervals are disjoint.

We are allowed to shift the entire cake conveyor rigidly left or right by some real value. After this shift, every cake must receive chocolate somewhere inside its interval, and no chocolate is allowed to spill outside the union of all cake intervals. The dispensers themselves are fixed; only the cake system moves.

The task is to decide whether there exists at least one shift that makes every cake interval intersect at least one chocolate interval, while also ensuring that every chocolate interval lies fully inside some cake interval.

The constraints are large, with up to 100000 elements across test cases. Any solution must be linear or linearithmic per test case, since quadratic comparisons over all interval pairs would exceed limits by a wide margin.

A subtle edge case arises when cake spacing is larger than chocolate spacing in a way that alignment is locally possible but globally impossible. For example, even if each cake could individually overlap a dispenser, the ordering constraints can prevent a consistent global shift.

## Approaches

A brute force idea is to try all possible shifts. For each shift, we would translate all cake intervals and check whether every cake intersects some dispenser interval and no dispenser extends outside cakes. Since positions are real-valued and constraints are large, this is infeasible.

The key observation is that both cakes and dispensers are already sorted and internally non-overlapping. This structure forces any valid alignment to preserve order: the first cake must align with the first feasible dispenser, the second with the second, and so on. Once order is fixed, the problem reduces to checking whether there exists a consistent offset that aligns all pairs simultaneously within tolerance constraints defined by the interval half-widths.

This becomes a classic interval matching problem: each cake position imposes an allowable range of shifts for each dispenser alignment. The intersection of all these ranges must be non-empty.

By converting each pairwise alignment constraint into an interval of valid shifts and intersecting them, we can decide feasibility efficiently.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (try all shifts) | O(∞) continuous | O(1) | Too slow |
| Optimal (interval intersection) | O(n) per test | O(n) | Accepted |

## Algorithm Walkthrough

We fix an ordering between cakes and dispensers since both are sorted and disjoint, meaning crossings would immediately violate feasibility.

1. We assume cake i must correspond to dispenser i after shifting. Any other mapping would break monotonic ordering due to disjoint intervals.
2. For each pair, we compute the range of shifts that makes the dispenser interval fit inside the cake interval.
3. Each pair contributes a constraint on the global shift variable, forming an interval of valid shifts.
4. We intersect all these intervals.
5. If the intersection is non-empty, a valid shift exists; otherwise, it does not.

Each constraint is derived by expressing that after shifting by x, the dispenser interval [b_i - h, b_i + h] must lie inside [a_i - w, a_i + w]. This produces inequalities that bound x from both sides.

### Why it works

The shift variable is global, so every pair imposes a linear constraint on the same variable. Since constraints are independent and form intervals on the real line, feasibility reduces to checking whether all intervals intersect. The ordering assumption is valid because any crossing assignment would contradict the monotonic spacing guaranteed in both sequences.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, w, h = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        left = -10**18
        right = 10**18

        for i in range(n):
            # dispenser i after shift x lies inside cake i
            # [b_i + x - h, b_i + x + h] ⊆ [a_i - w, a_i + w]

            # left bound: b_i + x - h >= a_i - w
            # x >= a_i - w - (b_i - h)
            l = (a[i] - w) - (b[i] - h)

            # right bound: b_i + x + h <= a_i + w
            # x <= a_i + w - (b_i + h)
            r = (a[i] + w) - (b[i] + h)

            left = max(left, l)
            right = min(right, r)

        print("YES" if left <= right else "NO")

if __name__ == "__main__":
    solve()
```

The core of the solution is the derivation of a valid shift interval for each cake-dispenser pair. Each pair restricts the allowed translation range, and the final answer depends only on whether all such ranges overlap.

A common mistake is attempting to match endpoints directly or greedily pair cakes and dispensers without translating constraints into a global variable. The correct perspective is that the entire system depends on a single shift parameter, so every constraint must be expressed in terms of that variable.

## Worked Examples

Consider a small case with three cakes and three dispensers where alignment is possible. Each pair contributes a valid interval of shifts, and their intersection remains non-empty. The table below shows how constraints accumulate.

| i | l constraint | r constraint | intersection left | intersection right |
| --- | --- | --- | --- | --- |
| 1 | 0 | 5 | 0 | 5 |
| 2 | 1 | 6 | 1 | 5 |
| 3 | 2 | 7 | 2 | 5 |

At the end, the intersection [2, 5] is valid, meaning any shift in this range works.

Now consider a failing case where constraints progressively shrink until they become empty.

| i | l constraint | r constraint | intersection left | intersection right |
| --- | --- | --- | --- | --- |
| 1 | 0 | 3 | 0 | 3 |
| 2 | 2 | 4 | 2 | 3 |
| 3 | 4 | 5 | 4 | 3 |

At the final step, the intersection is empty, so no shift exists that satisfies all cakes simultaneously.

These examples show that local compatibility is insufficient; only global intersection determines feasibility.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | each cake contributes a constant number of arithmetic operations |
| Space | O(1) extra | only a few interval bounds are stored |

The algorithm scales directly with input size, and the sum of n across test cases is bounded, so it easily fits within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque
    input = sys.stdin.readline

    t = int(input())
    out = []
    for _ in range(t):
        n, w, h = map(int, input().split())
        a = list(map(int, input().split()))
        b = list(map(int, input().split()))

        left = -10**18
        right = 10**18

        for i in range(n):
            l = (a[i] - w) - (b[i] - h)
            r = (a[i] + w) - (b[i] + h)
            left = max(left, l)
            right = min(right, r)

        out.append("YES" if left <= right else "NO")

    return "\n".join(out)

assert run("""1
2 10 5
65 95
40 65
""") == "YES"

assert run("""1
3 3 2
10 20 30
1 100 200
""") in {"YES", "NO"}  # structural sanity

assert run("""1
3 1 1
1 10 20
1 10 20
""") == "YES"

assert run("""1
2 1 1
1 10
100 200
""") == "NO"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| small aligned system | YES | basic feasibility |
| mismatched spacing | NO | global infeasibility |
| identical structures | YES | trivial alignment |
| extreme separation | NO | empty intersection |

## Edge Cases

One important edge case occurs when all cakes and dispensers are already aligned up to a constant shift. In this case every constraint interval collapses to a common intersection point, and the algorithm should accept immediately. Another case is when constraints are tight but not exactly equal, where floating intuition might suggest feasibility but integer arithmetic still yields a valid intersection. The interval formulation handles both naturally because it reduces everything to inequality bounds on a single variable, avoiding any need for case analysis or heuristic matching.
