---
title: "CF 1487E - Cheap Dinner"
description: "We have four layers of items. The first layer contains first courses, the second layer contains second courses, the third layer contains drinks, and the fourth layer contains desserts. Every item has a cost. Between every pair of adjacent layers, some combinations are forbidden."
date: "2026-06-10T23:01:56+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "graphs", "greedy", "implementation", "sortings", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 1487
codeforces_index: "E"
codeforces_contest_name: "Educational Codeforces Round 104 (Rated for Div. 2)"
rating: 2000
weight: 1487
solve_time_s: 144
verified: true
draft: false
---

[CF 1487E - Cheap Dinner](https://codeforces.com/problemset/problem/1487/E)

**Rating:** 2000  
**Tags:** brute force, data structures, graphs, greedy, implementation, sortings, two pointers  
**Solve time:** 2m 24s  
**Verified:** yes  

## Solution
## Problem Understanding

We have four layers of items.

The first layer contains first courses, the second layer contains second courses, the third layer contains drinks, and the fourth layer contains desserts. Every item has a cost.

Between every pair of adjacent layers, some combinations are forbidden. A first course may be incompatible with certain second courses, a second course may be incompatible with certain drinks, and a drink may be incompatible with certain desserts.

We must choose exactly one item from each layer. Every adjacent pair in the chosen sequence must be allowed. Among all valid dinners, we want the minimum possible total cost.

The most natural way to view the problem is as a layered graph. Each item is a vertex. Edges exist only between neighboring layers, and some of those edges are removed because they are forbidden. We need the cheapest path that starts in layer 1 and ends in layer 4, where the cost of a path is the sum of the costs of its vertices.

The constraints completely determine the direction of the solution. Each layer can contain up to 150,000 items, while each set of forbidden pairs contains at most 200,000 entries. A quadratic algorithm between layers is impossible. Even checking all pairs between two layers would require roughly $150000^2$ operations, which is far beyond the limit.

A useful observation is that the number of forbidden pairs is relatively small compared to the number of possible pairs. The input does not describe all allowed connections. Instead, it only lists the bad ones. That strongly suggests building a solution around forbidden sets rather than around all possible edges.

Several edge cases are easy to mishandle.

Consider a layer where every item becomes unreachable.

```
Layer A costs: [1]
Layer B costs: [2]
Forbidden: (A1,B1)
```

No valid transition exists. The correct value for the item in layer B is "impossible". If we accidentally keep its original cost, later layers may incorrectly build solutions through it.

Another subtle case occurs when the cheapest predecessor is forbidden but a more expensive one is available.

```
Previous layer values: [1, 5]
Current item forbids predecessor 1
```

The answer for this item is 5 plus its own cost, not infinity. A solution that only checks the globally cheapest predecessor would fail.

A third important case is when every predecessor of an item is forbidden.

```
Previous layer values: [3, 7]
Forbidden predecessors: {1, 2}
```

The item must become unreachable. Any implementation that forgets to detect this situation may accidentally reuse an invalid value.

## Approaches

The brute force approach tries every possible dinner.

For each first course, try every second course. For each valid pair, try every drink. For each valid triple, try every dessert. Whenever all adjacent pairs are allowed, compute the total cost and keep the minimum.

This approach is correct because it explicitly examines every valid dinner. Unfortunately, its complexity is

$$O(n_1 n_2 n_3 n_4)$$

which can be as large as

$$150000^4$$

and is completely infeasible.

We need to exploit the structure of the problem.

Suppose we already know the cheapest achievable cost for every item in one layer. We want to compute the cheapest achievable cost for every item in the next layer.

For a fixed item $v$ in the next layer,

$$dp[v] = cost[v] + \min(dp[u])$$

over all predecessors $u$ that are not forbidden with $v$.

The difficulty is finding that minimum efficiently.

A naive implementation would scan all predecessors for every item. That again becomes quadratic.

The key observation is that each item only forbids a relatively small number of predecessors overall. If we sort all predecessor values by cost, then for a given item we can walk through the sorted list from cheapest to most expensive and choose the first predecessor that is not forbidden.

Why is this efficient?

Each item only stores its forbidden predecessors. The number of forbidden pairs is at most 200,000. Since the sorted predecessor list is shared by all items, checking whether a candidate predecessor is forbidden is just a hash-set lookup.

For every item we search the sorted predecessor list until we find the first allowed predecessor. Because the total number of forbidden pairs is small, this process is fast enough.

We perform this transformation three times:

1. First courses → second courses.
2. Second courses → drinks.
3. Drinks → desserts.

After the last transformation, the answer is the minimum reachable value in the dessert layer.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | $O(n_1 n_2 n_3 n_4)$ | $O(1)$ | Too slow |
| Optimal | $O((N+M)\log N)$ | $O(N+M)$ | Accepted |

Here $N=n_1+n_2+n_3+n_4$ and $M=m_1+m_2+m_3$.

## Algorithm Walkthrough

Assume we know the best achievable costs for all items in a previous layer.

We need a procedure that computes the best achievable costs for the next layer.

### Transition Procedure

1. Sort all items of the previous layer by their current DP value.
2. For every item in the current layer, store the set of forbidden predecessors.
3. Process each current-layer item independently.
4. Scan the sorted predecessor list from cheapest to most expensive.
5. Find the first predecessor whose index is not present in the forbidden set of the current item.
6. If such a predecessor exists, add its DP value to the current item's own cost.
7. If no predecessor exists, mark the current item as unreachable using a very large value.

### Full Algorithm

1. Initialize the first layer's DP values to their costs.
2. Apply the transition procedure from layer 1 to layer 2.
3. Apply the transition procedure from layer 2 to layer 3.
4. Apply the transition procedure from layer 3 to layer 4.
5. Take the minimum DP value in the fourth layer.
6. If the minimum value is infinity, output `-1`. Otherwise output that minimum.

### Why it works

For any item in the current layer, every valid dinner ending at that item must come through some allowed predecessor.

The sorted predecessor list examines predecessors in increasing DP order. The first predecessor that is not forbidden is exactly the allowed predecessor with minimum DP value.

Thus the transition computes

$$cost[v]+\min_{\text{allowed }u} dp[u]$$

which is precisely the optimal value for item $v$.

Since every layer is computed from correct values of the previous layer, induction shows that all DP values remain optimal. The final minimum among dessert nodes is exactly the cheapest valid dinner.

## Python Solution

```python
import sys
input = sys.stdin.readline

INF = 10**18

n1, n2, n3, n4 = map(int, input().split())

a = list(map(int, input().split()))
b = list(map(int, input().split()))
c = list(map(int, input().split()))
d = list(map(int, input().split()))

def build(prev_dp, cur_costs):
    m = int(input())

    bad = [set() for _ in range(len(cur_costs))]
    for _ in range(m):
        x, y = map(int, input().split())
        bad[y - 1].add(x - 1)

    order = sorted(range(len(prev_dp)), key=lambda i: prev_dp[i])

    res = [INF] * len(cur_costs)

    for i in range(len(cur_costs)):
        for p in order:
            if p not in bad[i]:
                if prev_dp[p] < INF:
                    res[i] = cur_costs[i] + prev_dp[p]
                break

    return res

dp2 = build(a, b)
dp3 = build(dp2, c)
dp4 = build(dp3, d)

ans = min(dp4)

print(-1 if ans >= INF else ans)
```

The implementation follows the dynamic programming formulation directly.

The array passed as `prev_dp` already contains the minimum achievable cost for every item in the previous layer. The `build` function computes the DP values of the next layer.

Each current-layer item stores its forbidden predecessors in a hash set. Membership tests become $O(1)$ on average.

The sorted array `order` is the crucial optimization. It lists predecessor indices from smallest DP value to largest. When processing a current item, we search this list until we encounter a predecessor that is not forbidden. Since the list is sorted, that predecessor is automatically the cheapest allowed one.

The check `prev_dp[p] < INF` prevents unreachable states from being used as valid predecessors.

Indices in the input are 1-based, while Python lists are 0-based. The conversion is performed immediately when reading forbidden pairs.

The value `INF = 10**18` safely exceeds every possible valid answer. The largest dinner cost is at most $4 \times 10^8$, so there is no risk of confusion between reachable and unreachable states.

## Worked Examples

### Sample 1

Input:

```
4 3 2 1
1 2 3 4
5 6 7
8 9
10
...
```

After reading the first layer:

| Item | DP |
| --- | --- |
| A1 | 1 |
| A2 | 2 |
| A3 | 3 |
| A4 | 4 |

Transition to second courses:

| Second course | Forbidden first courses | Cheapest allowed predecessor | DP |
| --- | --- | --- | --- |
| B1 | {1} | A2 (2) | 7 |
| B2 | {1} | A2 (2) | 8 |
| B3 | {} | A1 (1) | 8 |

Transition to drinks:

| Drink | Forbidden second courses | Cheapest allowed predecessor | DP |
| --- | --- | --- | --- |
| C1 | {3} | B1 (7) | 15 |
| C2 | {3} | B1 (7) | 16 |

Transition to desserts:

| Dessert | Forbidden drinks | Cheapest allowed predecessor | DP |
| --- | --- | --- | --- |
| D1 | {1} | C2 (16) | 26 |

Final answer: **26**.

This trace shows the central idea. Whenever the cheapest predecessor is forbidden, the algorithm automatically falls through to the next cheapest valid predecessor.

### Impossible Example

```
1 1 1 1
1
2
3
4
1
1 1
0
0
```

First transition:

| Second course | Forbidden predecessors | Result |
| --- | --- | --- |
| B1 | {A1} | INF |

Second transition:

| Drink | Cheapest predecessor |
| --- | --- |
| C1 | none reachable |

Result remains `INF`.

Third transition:

| Dessert | Cheapest predecessor |
| --- | --- |
| D1 | none reachable |

Result remains `INF`.

The minimum value in the final layer is still infinity, so the answer is `-1`.

This example demonstrates propagation of unreachable states through later layers.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O((N+M)\log N)$ | Sorting each layer dominates, forbidden checks are hash lookups |
| Space | $O(N+M)$ | DP arrays plus forbidden-pair sets |

The total number of items is at most 600,000 and the total number of forbidden pairs is at most 600,000. The algorithm performs three sorting operations and stores the forbidden relations explicitly. Both time and memory comfortably fit within the limits.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys
import io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)

    input = sys.stdin.readline
    INF = 10**18

    n1, n2, n3, n4 = map(int, input().split())

    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    c = list(map(int, input().split()))
    d = list(map(int, input().split()))

    def build(prev_dp, cur_costs):
        m = int(input())
        bad = [set() for _ in range(len(cur_costs))]

        for _ in range(m):
            x, y = map(int, input().split())
            bad[y - 1].add(x - 1)

        order = sorted(range(len(prev_dp)), key=lambda i: prev_dp[i])

        res = [INF] * len(cur_costs)

        for i in range(len(cur_costs)):
            for p in order:
                if p not in bad[i]:
                    if prev_dp[p] < INF:
                        res[i] = cur_costs[i] + prev_dp[p]
                    break

        return res

    dp2 = build(a, b)
    dp3 = build(dp2, c)
    dp4 = build(dp3, d)

    ans = min(dp4)
    return str(-1 if ans >= INF else ans)

# custom minimum case
assert run(
"""1 1 1 1
1
2
3
4
0
0
0
"""
) == "10"

# impossible immediately
assert run(
"""1 1 1 1
1
2
3
4
1
1 1
0
0
"""
) == "-1"

# all equal costs
assert run(
"""2 2 2 2
5 5
5 5
5 5
5 5
0
0
0
"""
) == "20"

# cheapest predecessor forbidden
assert run(
"""2 1 1 1
1 100
5
7
9
1
1 1
0
0
"""
) == "121"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| Single item in every layer | 10 | Minimum-size valid instance |
| Only connection forbidden | -1 | Unreachable propagation |
| All costs equal | 20 | Multiple optimal solutions |
| Cheapest predecessor forbidden | 121 | Correct fallback to second-best predecessor |

## Edge Cases

Consider the case where an item forbids every predecessor.

```
Previous DP: [3, 7]
Forbidden predecessors: {1, 2}
```

The sorted predecessor order is `[3, 7]`. The algorithm checks both entries, finds both forbidden, and never updates the result. The item's value remains `INF`, which correctly marks it as unreachable.

Consider the case where the cheapest predecessor is forbidden but another valid predecessor exists.

```
Previous DP: [1, 5, 10]
Forbidden predecessors: {1}
```

The algorithm checks DP value `1`, rejects it because it is forbidden, then checks DP value `5` and accepts it. The resulting transition uses cost `5`, which is exactly the minimum among all allowed predecessors.

Consider the case where all items in a whole layer become unreachable.

```
Layer 1: [1]
Layer 2: [2]
Forbidden: (1,1)
```

The only item in layer 2 receives value `INF`. When later transitions are computed, the condition `prev_dp[p] < INF` prevents this unreachable item from being used. The impossibility propagates correctly to the final answer, which becomes `-1`.
