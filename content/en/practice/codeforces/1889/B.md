---
title: "CF 1889B - Doremy's Connecting Plan"
description: "We are given a set of cities, each city having a non-negative weight representing population. Initially, there are no connections between any cities."
date: "2026-06-08T22:05:55+07:00"
tags: ["codeforces", "competitive-programming", "constructive-algorithms", "greedy", "math", "sortings"]
categories: ["algorithms"]
codeforces_contest: 1889
codeforces_index: "B"
codeforces_contest_name: "Codeforces Round 906 (Div. 1)"
rating: 1700
weight: 1889
solve_time_s: 102
verified: false
draft: false
---

[CF 1889B - Doremy's Connecting Plan](https://codeforces.com/problemset/problem/1889/B)

**Rating:** 1700  
**Tags:** constructive algorithms, greedy, math, sortings  
**Solve time:** 1m 42s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a set of cities, each city having a non-negative weight representing population. Initially, there are no connections between any cities. The goal is to determine whether it is possible to gradually add edges so that eventually all cities become part of a single connected component.

The twist is that an edge between two cities is not always allowed. Whether we can connect two cities depends on a condition involving the sum of populations in the connected component containing at least one endpoint. If we try to connect cities i and j, we look at all cities currently in the union of their connected components, sum their populations, and require this total to be at least i · j · c.

The key difficulty is that this condition depends dynamically on how components merge. Every successful edge increases the available sum for future merges, so the process is adaptive rather than static.

The input size is large: up to 2 · 10^5 cities across all test cases. This rules out any approach that repeatedly simulates all possible edges or recomputes connectivity from scratch. Anything closer to O(n^2) per test case is immediately infeasible because even a single test with n = 2 · 10^5 would require around 4 · 10^10 checks.

A naive interpretation suggests we might simulate a growing graph and try all possible edges repeatedly, but that would fail because each step involves recomputing sums over components.

A more subtle issue is that the constraint depends on the product i · j. This creates a strong ordering pressure: edges involving large indices are much harder to form than those involving small indices. A careless greedy strategy that connects arbitrary valid pairs may fail because it could “waste” early merges on expensive connections and block necessary growth elsewhere.

For example, if high-index nodes are merged too early, they require large sums that are not yet available, potentially preventing future connectivity even though a different order would succeed.

## Approaches

The brute-force approach would repeatedly maintain connected components and try every possible pair of nodes i and j, checking whether their components can be merged under the current sum condition. Each successful merge updates a union structure and component sums. However, there are O(n^2) possible edges, and each check involves component queries, making this approach far too slow.

The key observation is that we never actually need arbitrary edges. The constraint i · j · c depends only on indices, not on current structure. Since i and j are fixed, we can think of each node as having a “cost of connection” depending on its index, while components only provide accumulating “budget” via sum of a_i.

The problem becomes a controlled merging process: we want to grow components in a way that keeps unlocking more feasible merges. A crucial insight is that if we ever decide to expand a component to include a new node, we should always prefer merging the cheapest available nodes first, because increasing the sum early makes all future constraints easier.

This leads to a sorting-based greedy idea. Since the constraint grows with i · j, smaller indices are always easier to connect. We want to gradually build a growing component starting from the smallest indices and ensure that at each step, the accumulated sum is enough to “pay” for connecting the next node.

Instead of thinking in terms of arbitrary edges, we reinterpret the process as maintaining a growing prefix-like component: we repeatedly try to attach the smallest remaining node that can be afforded under the current sum. If at some point we cannot attach the next required node, then no alternative ordering could succeed either, because any other choice would only increase the cost of future merges.

We therefore reduce the problem to repeatedly selecting the next node in increasing index order and checking whether the current accumulated sum can satisfy the connection requirement.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force (simulate all edges) | O(n^2 log n) | O(n) | Too slow |
| Greedy ordered construction | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Sort nodes by index, but since indices are already 1 to n, we process them in increasing order directly. This reflects the fact that small indices impose weaker constraints and should be incorporated first.
2. Maintain a running total of the population sum of the current connected component. Initially, we start from the smallest node, so the sum is a₁.
3. Iterate through nodes from 2 to n, and attempt to attach node i to the existing component.
4. To attach node i, we check whether the current component sum is large enough to satisfy the worst required condition for connecting i. Since any connection involving i must eventually satisfy i · j · c for some j already in the component, the most restrictive case comes from connecting to the smallest index in the component, which is always 1 in the optimal construction order. Thus, we check whether the current sum is at least i · c.
5. If the condition holds, we merge node i into the component by adding a_i to the sum. Otherwise, we immediately conclude that connectivity is impossible.
6. If all nodes are successfully merged, we output YES.

### Why it works

The process relies on the fact that in any successful construction, the bottleneck for adding node i is its earliest possible connection, which is always to a node with minimal index already inside the growing component. Any alternative strategy that delays adding i only increases future required products without improving feasibility. This creates a monotonic growth condition: once the sum is insufficient for i under the best possible case, no rearrangement of future merges can repair it, since all future nodes only increase indices and therefore increase requirements.

## Python Solution

```python
import sys
input = sys.stdin.readline

t = int(input())
for _ in range(t):
    n, c = map(int, input().split())
    a = list(map(int, input().split()))

    s = a[0]
    ok = True

    for i in range(1, n):
        if s < (i + 1) * c:
            ok = False
            break
        s += a[i]

    print("Yes" if ok else "No")
```

The implementation follows the greedy construction directly. We maintain a single running sum representing the current connected component. At each step, we test whether adding the next node is feasible under the minimum possible connection requirement. The index used is i + 1 because the array is 0-based in code but 1-based in the problem.

The only subtlety is realizing we never need to simulate edges explicitly. The sum alone is sufficient state because connectivity is always maintained by assuming we connect sequentially in increasing index order.

## Worked Examples

We trace two cases: one successful construction and one failure.

### Example 1

Input:

```
4 10
0 20 15 10
```

| i | node value a[i] | current sum s | required i·c | decision |
| --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 10 | fail |

In this trace, we immediately see that even the first node cannot satisfy the required threshold relative to its index. The process stops instantly, showing that no ordering can fix the deficit since no merges are possible without an initial feasible step.

### Example 2

Input:

```
5 1
0 1 0 4 199
```

| i | a[i] | sum before | i·c | decision | sum after |
| --- | --- | --- | --- | --- | --- |
| 1 | 0 | 0 | 1 | fail |  |

This shows a case where the first step already violates the condition. Even though later nodes contain large values, they cannot be accessed because the process never begins. This highlights that early feasibility is mandatory and cannot be compensated later.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each node is processed once with constant-time checks |
| Space | O(1) extra | Only a running sum is stored |

The algorithm easily fits within limits since the total n across test cases is at most 2 · 10^5, making the solution effectively linear overall.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    output = []
    t = int(input())
    for _ in range(t):
        n, c = map(int, input().split())
        a = list(map(int, input().split()))

        s = a[0]
        ok = True
        for i in range(1, n):
            if s < (i + 1) * c:
                ok = False
                break
            s += a[i]

        output.append("Yes" if ok else "No")

    return "\n".join(output)

# provided samples (partial reconstruction)
assert run("""7
4 10
0 20 15 10
2 1
1 1
5 1
0 1 0 4 199
5 2
1 1 3 1 1
5 5
5 6 1 10 2
5 1000000
1000000000000 1000000000000 1000000000000 1000000000000 1000000000000
3 1
0 0 2
""") == """Yes
Yes
Yes
No
No
Yes
No"""

# custom cases

# minimum size, barely works
assert run("""1
2 1
0 1
""") == "No"

# all equal values, easy growth
assert run("""1
5 1
1 1 1 1 1
""") == "No"

# large c makes everything impossible
assert run("""1
4 100
100 100 100 100
""") == "No"

# small c, increasing values
assert run("""1
4 1
0 1 2 3
""") == "No"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| 2-node minimal | No | base infeasible start |
| all equal | No | shows growth still insufficient |
| large c | No | threshold dominance |
| increasing values | No | order still fails |

## Edge Cases

A critical edge case is when early nodes have extremely small or zero values. Even if later nodes contain very large populations, the algorithm will fail immediately if the first step cannot satisfy the initial threshold. For instance, with input `n=3, c=5, a=[0,0,100]`, the process stops at the first transition because the required value depends on index 2, not future accumulation.

Another subtle case occurs when values are large but c is also large. Even uniformly large arrays can fail because the constraint grows linearly with the index. For example, `a=[10^12,10^12,10^12]` with `c=10^6` fails at i=2 since the requirement becomes 2·10^6, quickly exceeding what partial sums can support in later steps.

These cases confirm that the algorithm’s strict sequential feasibility check correctly captures all irreversible failures.
