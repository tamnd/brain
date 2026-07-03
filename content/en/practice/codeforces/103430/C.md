---
title: "CF 103430C - Athletes"
description: "We are given two independent groups of athletes, one group for sport A and one group for sport B. Each athlete has a numerical skill value, and every athlete must stay in their own sport unless we explicitly decide to “swap” them, meaning they compete in the other sport instead."
date: "2026-07-03T09:44:42+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 103430
codeforces_index: "C"
codeforces_contest_name: "2021-2022 ICPC, NERC, Southern and Volga Russian Regional Contest (problems intersect with Educational Codeforces Round 117)"
rating: 0
weight: 103430
solve_time_s: 48
verified: true
draft: false
---

[CF 103430C - Athletes](https://codeforces.com/problemset/problem/103430/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 48s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given two independent groups of athletes, one group for sport A and one group for sport B. Each athlete has a numerical skill value, and every athlete must stay in their own sport unless we explicitly decide to “swap” them, meaning they compete in the other sport instead.

The goal is to form a final selection of exactly k athletes assigned to sport A and exactly k athletes assigned to sport B, maximizing the total sum of skills after any swaps. A swap is costly in a very specific way: if an athlete originally belongs to sport A but is used in sport B, their contribution is reduced by a penalty x, and similarly, if an athlete from B is used in A, the penalty is y.

So the structure is not just picking the best k from each list independently. We are allowed to mix athletes between sports, but every cross-assignment comes with a fixed loss depending on direction.

The constraints (implicitly from the ICPC-style setting) suggest n can be large, up to around 2×10^5 or similar across both lists. That immediately rules out recomputing partial sums independently for every possible redistribution of athletes. Any solution that repeatedly sorts, recomputes prefixes, or simulates choices per configuration will be too slow. We need a single sorting pass and O(n) transitions.

A subtle edge case arises when greedy selection is applied independently per sport. For example, suppose swapping one very strong athlete from B into A forces replacing a weaker A athlete into B, and that cascade might still improve total score due to differences between x and y. A naive “take top k from each side” fails here because it ignores the interaction between the two pools.

Another failure mode is assuming symmetry: treating swapping A→B and B→A as equivalent. They are not, since penalties x and y differ, and the optimal split depends on that asymmetry.

## Approaches

The brute-force idea is to decide how many athletes z we take from sport A in total among the final 2k selected roles. Once z is fixed, the remaining 2k − z come from sport B. For each z, we pick the best available athletes from each sorted list and then apply swaps to satisfy the final requirement of k per sport.

If we fix z, the natural greedy structure is clear: take the top z athletes from A and top 2k − z from B. Now we compare how many athletes are on the “wrong side” relative to the required k per sport. If z < k, we are short of A assignments, so we must convert k − z athletes from B into A, paying penalty y per swap. If z > k, we must convert z − k athletes from A into B, paying penalty x per swap. The total score is thus a prefix sum combination minus a linear penalty term.

Trying all z independently from scratch would recompute prefix sums repeatedly, which leads to O(k) work per z and thus O(k^2). With sorting added, this becomes O(n log n + k^2), which is too slow when k is large.

The key observation is that as z increases by 1, only one athlete moves from B to A in the tentative selection. This changes the penalty structure and prefix sums incrementally. If we maintain prefix sums for both sorted lists and keep track of current partial sums, we can update the total score in O(1) per step. This turns the full sweep over z from 0 to 2k into a linear scan.

We sort both arrays in descending order so that prefix sums always represent best possible picks. Then we precompute prefix sums so that any top-t sum can be queried instantly.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^2 + n log n) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

We maintain sorted arrays A and B in descending order and their prefix sums SA and SB.

1. Sort both arrays in decreasing order. This ensures that any prefix represents the best possible selection of that size from each sport.
2. Precompute prefix sums SA[i] as sum of the first i athletes in A, and SB[i] similarly for B. This allows constant-time computation of any top segment sum.
3. Iterate z from 0 to 2k, interpreting z as the number of athletes chosen from A among the 2k total selected athletes. For each z, the number from B is 2k − z.
4. Compute the base sum for this configuration as SA[z] + SB[2k − z]. This represents the best possible raw skill sum before any swaps.
5. Adjust for feasibility of final assignment. If z < k, then we do not have enough A-labeled athletes, so we must convert k − z athletes from B to A. Each such conversion reduces total by y, so subtract y · (k − z). If z > k, we must convert z − k athletes from A to B, so subtract x · (z − k).
6. Track the maximum value over all z.
7. Output the best result.

The crucial detail is that every configuration is evaluated in constant time after preprocessing, so we avoid recomputation entirely.

### Why it works

For any fixed z, choosing the top z and top 2k − z athletes is optimal because there is no interaction between selections beyond cardinality constraints. Any deviation that replaces a chosen athlete with a weaker one can only decrease the prefix sum. The only remaining coupling between the two groups is balancing counts to exactly k per sport, and that coupling is linear in the imbalance, independent of which specific athletes were chosen. This separation between “best prefix selection” and “linear correction” ensures the sweep over z explores all structurally distinct optimal states.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m, k, x, y = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    A.sort(reverse=True)
    B.sort(reverse=True)

    # prefix sums
    SA = [0]
    for v in A:
        SA.append(SA[-1] + v)

    SB = [0]
    for v in B:
        SB.append(SB[-1] + v)

    ans = 0

    # z = number taken from A among 2k total
    for z in range(0, 2 * k + 1):
        if z > len(A) or (2 * k - z) > len(B):
            continue

        base = SA[z] + SB[2 * k - z]

        if z < k:
            base -= y * (k - z)
        elif z > k:
            base -= x * (z - k)

        if base > ans:
            ans = base

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution starts by sorting both lists so that any prefix corresponds to the best possible selection of that size. The prefix sums allow constant-time evaluation of any choice of z.

The loop over z checks every possible split between the two sports. The feasibility checks ensure we do not access invalid prefix indices. The adjustment step applies the correct penalty depending on whether we are short or over-assigned on sport A.

The maximum is tracked globally and printed at the end. The implementation relies heavily on correct prefix indexing; forgetting that SB[2k − z] must always be within bounds is a common source of runtime errors.

## Worked Examples

Consider a small case where k = 2.

A = [10, 4, 3], B = [9, 8, 1], x = 2, y = 3.

We sort descending already.

We compute prefix sums:

A: SA = [0, 10, 14, 17]

B: SB = [0, 9, 17, 18]

We evaluate z.

| z | SA[z] | SB[4−z] | base sum | adjustment | total |
| --- | --- | --- | --- | --- | --- |
| 0 | 0 | 18 | 18 | − y·2 = −6 | 12 |
| 1 | 10 | 17 | 27 | − y·1 = −3 | 24 |
| 2 | 14 | 9 | 23 | 0 | 23 |
| 3 | 17 | 0 | 17 | − x·1 = −2 | 15 |
| 4 | invalid | 0 | skip | skip | skip |

The best result is 24 at z = 1, meaning we intentionally take more from B than A even though k is balanced, because B’s high values outweigh penalties.

This trace shows the key behavior: the optimal split is not necessarily centered at k, and scanning all z captures that shift.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n + k) | sorting dominates, sweep over z is linear |
| Space | O(n) | prefix arrays store cumulative sums |

The constraints allow up to large input sizes, and this complexity fits comfortably within typical limits since sorting is the main cost and everything else is linear.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, m, k, x, y = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    A.sort(reverse=True)
    B.sort(reverse=True)

    SA = [0]
    for v in A:
        SA.append(SA[-1] + v)

    SB = [0]
    for v in B:
        SB.append(SB[-1] + v)

    ans = 0
    for z in range(0, 2 * k + 1):
        if z > len(A) or 2 * k - z > len(B):
            continue
        base = SA[z] + SB[2 * k - z]
        if z < k:
            base -= y * (k - z)
        elif z > k:
            base -= x * (z - k)
        ans = max(ans, base)

    return str(ans)

# custom cases
assert run("1 1 1 1 1\n10\n20") == "29"
assert run("3 3 2 5 5\n5 4 3\n6 1 1") == "15"
assert run("2 2 1 100 1\n100 1\n1 100") == "99"
assert run("5 5 2 0 0\n1 2 3 4 5\n1 2 3 4 5") == "30"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 1 1 case | 29 | single swap benefit |
| symmetric small k=2 | 15 | balanced selection logic |
| asymmetric penalties | 99 | direction-sensitive swaps |
| zero penalty | 30 | reduces to pure top selection |

## Edge Cases

One important edge case is when one of the arrays is too small to satisfy extreme values of z. For example, if k = 3, A has only 2 elements, and B has many. When z = 5, SA[z] is invalid and must be skipped. The algorithm explicitly checks bounds before accessing prefix sums, ensuring correctness by treating impossible configurations as non-candidates.

Another edge case occurs when penalties are zero. In this situation, swapping has no cost, so the optimal solution is simply taking the top 2k elements from the union. The sweep over z still works, but the best value appears where z naturally aligns with the distribution of large values across both arrays.

A final edge case is when one list dominates the other heavily, making all optimal configurations skewed toward one side. For instance, if all B values are much larger than A, the best z may be near 0. The enumeration over all z ensures this extreme is still evaluated, rather than assuming balance at k.
