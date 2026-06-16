---
title: "CF 1346D - Constructing the Dungeon"
description: "We are given an undirected connected graph where vertices represent rooms and edges represent tunnels. Each tunnel already has a fixed value, and we must assign a value to every room."
date: "2026-06-16T10:00:57+07:00"
tags: ["codeforces", "competitive-programming", "*special", "graphs", "greedy"]
categories: ["algorithms"]
codeforces_contest: 1346
codeforces_index: "D"
codeforces_contest_name: "Kotlin Heroes: Episode 4"
rating: 1600
weight: 1346
solve_time_s: 176
verified: true
draft: false
---

[CF 1346D - Constructing the Dungeon](https://codeforces.com/problemset/problem/1346/D)

**Rating:** 1600  
**Tags:** *special, graphs, greedy  
**Solve time:** 2m 56s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an undirected connected graph where vertices represent rooms and edges represent tunnels. Each tunnel already has a fixed value, and we must assign a value to every room.

The rule ties rooms and tunnels together tightly: for every edge between two rooms, the edge value must equal the smaller of the two room values. Once the room values are chosen, every edge is automatically forced, so the only freedom we have is the assignment of room values.

The goal is not just to satisfy all constraints but to minimize the total sum of room values. If no assignment exists, we must report impossibility.

The constraints push us toward a linear or near-linear solution per test case. The total number of vertices and edges across all tests is at most 200,000, so any approach that is even quadratic per test case will fail. Even something like repeatedly recomputing consistency with full graph scans is too slow. We need a construction that is essentially one or two graph passes per test.

A subtle issue arises from cycles. On a tree, constraints propagate cleanly from leaves inward. In a cyclic graph, conflicting requirements can appear: a room might be forced to be both strictly greater than and equal to different neighbors in inconsistent ways. A naive greedy assignment without global propagation can easily accept invalid configurations.

A simple failure case is a triangle where edges enforce incompatible minima. For example, if edges demand (1,2)=5, (2,3)=7, (1,3)=6, then room 2 must be at least 7, room 1 at least 6, but then edge (1,2) would require min(a1,a2)=5, which cannot hold. A local assignment strategy will miss this contradiction unless it propagates constraints globally.

The core difficulty is that each edge constrains the lower endpoint among its two rooms, and these constraints must be globally consistent across all possible ways a room can act as the minimum endpoint.

## Approaches

A brute-force idea is to treat each room value as an unknown integer and try to enforce constraints iteratively. We could start with all rooms unassigned, repeatedly pick an edge, and try to set both endpoints so that the minimum matches the required edge weight. This quickly becomes ambiguous: assigning one endpoint affects all its neighbors, and revisiting edges can force revisions.

In the worst case, each update can cascade across the entire graph, and we may end up revisiting edges many times. This behaves like constraint propagation with potential repeated relaxations, giving an exponential or at least quadratic worst case due to cycles repeatedly tightening values.

The key observation is that each room must be at least as large as every incident edge weight, because if a room participates in an edge with weight w and it is the smaller endpoint, then that room must equal w; if it is the larger endpoint, then the other endpoint equals w, forcing the larger one to be at least w anyway. So every room has a natural lower bound: the maximum edge weight incident to it.

Let this lower bound be L[i] = max weight of edges touching i. The optimal solution will never choose a value larger than necessary, so we start by setting a[i] = L[i].

Now we check feasibility: for every edge (u, v, w), the condition min(a[u], a[v]) = w must hold. Since both endpoints are already at least their incident maxima, this reduces to verifying that at least one endpoint is exactly w and the other is at least w. If both endpoints are strictly greater than w, the edge cannot achieve its required minimum, so the configuration is invalid.

Thus the construction becomes: assign each node its maximum incident edge weight, then verify all edges. If all edges satisfy the minimum condition, this assignment is optimal; otherwise no solution exists.

This works because reducing any node below its maximum incident edge weight would immediately break that edge, and increasing any node beyond its maximum only increases the total sum unnecessarily.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force Constraint Propagation | O(nm) worst-case | O(n + m) | Too slow / Unstable |
| Optimal Max-Assignment + Verification | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We process each test case independently.

1. Compute for every room the maximum weight among all tunnels incident to it. This value represents the smallest feasible assignment that can still satisfy any edge where the room acts as the minimum endpoint. Any smaller value would immediately violate at least one constraint.
2. Assign each room its computed maximum incident edge weight. At this point, every room is set to the smallest value that does not instantly contradict local edge requirements.
3. Check every tunnel (u, v, w) and verify that the condition min(a[u], a[v]) equals w holds. This step ensures that for each edge, at least one endpoint is exactly w and the other is not below w.
4. If any edge fails this condition, output NO because no adjustment can fix it without breaking a previously satisfied constraint.
5. Otherwise output YES followed by all assigned room values.

### Why it works

Each room value is forced to be at least the largest edge weight incident to it, otherwise that edge cannot achieve its required minimum. Setting a[i] exactly to this bound minimizes the sum.

If an edge (u, v, w) cannot satisfy min(a[u], a[v]) = w under this assignment, then both endpoints exceed w, meaning neither endpoint is allowed to drop to w without violating another incident constraint. That implies a global contradiction: every candidate assignment would require lowering at least one endpoint below its own incident maximum, which is impossible by definition of the construction. This makes the check both necessary and sufficient.

## Python Solution

```python
import sys
input = sys.stdin.readline

def solve():
    t = int(input())
    for _ in range(t):
        n, m = map(int, input().split())
        adj_max = [0] * n
        edges = []

        for _ in range(m):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            edges.append((u, v, w))
            if w > adj_max[u]:
                adj_max[u] = w
            if w > adj_max[v]:
                adj_max[v] = w

        a = adj_max[:]
        ok = True

        for u, v, w in edges:
            if min(a[u], a[v]) != w:
                ok = False
                break

        if not ok:
            print("NO")
        else:
            print("YES")
            print(*a)

if __name__ == "__main__":
    solve()
```

The implementation first builds the maximum required value per node while reading edges, so no extra pass over adjacency lists is needed. The assignment step is just copying these maxima.

The validation loop is essential because the construction is not automatically guaranteed to satisfy the minimum condition on every edge; it only guarantees that no node violates its strongest local constraint. The final check ensures consistency across edges that might have asymmetric maxima.

## Worked Examples

### Example 1

Input:

```
3 2
1 2 1
2 3 1
```

We compute maximum incident weights:

room 1 → 1, room 2 → 1, room 3 → 1

Assignment:

a = [1, 1, 1]

| Step | Edge | a[u] | a[v] | min(a[u], a[v]) | w | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (1,2) | 1 | 1 | 1 | 1 | yes |
| 2 | (2,3) | 1 | 1 | 1 | 1 | yes |

All edges match, so output is YES.

This shows the case where all constraints align and the maximal-per-node assignment already satisfies every equality exactly.

### Example 2

Input:

```
4 4
1 2 5
3 2 2
4 1 3
3 4 4
```

Compute maxima:

room 1 → 5, room 2 → 5, room 3 → 4, room 4 → 4

Assignment:

a = [5, 5, 4, 4]

| Step | Edge | a[u] | a[v] | min(a[u], a[v]) | w | Valid |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | (1,2) | 5 | 5 | 5 | 5 | yes |
| 2 | (3,2) | 4 | 5 | 4 | 2 | no |

Edge (3,2) fails since min is 4 but required is 2.

This demonstrates that even if local maxima are consistent, global structure can still force an impossible configuration when an edge weight is strictly smaller than both endpoints' enforced lower bounds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) per test case | One pass to compute maxima and one pass to verify edges |
| Space | O(n + m) | Storage for edge list and node values |

The total size across all test cases is bounded by 200,000, so the linear traversal strategy easily fits within time limits. The algorithm performs only constant work per edge and per node.

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
        n, m = map(int, input().split())
        adj_max = [0] * n
        edges = []
        for _ in range(m):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            edges.append((u, v, w))
            adj_max[u] = max(adj_max[u], w)
            adj_max[v] = max(adj_max[v], w)

        a = adj_max[:]
        ok = True
        for u, v, w in edges:
            if min(a[u], a[v]) != w:
                ok = False
                break

        if not ok:
            out.append("NO")
        else:
            out.append("YES")
            out.append(" ".join(map(str, a)))

    return "\n".join(out)

# provided sample 1
assert run("""3
3 2
1 2 1
2 3 1
5 7
3 2 7
3 4 9
1 5 5
1 2 5
4 1 5
4 2 7
3 1 5
4 4
1 2 5
3 2 2
4 1 3
3 4 4
""") == """YES
1 1 1
YES
5 7 9 9 5
NO"""

# custom 1: single edge
assert run("""1
2 1
1 2 7
""").startswith("YES")

# custom 2: impossible triangle
assert run("""1
3 3
1 2 5
2 3 6
1 3 4
""").endswith("NO")

# custom 3: star graph
assert run("""1
4 3
1 2 2
1 3 3
1 4 4
""").startswith("YES")

# custom 4: all equal
assert run("""1
3 3
1 2 1
2 3 1
1 3 1
""").startswith("YES")
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single edge | YES ... | basic feasibility |
| triangle conflict | NO | global inconsistency detection |
| star graph | YES | independent constraints per node |
| all equal | YES | uniform edge consistency |

## Edge Cases

One important edge case is when a node has multiple incident edges with different weights. The construction sets the node to the maximum, which can immediately invalidate smaller edges. For example, if a node connects with weights 2 and 10, it becomes 10, and the edge with weight 2 can only remain valid if its other endpoint is exactly 2.

Another edge case is when the graph is a tree. In that case, the construction always succeeds because each edge can always assign the smaller endpoint correctly without cycles forcing contradictions. The algorithm naturally handles this because the verification step will never fail when a consistent tree assignment exists.

A final case is when all edges have identical weights. Every node receives that same value, and every edge trivially satisfies the minimum condition.
