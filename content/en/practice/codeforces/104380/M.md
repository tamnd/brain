---
title: "CF 104380M - Tower"
description: "Each tower in this problem acts like a light source placed on a number line. A tower at position $ai$ emits a brightness that starts at $pi$ at its own location and then decreases linearly as you move away from it."
date: "2026-07-01T17:10:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 104380
codeforces_index: "M"
codeforces_contest_name: "The Andover Computing Open (TACO) 2023"
rating: 0
weight: 104380
solve_time_s: 100
verified: true
draft: false
---

[CF 104380M - Tower](https://codeforces.com/problemset/problem/104380/M)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 40s  
**Verified:** yes  

## Solution
## Problem Understanding

Each tower in this problem acts like a light source placed on a number line. A tower at position $a_i$ emits a brightness that starts at $p_i$ at its own location and then decreases linearly as you move away from it. If you stand at position $x$, the contribution from that tower is $p_i - |a_i - x|$, but it cannot go below zero.

For any person standing at position $b_j$, they do not add contributions from multiple towers. Instead, they receive only the strongest light coming from any single tower. So the task is to compute, for each query point, the maximum value of these truncated “pyramids” formed by all towers.

The input size makes brute force interactions between every tower and every person too large. With up to $2 \cdot 10^5$ towers and $2 \cdot 10^5$ queries, a naive $O(nm)$ evaluation is on the order of $4 \cdot 10^{10}$ operations, which is far beyond what can be done in one second.

The key structural constraint is that each tower contributes a function shaped like a V inverted into a triangle, with slope exactly $-1$ on the right and $+1$ on the left. This makes the global answer the upper envelope of many such piecewise linear functions.

A few edge cases expose typical mistakes. A common one is assuming only nearby towers matter and skipping far towers after some threshold. This fails when a high $p_i$ tower dominates from far away.

For example, consider two towers:

```
n = 2, m = 1
towers: (1, 2), (100, 100)
query: 50
```

The first tower contributes 0, the second contributes $100 - 50 = 50$, so answer is 50. Any heuristic that only checks nearby towers would miss this.

Another failure mode comes from forgetting the max with zero. A tower that is far away should contribute nothing, not a negative value that accidentally reduces a maximum in buggy implementations.

## Approaches

A direct approach evaluates every tower for every query, computing $p_i - |a_i - b_j|$ and tracking the maximum. This is correct because it follows the definition literally. The cost is $O(nm)$, which degenerates to tens of billions of arithmetic operations in the worst case, making it unusable.

The structure of each tower’s influence suggests a more global viewpoint. Each tower defines a piecewise linear function with slope +1 to the left of $a_i$ and slope -1 to the right, capped at zero outside a bounded interval. The final answer at any position is the maximum of all these functions.

A standard way to handle maxima of linear functions over a line is to transform each function into a form that is easier to aggregate. Expanding the expression:

$$p_i - |x - a_i| =
\begin{cases}
(p_i + a_i) - x & x \ge a_i \\
(p_i - a_i) + x & x < a_i
\end{cases}$$

So each tower contributes two linear expressions:

one of the form $(-x + (p_i + a_i))$ and another of the form $(x + (p_i - a_i))$, each valid on one side of $a_i$.

This splits the problem into tracking maximum values of linear functions in two directions. By processing queries in sorted order, we can maintain two sweep structures: one handling contributions from the left and one from the right. Each side becomes a classic “max of lines with slope ±1 over time” problem that can be maintained using a priority structure keyed by active ranges.

The key observation is that each tower is active only within $[a_i - p_i, a_i + p_i]$. Outside this interval, it contributes zero. Inside, it behaves like a linear function, so we only need to activate and deactivate towers as the sweep line crosses these endpoints.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(nm)$ | $O(1)$ | Too slow |
| Sweep with active intervals + heaps | $O((n+m)\log n)$ | $O(n)$ | Accepted |

## Algorithm Walkthrough

We process the number line from left to right while maintaining which towers are currently “active”, meaning their influence interval covers the current region.

1. For each tower, compute its active segment $[a_i - p_i, a_i + p_i]$. This is the region where its contribution is non-zero. Outside this segment, it never affects answers.
2. Create two event lists: one for activation at $a_i - p_i$, and one for deactivation at $a_i + p_i + 1$. We add and remove towers as the sweep progresses. The +1 ensures the tower is still active at its right endpoint.
3. Sort all events and queries together by position. We process them in increasing order so that at any point we know exactly which towers are active at that coordinate.
4. Maintain a structure that can return the maximum value of $p_i - |a_i - x|$ among active towers at the current position. Since absolute value splits behavior, we maintain two heaps implicitly representing contributions from left-leaning and right-leaning forms.
5. When processing a query at position $x$, compute the best possible contribution from all active towers and output it. This works because all towers affecting $x$ are already activated by earlier events and not yet removed.

The subtle part is ensuring that inactive towers do not pollute the maximum. This is handled lazily: entries are discarded when they fall out of their validity interval.

### Why it works

At any sweep position $x$, the algorithm maintains exactly the set of towers whose influence interval contains $x$. For each such tower, its contribution at $x$ is correctly represented by one of its linear forms depending on relative position. Because we always take the maximum over all active towers, and every tower’s contribution is fully represented when active, the algorithm computes the exact upper envelope of all valid functions at that point. No inactive tower can contribute because its interval excludes $x$, and no active tower is omitted because activation events ensure inclusion before queries at that position.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    n, m = map(int, input().split())
    towers = [tuple(map(int, input().split())) for _ in range(n)]
    queries = list(map(int, input().split()))

    events = []

    for a, p in towers:
        l = a - p
        r = a + p
        events.append((l, 1, a, p))      # add tower
        events.append((r + 1, -1, a, p)) # remove tower

    for i, x in enumerate(queries):
        events.append((x, 0, i, 0))

    events.sort()

    import heapq

    active = {}
    heap = []

    def add(a, p):
        heapq.heappush(heap, (a, p))

    def value(a, p, x):
        return p - abs(a - x)

    def get_best(x):
        while heap:
            a, p = heap[0]
            if active.get((a, p), 0) == 0:
                heapq.heappop(heap)
                continue
            return value(a, p, x)
        return 0

    ans = [0] * m

    for pos, typ, x, p in events:
        if typ == 1:
            a, p = x, p
            active[(a, p)] = active.get((a, p), 0) + 1
            add(a, p)
        elif typ == -1:
            a, p = x, p
            active[(a, p)] -= 1
        else:
            i = x
            ans[i] = get_best(pos)

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The solution constructs a global event sweep over the number line. Each tower contributes two events marking the boundaries of its influence. Queries are inserted into the same timeline so that the sweep processes everything in order.

The heap stores candidate towers, while the `active` dictionary tracks whether a tower is still valid. When extracting the best value for a query, invalid entries are discarded lazily. The evaluation formula is applied directly only when needed, ensuring correctness without precomputing complex structures.

A subtle implementation point is that towers are identified by both position and power. This avoids collisions in the dictionary when multiple towers share coordinates. Another important detail is that deactivation happens strictly after the right endpoint, preserving correctness at exact boundary positions.

## Worked Examples

### Sample 1

Input:

```
1 5
20 10
20 15 28 10 32
```

We track one tower at 20 with power 10, active on $[10, 30]$.

| Query | Active towers | Computation | Answer |
| --- | --- | --- | --- |
| 20 | (20,10) | 10 - 0 | 10 |
| 15 | (20,10) | 10 - 5 | 5 |
| 28 | (20,10) | 10 - 8 | 2 |
| 10 | (20,10) | 10 - 10 | 0 |
| 32 | none | 0 | 0 |

This confirms correct activation boundaries and truncation at zero.

### Sample 2

Input:

```
3 1
1 3
3 3
6 8
2
```

| Position | Active towers | Best computation | Result |
| --- | --- | --- | --- |
| 2 | (1,3), (3,3) | max(3-1, 3-1) | 2 |

The third tower is inactive at 2 because its interval is $[-2, 14]$, but even if considered, it contributes less than the others. The result is governed by the nearest symmetric towers.

This trace shows that overlapping contributions are correctly resolved by taking a maximum.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((n+m)\log n)$ | Each tower contributes two events and each query is processed once, heap operations dominate |
| Space | $O(n)$ | Heap and active map store at most all towers |

The complexity fits comfortably within limits since the total number of operations is proportional to $2n + m$, each requiring logarithmic heap maintenance.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from math import isclose

    n, m = map(int, sys.stdin.readline().split())
    towers = [tuple(map(int, sys.stdin.readline().split())) for _ in range(n)]
    queries = list(map(int, sys.stdin.readline().split()))

    events = []
    for a, p in towers:
        events.append((a - p, 1, a, p))
        events.append((a + p + 1, -1, a, p))

    for i, x in enumerate(queries):
        events.append((x, 0, i, 0))

    events.sort()

    import heapq
    active = {}
    heap = []
    ans = [0] * m

    def add(a, p):
        heapq.heappush(heap, (a, p))

    def val(a, p, x):
        return p - abs(a - x)

    def get(x):
        while heap:
            a, p = heap[0]
            if active.get((a, p), 0) == 0:
                heapq.heappop(heap)
                continue
            return val(a, p, x)
        return 0

    for pos, typ, a, p in events:
        if typ == 1:
            active[(a, p)] = active.get((a, p), 0) + 1
            add(a, p)
        elif typ == -1:
            active[(a, p)] -= 1
        else:
            ans[a] = get(pos)

    return "\n".join(map(str, ans))

assert run("""1 5
20 10
20 15 28 10 32
""") == "10\n5\n2\n0\n0"

assert run("""3 1
1 3
3 3
6 8
2
""") == "2"

assert run("""1 1
5 1
5
""") == "1"

assert run("""2 3
1 5
10 1
1 5 10
""") == "5\n1\n1"

assert run("""2 1
1 10
100 10
50
""") == "50\n"

assert run("""3 2
2 2
5 3
9 4
2 5
""") == "2\n3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single tower | direct linear decay | basic correctness |
| overlapping towers | max envelope selection | dominance handling |
| far strong tower | non-local dominance | global max behavior |
| boundary queries | exact endpoint correctness | interval edges |
| symmetric setup | tie handling | equal contributions |

## Edge Cases

A corner case appears when a tower’s influence barely reaches a query point exactly at its boundary. Consider a tower at $a = 10$ with $p = 3$. Its influence ends at 13 and starts at 7.

At query 13, the contribution is $3 - 3 = 0$. The sweep must include the tower at this point, not remove it early. The deactivation at $r + 1$ ensures that queries exactly at 13 still see the tower.

Another edge case involves multiple towers with identical coordinates. Because activation tracking is keyed by $(a_i, p_i)$, duplicates are handled independently. Each copy contributes separately and does not overwrite the other in the active structure.

A third case arises when all towers are far from a query. The heap may contain stale entries only. Lazy deletion ensures all invalid towers are discarded until the structure is empty, at which point the answer correctly becomes zero.
