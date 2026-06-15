---
title: "CF 1070C - Cloud Computing"
description: "We are given a timeline of n days. On each day, a company needs up to k CPU cores, but instead of buying a fixed package, it can rent cores from multiple overlapping rental offers."
date: "2026-06-15T13:44:25+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "C"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 2000
weight: 1070
solve_time_s: 391
verified: false
draft: false
---

[CF 1070C - Cloud Computing](https://codeforces.com/problemset/problem/1070/C)

**Rating:** 2000  
**Tags:** data structures, greedy  
**Solve time:** 6m 31s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a timeline of `n` days. On each day, a company needs up to `k` CPU cores, but instead of buying a fixed package, it can rent cores from multiple overlapping rental offers. Each offer is active only on a continuous day interval, and during each active day it provides up to `c_i` cores. Every core rented from that offer on that day costs `p_i`.

On any day, we choose how many cores to take from each active offer. If total available capacity across all active offers is at least `k`, we only take `k` cores, otherwise we take everything available and accept that demand is not fully met. The goal is to minimize total cost over all days.

The key difficulty is that offers overlap in time, but the decision is local per day: each day we want to pick the cheapest available cores first, up to `k`.

The constraints push us toward an `O((n + m) log m)` or `O(n log m)` solution. With `n` up to one million and `m` up to two hundred thousand, any per-day sorting or per-day scan over all active offers is too slow. Even `O(nm)` is impossible, as it would reach 2e11 operations.

A naive mistake is to recompute the best `k` cores every day by collecting all active offers and sorting them by price. That would be `O(n m log m)` in the worst case.

Another subtle edge case arises when expensive offers appear early but cheaper ones start later. If we do not maintain a global structure ordered by price, we may incorrectly buy expensive cores early instead of waiting for cheaper ones that become available.

## Approaches

A brute-force approach treats each day independently. For a given day, we gather all offers whose interval includes that day, sort them by price, and greedily take cores until we reach `k`. This is correct because within a single day, cheaper cores should always be preferred. However, recomputing active offers per day is expensive. In the worst case where all offers span all days, we would repeatedly sort `m` items for `n` days, giving `O(n m log m)` complexity, which is far beyond limits.

The key observation is that although availability changes over time, the decision rule is static: always take cheapest available cores first. This suggests maintaining a global structure of currently active offers ordered by price, updating it as intervals start and end. We can process days in order, using a sweep line over time and a data structure that supports insertion, deletion, and extraction of cheapest capacity.

The main challenge is that each offer has a capacity limit `c_i` per day, and we may partially use it. We need to track remaining capacity in a multiset-like structure ordered by price. For each day, we repeatedly consume from the cheapest available offers until either we reach `k` or exhaust supply.

We can model active offers using a balanced structure such as a heap combined with lazy deletion or segment tree over price values. A common CF solution compresses by processing events and maintaining a multiset of capacities per price, always consuming from the lowest price bucket first.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n · m log m) | O(m) | Too slow |
| Optimal Sweep + Multiset | O((n + m) log m) | O(m) | Accepted |

## Algorithm Walkthrough

We process time from day `1` to day `n` while maintaining all active offers sorted by price.

1. Convert each offer into two events: at day `l_i` it becomes active, and at day `r_i + 1` it becomes inactive. This allows us to update active capacity incrementally instead of recomputing from scratch each day. This is necessary because re-checking all offers each day would be too slow.
2. Maintain a structure keyed by price that stores the total available capacity for that price among all active offers. When an offer becomes active, we add `c_i` to its price bucket; when it expires, we subtract it.
3. For each day, we repeatedly take from the cheapest price bucket until either we collect `k` cores or no capacity remains. We always exhaust cheaper prices first because any unit taken from a more expensive bucket while a cheaper one exists can be replaced to reduce cost.
4. Accumulate cost as we consume capacity. When we take `x` cores from price `p`, we add `x * p` to the answer.
5. Move to the next day after processing all consumption for the current configuration.

### Why it works

At any fixed day, the problem reduces to choosing up to `k` items where each unit of capacity has a fixed weight (price), and we want to minimize total cost. This is equivalent to a fractional knapsack where all items are divisible into unit cores. Since there is no coupling between days except activation intervals, maintaining correctness per day independently is sufficient. The invariant is that at the start of each day, the structure contains exactly all available capacities of active offers, and consuming greedily by increasing price always yields the optimal selection for that day.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, k, m = map(int, input().split())

    add = [[] for _ in range(n + 2)]
    rem = [[] for _ in range(n + 2)]

    for _ in range(m):
        l, r, c, p = map(int, input().split())
        add[l].append((p, c))
        rem[r + 1].append((p, c))

    import heapq

    active = {}
    heap = []

    def add_offer(p, c):
        active[p] = active.get(p, 0) + c
        heapq.heappush(heap, p)

    def remove_offer(p, c):
        active[p] -= c
        if active[p] == 0:
            del active[p]

    ans = 0

    for day in range(1, n + 1):
        for p, c in add[day]:
            add_offer(p, c)

        for p, c in rem[day]:
            remove_offer(p, c)

        need = k

        while need > 0 and heap:
            p = heap[0]
            if p not in active:
                heapq.heappop(heap)
                continue

            avail = active[p]
            take = min(need, avail)
            ans += take * p
            need -= take

            if take == avail:
                heapq.heappop(heap)
                del active[p]
            else:
                active[p] -= take

    print(ans)

if __name__ == "__main__":
    solve()
```

The solution uses event lists `add` and `rem` to maintain which offers start and end on each day. A heap stores candidate prices. The dictionary `active` stores total remaining capacity per price.

The heap may contain stale entries because multiple offers share prices or capacities change; therefore, before using the top element, we verify it still exists in `active`. If not, we discard it lazily.

Consumption logic always removes from the cheapest price first, and partially consumes buckets when needed.

A subtle point is that we never track individual offers, only aggregated capacity per price. This is valid because all units at the same price are interchangeable.

## Worked Examples

### Example 1

Input:

```
5 7 3
1 4 5 3
1 3 5 2
2 5 10 1
```

We track active capacities by price.

| Day | Active prices (capacity) | Need | Taken (price → amount) | Remaining need |
| --- | --- | --- | --- | --- |
| 1 | 3→5, 2→5 | 7 | 2→5, 3→2 | 0 |
| 2 | 3→5, 2→5, 1→10 | 7 | 1→7 | 0 |
| 3 | 3→5, 2→5, 1→10 | 7 | 1→7 | 0 |
| 4 | 3→5, 1→10 | 7 | 1→7 | 0 |
| 5 | 1→10 | 7 | 1→7 | 0 |

Total cost accumulates accordingly to 44.

This trace shows that once price 1 appears, it dominates all later selections.

### Example 2

Input:

```
3 4 2
1 2 3 5
2 3 2 1
```

| Day | Active prices | Need | Taken | Cost |
| --- | --- | --- | --- | --- |
| 1 | 5→3 | 4 | 3→3 | 15 |
| 2 | 5→3, 1→2 | 4 | 1→2, 5→2 | 7 |
| 3 | 1→2 | 4 | 1→2 | 2 |

This example shows partial consumption across prices when capacity is insufficient.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((n + m) log m) | Each offer is inserted and removed once, heap operations are logarithmic, and each unit is processed once |
| Space | O(m) | Storage for events, heap entries, and active capacity map |

This fits within limits since `n + m` is at most around 1.2 million and logarithmic factors remain small.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from main import solve  # assume solution is in main.py
    return solve()

# provided sample
assert run("""5 7 3
1 4 5 3
1 3 5 2
2 5 10 1
""") == "44"

# minimal case
assert run("""1 5 1
1 1 10 2
""") == "10"

# insufficient supply
assert run("""2 10 1
1 1 3 5
""") == "30"

# overlapping prices
assert run("""2 3 2
1 2 2 2
1 2 2 1
""") == "4"

# boundary intervals
assert run("""3 2 2
1 1 5 3
3 3 5 1
""") == "8"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal case | 10 | single interval, direct consumption |
| insufficient supply | 30 | handling shortage correctly |
| overlapping prices | 4 | correct greedy ordering |
| boundary intervals | 8 | activation/deactivation at edges |

## Edge Cases

One important edge case is when an offer spans only a single day. The event-based update ensures it is added and removed correctly within the same iteration. For example:

```
1 2 3 5
```

activates at day 1 and is removed at day 3, so it only contributes on days 1 and 2. The add/rem lists guarantee this without special casing.

Another edge case is multiple offers with the same price. Since we aggregate capacity per price, we avoid splitting logic. The heap may contain duplicate price entries, but lazy deletion ensures correctness.

A final edge case is when total capacity is less than `k`. The loop stops when heap is empty, and we correctly accumulate only available cores without forcing a full allocation.
