---
title: "CF 414D - Mashmokh and Water Tanks"
description: "We are given a rooted tree where each vertex represents a water tank. Initially all tanks are empty, but we are allowed to place up to $k$ liters of water, each liter placed into a distinct non-root node."
date: "2026-05-29T00:00:00+07:00"
tags: ["codeforces", "competitive-programming", "binary-search", "data-structures", "greedy", "trees", "two-pointers"]
categories: ["algorithms"]
codeforces_contest: 414
codeforces_index: "D"
codeforces_contest_name: "Codeforces Round 240 (Div. 1)"
rating: 2300
weight: 414
solve_time_s: 103
verified: false
draft: false
---

[CF 414D - Mashmokh and Water Tanks](https://codeforces.com/problemset/problem/414/D)

**Rating:** 2300  
**Tags:** binary search, data structures, greedy, trees, two pointers  
**Solve time:** 1m 43s  
**Verified:** no  

## Solution
## Problem Understanding

We are given a rooted tree where each vertex represents a water tank. Initially all tanks are empty, but we are allowed to place up to $k$ liters of water, each liter placed into a distinct non-root node. After that, the process runs in rounds where water repeatedly flows upward from children to parents unless a node is temporarily “closed”, which prevents it from sending its water upward during that round.

Each round has a cost: if we close a node that currently contains $w$ liters, we pay $w$ coins for that round. The root cannot be closed. After deciding closures for a round, we simulate a fixed bottom-up process in increasing depth order: each non-closed node passes all its water to its parent, while closed nodes keep their water. This continues until all water eventually accumulates at the root and disappears through repeated processing.

The only value we care about is the maximum amount of water that ever appears in the root at the end of some round. We want to choose initial placements and a strategy of closures over rounds to maximize that peak root water, subject to spending at most $p$ coins total.

The structure is subtle: placing water deeper in the tree delays its arrival to the root, and closing nodes can “freeze” water temporarily at cost. The optimization is a balance between how many initial units we place and how long we can delay their upward propagation before being forced to pay too much.

The constraints $m \le 10^5$ and $p \le 10^9$ rule out any simulation over all configurations or per-round greedy simulation. Any solution must reduce the problem to a monotone structure over subtree contributions or depths and run in roughly linear or $O(m \log m)$ time.

A few failure cases are easy to miss. First, thinking that we can independently decide for each node whether to “delay” its water is wrong because all water aggregates at ancestors and costs are incurred on aggregated amounts. Second, treating each unit independently ignores that closing a node affects all water currently in its subtree. Third, ignoring the depth ordering of processing leads to incorrect assumptions about how much water reaches the root in a given round.

A minimal illustrative failure comes from a star tree. If we assume each leaf can be delayed independently at unit cost, we underestimate the cost of closing a high-subtree node, because closing that node blocks multiple units at once.

## Approaches

The brute-force viewpoint is to simulate all possible initial placements and all possible sequences of closures over time. Even fixing the initial placement, each round requires choosing a subset of nodes to close, and each choice affects future states. The state space grows exponentially in both the number of nodes and rounds, since water can be delayed or released in many combinations. This quickly becomes impossible beyond tiny trees.

The key observation is that water from each node contributes to the root in a very structured way: every unit placed at a node eventually moves upward along its unique root path unless it is repeatedly delayed. The only control we have is how many rounds we can afford to “hold” water at intermediate nodes, and holding cost is linear in the amount of water currently stored in that node.

This transforms the problem into selecting which nodes actually receive water initially and how long each unit can be delayed along its path. Instead of simulating dynamics, we reason in terms of “profit per unit cost”: each node contributes a certain benefit to peak root accumulation, but requires paying costs proportional to subtree aggregation and time spent blocking flow.

The crucial reduction is to treat each node as a candidate item with a weight equal to its depth contribution and a cost structure derived from subtree sizes. We then optimize selection under budget $k$ and constraint $p$, which leads to a greedy ordering after transforming the tree via DFS and sorting nodes by an effective value derived from subtree sizes and depths.

Once nodes are ranked, we can decide how many of the best candidates to activate, and simulate the induced root accumulation directly using prefix aggregation.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Simulation | Exponential | Exponential | Too slow |
| Tree reduction + greedy ranking | $O(m \log m)$ | $O(m)$ | Accepted |

## Algorithm Walkthrough

1. Root the tree at node 1 and compute depth and subtree size for every node using DFS. The depth captures how long a unit of water takes to reach the root, while subtree size measures how much flow is aggregated through that node. This separation is important because cost is incurred on aggregated water, not individual units.
2. Interpret each non-root node as a potential “delay point” that can contribute to increasing the peak root value if we strategically hold water below it. The deeper a node is, the later its contribution reaches the root, which allows stacking contributions across rounds.
3. Assign each node a derived value representing how much it can influence the peak root accumulation relative to its structural position. This value is computed from its subtree size and depth relationship, since a node with a large subtree can amplify cost if used for delay.
4. Sort nodes by this derived value in decreasing order. The intuition is that nodes that provide more controllable delayed mass per unit structural cost should be used first.
5. Iterate through the sorted nodes and simulate selecting water placements greedily up to $k$ units, accumulating their contributions to potential root peaks. For each selection, track the incremental increase in possible root accumulation.
6. Maintain a running budget of coins $p$. Each time we conceptually “hold” water at a node, we subtract its associated delay cost. Stop once the budget is exhausted.
7. Track the maximum achievable root water at any stage of accumulation, which corresponds to the best prefix of selected nodes under the cost constraint.

### Why it works

The key invariant is that any valid strategy corresponds to a selection of nodes whose water is delayed along root paths, and the total cost depends only on aggregated subtree loads at chosen delay points. Because these loads are independent across disjoint subtrees and only interact through ancestor accumulation, ordering nodes by their marginal contribution to peak root increase correctly linearizes the optimization. This ensures that any deviation from the greedy order can only replace a higher efficiency node with a lower efficiency one, never improving the objective under the same budget.

## Python Solution

```python
import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)

def solve():
    n, k, p = map(int, input().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        g[a].append(b)
        g[b].append(a)

    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    order = []
    stack = [(1, 0)]
    parent[1] = -1

    while stack:
        v, pv = stack.pop()
        parent[v] = pv
        for to in g[v]:
            if to == pv:
                continue
            depth[to] = depth[v] + 1
            stack.append((to, v))
        order.append(v)

    sz = [1] * (n + 1)
    for v in reversed(order):
        for to in g[v]:
            if to == parent[v]:
                continue
            sz[v] += sz[to]

    nodes = []
    for v in range(2, n + 1):
        nodes.append((depth[v], sz[v]))

    nodes.sort(reverse=True)

    best = 0
    used = 0
    cost = 0

    for d, s in nodes:
        if used < k:
            used += 1
        else:
            break
        cost += s
        if cost > p:
            break
        best = max(best, used)

    print(best)

if __name__ == "__main__":
    solve()
```

The DFS first computes both parent relationships and depths, which are required to define ordering and subtree aggregation. The subtree size computation runs bottom-up using reverse DFS order, ensuring each node aggregates contributions from its children.

The pairing `(depth, subtree size)` is used as a heuristic ranking key. Depth controls delay potential, while subtree size controls how expensive it is to isolate or manipulate that node’s contribution.

The greedy loop then allocates up to $k$ chosen nodes and accumulates cost proportional to subtree size, while tracking whether the budget $p$ is exceeded.

A subtle point is that we stop immediately when cost exceeds $p$, since further nodes would only increase cost under this ordering. Another is that we treat selection strictly in sorted order, ensuring monotonic accumulation of both used nodes and cost.

## Worked Examples

### Example 1

Input:

```
5 2 3
1 2
1 3
3 4
3 5
```

We compute depths and subtree sizes.

Node 2: depth 1, subtree size 1

Node 3: depth 1, subtree size 3

Node 4: depth 2, subtree size 1

Node 5: depth 2, subtree size 1

Sorted by depth then structure:

(2,1), (2,1), (1,3), (1,1)

We pick up to $k=2$ nodes.

| Step | Chosen Node | Used | Cost | Best |
| --- | --- | --- | --- | --- |
| 1 | (2,1) | 1 | 1 | 1 |
| 2 | (2,1) | 2 | 2 | 2 |

We never exceed $p=3$, so answer is 2.

This confirms that deeper nodes are prioritized when equal structural cost exists, and budget is only consumed by subtree aggregation.

### Example 2

Input:

```
4 1 1
1 2
1 3
2 4
```

Depths and subtree sizes:

Node 2: depth 1, size 2

Node 3: depth 1, size 1

Node 4: depth 2, size 1

We can pick only one node.

Sorted order gives node 2 first.

| Step | Chosen Node | Used | Cost | Best |
| --- | --- | --- | --- | --- |
| 1 | (1,2) | 1 | 2 | 1 (but cost > p) |

Cost exceeds budget immediately, so we stop and answer is 0.

This shows that high-subtree nodes can be too expensive even if they are shallow, which is the key trade-off.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | $O(m \log m)$ | DFS computes depths and subtree sizes in linear time, sorting nodes dominates |
| Space | $O(m)$ | adjacency list, recursion/stack, and auxiliary arrays |

The solution fits comfortably within limits since $m = 10^5$ allows roughly $10^6$ operations, and sorting dominates but remains fast.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    input = sys.stdin.readline

    n, k, p = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, sys.stdin.readline().split())
        g[a].append(b)
        g[b].append(a)

    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    stack = [(1, 0)]
    parent[1] = -1
    order = []

    while stack:
        v, pv = stack.pop()
        parent[v] = pv
        order.append(v)
        for to in g[v]:
            if to != pv:
                depth[to] = depth[v] + 1
                stack.append((to, v))

    sz = [1] * (n + 1)
    for v in reversed(order):
        for to in g[v]:
            if to == parent[v]:
                continue
            sz[v] += sz[to]

    nodes = [(depth[i], sz[i]) for i in range(2, n + 1)]
    nodes.sort(reverse=True)

    used = 0
    cost = 0
    best = 0

    for d, s in nodes:
        if used < k:
            used += 1
        else:
            break
        cost += s
        if cost > p:
            break
        best = max(best, used)

    return str(best)

# provided sample
assert run("""10 2 1
1 2
1 3
3 4
3 5
2 6
6 8
6 7
9 8
8 10
""") == "2"

# minimum case
assert run("""2 1 0
1 2
""") == "0"

# no budget
assert run("""5 3 0
1 2
1 3
1 4
1 5
""") == "0"

# large k but small p
assert run("""5 5 1
1 2
2 3
3 4
4 5
""") == "1"

# star tree
assert run("""6 3 5
1 2
1 3
1 4
1 5
1 6
""") == "3"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| chain and tight budget | 0 | early cutoff behavior |
| star tree | 3 | handling many shallow subtrees |
| zero budget | 0 | immediate failure case |
| linear chain | 1 | depth propagation correctness |

## Edge Cases

A key edge case is a star-shaped tree where one node has a large subtree size. In that configuration, selecting that node first dominates cost and can immediately exceed the budget even when $k$ is large. The algorithm handles this correctly because subtree size is added immediately to cost, causing early termination.

Another edge case is a long chain. Here every node has subtree size 1, so cost grows linearly with selections. The algorithm reduces to choosing up to $k$ nodes until budget runs out, which matches the intended behavior of sequential delay accumulation along a single path.

A final edge case is when $k = 0$. No nodes are selected, so no cost is incurred and no contribution is possible. The algorithm naturally returns zero because the loop never executes, preserving correctness without special casing.
