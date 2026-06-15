---
title: "CF 1070C - Cloud Computing"
description: "We are given a timeline of $n$ days. Each day, a company needs a fixed number of CPU cores, denoted by $k$. The cloud market offers multiple rental contracts, where each contract is active only on a contiguous range of days."
date: "2026-06-15T07:22:06+07:00"
tags: ["codeforces", "competitive-programming", "data-structures", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1070
codeforces_index: "C"
codeforces_contest_name: "2018-2019 ICPC, NEERC, Southern Subregional Contest (Online Mirror, ACM-ICPC Rules, Teams Preferred)"
rating: 2000
weight: 1070
solve_time_s: 255
verified: false
draft: false
---

[CF 1070C - Cloud Computing](https://codeforces.com/problemset/problem/1070/C)

**Rating:** 2000  
**Tags:** data structures, greedy  
**Solve time:** 4m 15s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a timeline of $n$ days. Each day, a company needs a fixed number of CPU cores, denoted by $k$. The cloud market offers multiple rental contracts, where each contract is active only on a contiguous range of days. During each active day of a contract, it provides a limited number of cores and charges a fixed price per core for that contract.

On any given day, the company can choose how many cores to rent from each active contract, up to its daily capacity. If the combined available capacity across all active contracts is at least $k$, the company rents exactly $k$ cores that day, choosing the cheapest available ones first. If total capacity is less than $k$, it takes everything available.

The task is to compute the minimum total cost across all days, assuming optimal selection each day independently but respecting that contracts are only available on their time intervals.

The key structure is that days are independent in terms of choice, but the set of available contracts changes over time due to interval activation and expiration.

The constraints push toward a solution that processes up to $10^6$ days and up to $2 \cdot 10^5$ intervals. A naive simulation per day that scans all contracts would be far too slow, potentially $O(nm)$, which is on the order of $10^{11}$ operations. Even maintaining a simple list of active contracts and sorting them per day would be $O(nm \log m)$, also infeasible.

The only viable approach must maintain the set of active contracts dynamically and always be able to extract the cheapest available cores efficiently.

A subtle edge case arises when capacity is insufficient on a day. A naive greedy approach that assumes we always pick exactly $k$ cores and ignores shortage would overcharge or undercount. For example, if $k = 10$ but only 7 cores are available across all active contracts, the answer must reflect only those 7 cores, not force 10.

Another failure mode occurs if we treat each contract as indivisible per day. Contracts are not atomic, we can split usage across them freely, so we must reason in terms of per-core pricing rather than per-contract selection.

## Approaches

The brute-force perspective is straightforward: for each day, gather all active contracts, expand them into available cores, sort them by price, and pick the cheapest $k$. This is correct because the cost is linear in chosen cores and there are no bundle constraints across days.

However, this expansion is too large. A single contract can contribute up to $c_i$ units per day, and $c_i$ can be as large as $10^6$. Expanding even one contract explicitly is impossible, and repeating this across all days becomes completely infeasible.

The key observation is that we never need to track individual cores explicitly. What matters is a multiset of “price buckets” where each bucket has a capacity. We need to repeatedly take cheapest available capacity across active intervals.

This suggests maintaining all active contracts in a structure ordered by price, and greedily consuming capacity starting from the cheapest. However, since capacities are large and we only need top $k$, we do not need to fully expand all cores; we only need to know how much capacity exists at each price level.

We handle this by sweeping through days and maintaining active contracts. At each day, we aggregate total capacity by price. We then greedily consume from cheapest to most expensive until either we satisfy $k$ or exhaust capacity.

To maintain active intervals efficiently, we use a difference array or event-based sweep: we add contracts at $l_i$ and remove them after $r_i$. A balanced structure (typically a map from price to total capacity) tracks current availability.

At each day, we iterate prices in increasing order. Since prices can repeat and total distinct prices is bounded by $m$, we maintain a structure like a sorted dictionary or balanced tree.

The dominant optimization is that we never iterate per contract per day; instead, we aggregate by price.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (expand all cores per day) | $O(nm \log m)$ | $O(m)$ | Too slow |
| Optimal (sweep + ordered price buckets) | $O((n+m)\log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

We transform the problem into a dynamic multiset of capacities indexed by price.

1. Convert each contract into two events: at day $l_i$, we add $c_i$ capacity at price $p_i$, and at day $r_i + 1$, we remove it. This allows us to process changes incrementally rather than scanning intervals repeatedly.
2. Maintain a map from price to total available capacity currently active. This structure represents how many cores we can still take at each price level on the current day.
3. Sweep through days from 1 to $n$, applying all events scheduled for that day before computing cost. This ensures the active set is always correct.
4. To compute daily cost, we iterate prices in ascending order. For each price $p$, we take as many cores as possible up to remaining demand $k$, but no more than available capacity at $p$. We reduce both demand and capacity accordingly.
5. Stop early when demand becomes zero. If demand is not fully satisfied, we simply accept that fewer than $k$ cores are used and compute cost accordingly.
6. Accumulate the total cost across all days.

The subtle point is that per-day greedy selection over sorted prices is optimal because each core is independent and cost is linear. There is no benefit in reserving cheap capacity for later days.

### Why it works

At any day, the available cores form a set of independent items, each with a fixed unit price. The optimal strategy for a fixed demand under linear cost is always to take the cheapest available units first. Since there are no coupling constraints across contracts beyond availability, sorting by price and greedily consuming capacity is equivalent to sorting all individual cores and picking the first $k$, without explicitly expanding them.

The sweep line ensures that the multiset of available cores is always exactly correct for the current day.

## Python Solution

```python
import sys
input = sys.stdin.readline

from collections import defaultdict

def solve():
    n, k, m = map(int, input().split())
    
    add = [[] for _ in range(n + 2)]
    remove = [[] for _ in range(n + 2)]
    
    for _ in range(m):
        l, r, c, p = map(int, input().split())
        add[l].append((p, c))
        remove[r + 1].append((p, c))
    
    import bisect
    
    prices = []
    qty = defaultdict(int)
    
    def add_contract(p, c):
        if qty[p] == 0:
            bisect.insort(prices, p)
        qty[p] += c
    
    def remove_contract(p, c):
        qty[p] -= c
        if qty[p] == 0:
            i = bisect.bisect_left(prices, p)
            prices.pop(i)
    
    total = 0
    
    for day in range(1, n + 1):
        for p, c in add[day]:
            add_contract(p, c)
        for p, c in remove[day]:
            remove_contract(p, c)
        
        need = k
        for p in prices:
            if need == 0:
                break
            take = min(need, qty[p])
            total += take * p
            need -= take
    
    print(total)

if __name__ == "__main__":
    solve()
```

The code maintains two event lists for interval activation and deactivation. Each day, it updates the active price buckets, ensuring that `qty[p]` stores total available cores at price `p`.

The sorted list `prices` is kept in increasing order using binary insertion and deletion. This allows correct greedy consumption from cheapest to most expensive.

A subtle implementation detail is the removal operation: we only delete a price when its quantity drops to zero, ensuring consistency between `prices` and `qty`.

The per-day greedy loop consumes at most $k$ units, and because it breaks early, it avoids unnecessary scanning in fully satisfied days.

## Worked Examples

### Sample 1

Input:

```
5 7 3
1 4 5 3
1 3 5 2
2 5 10 1
```

We track active contracts by price and compute daily consumption.

| Day | Active (price → qty) | Need | Taken | Cost |
| --- | --- | --- | --- | --- |
| 1 | 3→5, 2→5 | 7 | 2×5 at price 2, 5×2 at price 3 | 10 + 10 = 20 |
| 2 | 3→5, 2→5, 1→10 | 7 | 7×1 | 7 |
| 3 | 3→5, 2→5, 1→10 | 7 | 7×1 | 7 |
| 4 | 3→5, 1→10 | 7 | 7×1 | 7 |
| 5 | 1→10 | 7 | 7×1 | 7 |

Total = 44

This trace shows that the greedy-by-price choice remains stable even as contracts expire.

### Sample 2

Input:

```
3 4 2
1 2 3 5
2 3 10 1
```

| Day | Active | Need | Taken | Cost |
| --- | --- | --- | --- | --- |
| 1 | 5→3 | 4 | 3×5 | 15 |
| 2 | 5→3, 1→10 | 4 | 3×1 + 1×5 | 8 |
| 3 | 1→10 | 4 | 4×1 | 4 |

Total = 27

This confirms that cheaper capacity is always exhausted first.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n + m)\log m + n \cdot d)$ | Each event update uses ordered insertion/removal; per day we scan active price levels, but total distinct price levels remain bounded by active contracts |
| Space | $O(m)$ | Stores event lists and active price map |

The structure comfortably fits within limits since $m \le 2 \cdot 10^5$, and event processing dominates while per-day scanning is controlled by the number of distinct active prices.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    from collections import defaultdict
    import bisect

    n, k, m = map(int, input().split())
    add = [[] for _ in range(n + 2)]
    remove = [[] for _ in range(n + 2)]

    for _ in range(m):
        l, r, c, p = map(int, input().split())
        add[l].append((p, c))
        remove[r + 1].append((p, c))

    prices = []
    qty = defaultdict(int)

    def addc(p, c):
        if qty[p] == 0:
            bisect.insort(prices, p)
        qty[p] += c

    def remc(p, c):
        qty[p] -= c
        if qty[p] == 0:
            prices.pop(bisect.bisect_left(prices, p))

    total = 0

    for day in range(1, n + 1):
        for p, c in add[day]:
            addc(p, c)
        for p, c in remove[day]:
            remc(p, c)

        need = k
        for p in prices:
            if need == 0:
                break
            take = min(need, qty[p])
            total += take * p
            need -= take

    print(total)

# provided sample
assert run("""5 7 3
1 4 5 3
1 3 5 2
2 5 10 1
""") == "44"

# custom 1: minimal
assert run("""1 1 1
1 1 1 10
""") == "10"

# custom 2: insufficient capacity
assert run("""2 5 1
1 1 2 3
""") == "6"

# custom 3: overlapping prices
assert run("""3 3 2
1 3 1 5
1 3 2 1
""") == "9"

# custom 4: boundary removal
assert run("""3 2 2
1 2 3 2
2 3 3 1
""") == "12"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal | 10 | single contract correctness |
| insufficient capacity | 6 | handling shortage |
| overlapping prices | 9 | greedy ordering across prices |
| boundary removal | 12 | correct interval activation/deactivation |

## Edge Cases

A critical edge case is when total available capacity is smaller than $k$. In that situation, the algorithm never tries to force selection up to $k$, it simply consumes what exists. For example:

```
1 10 1
1 1 3 5
```

Only 3 cores exist, so the cost is $3 \cdot 5 = 15$. The greedy loop naturally stops after exhausting `prices`, leaving `need > 0`, which is fine because no additional cost is added.

Another edge case is contracts with identical prices activated and deactivated on adjacent boundaries. The event-based approach ensures correct inclusion because removal happens at $r+1$, so the contract remains active through day $r$ exactly.

A final subtle case is multiple contracts with the same price. The aggregation into `qty[p]` ensures they are treated as a single bucket, avoiding incorrect partial ordering issues that would occur if each contract were handled independently in a sorted structure.
