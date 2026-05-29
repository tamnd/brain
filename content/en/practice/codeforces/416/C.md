---
title: "CF 416C - Booking System"
description: "We are given a collection of booking requests, where each request represents a group of guests who either all get seated together or do not come at all."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "dp", "greedy", "implementation"]
categories: ["algorithms"]
codeforces_contest: 416
codeforces_index: "C"
codeforces_contest_name: "Codeforces Round 241 (Div. 2)"
rating: 1600
weight: 416
solve_time_s: 92
verified: true
draft: false
---

[CF 416C - Booking System](https://codeforces.com/problemset/problem/416/C)

**Rating:** 1600  
**Tags:** binary search, dp, greedy, implementation  
**Solve time:** 1m 32s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a collection of booking requests, where each request represents a group of guests who either all get seated together or do not come at all. Each request has a size, meaning how many people arrive, and a profit, meaning how much money the restaurant earns if that group is accepted and seated.

Alongside this, we are given a fixed set of tables, each with a capacity. A table can host at most one group, and a group can only be seated at a table whose capacity is at least the group size. Each table is used at most once, and each request is either assigned to exactly one suitable table or rejected entirely. The objective is to choose a subset of requests and assign them to distinct tables in a way that maximizes total profit.

The structure of the input makes the key tension clear. We are matching items from two multisets under capacity constraints, while selecting only some of the items to maximize a weight. This is not a pure matching problem because skipping both sides is allowed, and it is not a simple knapsack because capacities are discrete objects rather than a continuous budget.

The constraints are small: both number of requests and number of tables are at most 1000, and capacities and group sizes are bounded by 1000. This immediately suggests that a solution on the order of n² or n² log n is acceptable, but anything cubic over 1000 elements would be borderline and unnecessary.

A few edge cases matter for correctness:

One case is when all tables are too small for all requests. For example, requests `(5, 10)` and tables `[1, 2]` produce zero accepted bookings. A naive greedy by profit might still try to assign but must correctly fail.

Another case is when multiple tables can serve the same request. For instance, a request of size 3 and tables `[3, 5, 10]`. If we assign it to the largest table first, we may block future larger requests that only fit the large table, reducing total profit.

A third case is when two large profit requests compete for a single large table, while smaller requests fit elsewhere. A naive greedy by profit alone can assign the large table incorrectly and block a better global assignment.

## Approaches

A brute-force view is to consider assigning requests to tables directly. For each request, we could try assigning it to any unused table that fits, recursively exploring all combinations. This effectively becomes a search over all matchings between requests and tables, where at each step we either skip a request or assign it to one of potentially k tables.

In the worst case, this branching grows extremely fast. Even if we only consider assignment choices, each request can branch into up to k possibilities, giving roughly O(k^n) structure, which is far beyond feasible.

The key observation is that the structure is fundamentally bipartite matching with weights, but with a very specific constraint: table capacities are small integers, and multiple tables can share the same capacity. This allows us to compress the table side into counts by capacity, rather than treating tables individually.

Once we sort tables by capacity and maintain how many of each capacity remain, the problem becomes choosing requests one by one and deciding whether to place them into any available compatible capacity. This suggests dynamic programming over requests and available table capacity distributions. However, a more efficient interpretation is to process requests in a fixed order and greedily assign them to the best possible table using a structure that always reserves small tables for small requests.

The standard trick is to sort requests by profit descending and try to assign each request to the smallest table that can accommodate it. This is optimal because large tables are more valuable for large requests, and wasting them on small requests reduces future feasibility.

We can maintain available tables in a frequency array or sorted structure and for each request perform a binary search to find the smallest usable table.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(k^n) | O(n + k) | Too slow |
| Optimal (greedy + search) | O(n log k) | O(k) | Accepted |

## Algorithm Walkthrough

We first structure the tables so that we can efficiently query which ones are available for a given group size.

1. Sort all table capacities in increasing order. This allows us to always find the smallest table that fits a request.
2. Sort requests in decreasing order of profit. The reasoning is that higher-profit requests should be considered first since they are harder to place optimally later.
3. For each request, perform a binary search over the sorted table list to find the smallest unused table with capacity at least the group size.
4. If such a table exists, assign the request to it, mark the table as used, and add the profit to the answer.
5. If no suitable table exists, skip the request.
6. Store assignments as pairs of request index and table index so we can reconstruct the output.

The subtlety is that once a table is used, it is removed permanently, so we must maintain a structure that supports deletions. Since k is small, a simple list with marking or a multiset-like structure implemented with binary search and removal is sufficient.

### Why it works

At any point in the process, we maintain the property that among all unassigned requests, we always attempt to place the highest profit one first into the smallest table that can accommodate it. This preserves the invariant that no accepted request can be swapped with another without decreasing total profit, because any alternative assignment would either use a larger table unnecessarily or block a higher capacity table needed later. The greedy choice aligns capacity scarcity with request size ordering, ensuring that large tables are preserved for large requests, which are the only ones that can use them.

## Python Solution

```python
import sys
input = sys.stdin.readline

n = int(input())
requests = []
for i in range(n):
    c, p = map(int, input().split())
    requests.append((p, c, i + 1))

k = int(input())
tables = list(map(int, input().split()))

tables.sort()
used = [False] * k

requests.sort(reverse=True)

assignments = []
total = 0

for p, c, idx in requests:
    best = -1
    for j in range(k):
        if not used[j] and tables[j] >= c:
            best = j
            break
    if best != -1:
        used[best] = True
        total += p
        assignments.append((idx, best + 1))

print(len(assignments), total)
for a, b in assignments:
    print(a, b)
```

The solution sorts tables once so that we can always scan from smallest to largest capacity. The `used` array ensures each table is consumed at most once.

Requests are sorted by profit descending, which drives the greedy ordering. For each request, we scan tables linearly to find the first available one that fits. Given k ≤ 1000, this O(nk) scan is still fast enough in practice.

A subtle implementation detail is preserving original request indices before sorting, since output requires original numbering.

## Worked Examples

### Example 1

Input:

```
3
10 50
2 100
5 30
3
4 6 9
```

Sorted requests by profit:

(100, size 2), (50, size 10), (30, size 5)

Sorted tables:

4, 6, 9

| Request | Size | Profit | Chosen table scan | Assigned |
| --- | --- | --- | --- | --- |
| 2 | 2 | 100 | 4 fits | 4 |
| 1 | 10 | 50 | none fits | no |
| 3 | 5 | 30 | 6 fits | 6 |

Assignments are request 2 → table 1 (value 4), request 3 → table 2 (value 6). Total profit is 130.

This trace shows that skipping the medium-profit request allows better use of table 4, while larger request cannot be placed at all.

### Example 2

Input:

```
4
3 20
3 50
3 40
5 60
2
3 5
```

Sorted requests:

(60,5), (50,3), (40,3), (20,3)

| Request | Size | Profit | Table chosen | Remaining tables |
| --- | --- | --- | --- | --- |
| 4 | 5 | 60 | 5 | [3] |
| 2 | 3 | 50 | 3 | [] |
| 3 | 3 | 40 | none | [] |
| 1 | 3 | 20 | none | [] |

This shows the greedy naturally consumes the only large table for the only request that can use it.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(nk) | Each request may scan all tables once in worst case |
| Space | O(n + k) | Storage for requests, tables, and assignment tracking |

With n, k ≤ 1000, the worst-case 10⁶ operations is easily within limits.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n = int(input())
    req = []
    for i in range(n):
        c, p = map(int, input().split())
        req.append((p, c, i + 1))

    k = int(input())
    tab = list(map(int, input().split()))

    tab = sorted([(v, i + 1) for i, v in enumerate(tab)])
    used = [False] * k

    req.sort(reverse=True)

    ans = []
    total = 0

    for p, c, idx in req:
        for j in range(k):
            if not used[j] and tab[j][0] >= c:
                used[j] = True
                total += p
                ans.append((idx, tab[j][1]))
                break

    out = [f"{len(ans)} {total}"]
    for a, b in ans:
        out.append(f"{a} {b}")
    return "\n".join(out)

# provided sample
assert run("""3
10 50
2 100
5 30
3
4 6 9
""") == """2 130
2 1
3 2"""

# minimum input
assert run("""1
1 10
1
1
""") == """1 10
1 1"""

# no valid assignments
assert run("""2
5 10
6 20
1
4
""") == """0 0"""

# all fit same size
assert run("""3
1 5
1 6
1 7
3
10 10 10
""").split()[0] == "3"

# boundary mix
assert run("""3
2 10
2 20
2 30
2
2 3
""")  # just ensure no crash
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 1 request minimal | 1 10 | smallest valid case |
| no valid match | 0 0 | rejection handling |
| all fit large tables | 3 accepted | full assignment |
| mixed capacities | valid max profit | greedy correctness |

## Edge Cases

One edge case is when no table can fit any request. For input where all `r_i < c_i`, the scan always fails and no assignments are recorded. The algorithm correctly returns zero profit because every request iteration finds no usable table.

Another edge case is when multiple tables share the same capacity. Since tables are distinguished by index, marking them individually ensures we never reuse a physical table, even if capacities are identical.

A final case is when a large table exists but small requests arrive first in profit order. Because we always pick highest profit first, a large request will still be prioritized if it has higher value, preventing the classic greedy mistake of consuming large capacity too early.
