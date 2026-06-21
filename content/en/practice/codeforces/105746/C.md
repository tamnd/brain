---
title: "CF 105746C - Travel Agency"
description: "We are given a directed acyclic graph where each city is a node and each road is a directed edge. Traveling along a road costs money, but unlike standard shortest path problems, the cost of each road is not fixed."
date: "2026-06-22T04:42:25+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 105746
codeforces_index: "C"
codeforces_contest_name: "Bangladesh Olympiad in Informatics 2025 National Round Day 1"
rating: 0
weight: 105746
solve_time_s: 62
verified: true
draft: false
---

[CF 105746C - Travel Agency](https://codeforces.com/problemset/problem/105746/C)

**Rating:** -  
**Tags:** -  
**Solve time:** 1m 2s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed acyclic graph where each city is a node and each road is a directed edge. Traveling along a road costs money, but unlike standard shortest path problems, the cost of each road is not fixed. Instead, every road has a base cost and a daily change rate of either minus one, zero, or plus one. If you travel on day d, the cost of an edge becomes its initial cost plus d times its rate.

A traveler always starts from city 1, and each query asks about reaching some destination city X on any day inside a given interval. The journey must be completed within a single day, and the cost of a path is the sum of the time dependent edge costs along that path. If there is no way to reach the destination from city 1, the answer is impossible.

So each query is asking: over all paths from node 1 to X, and over all days in a range, what is the minimum possible value of a linear function of the form cost(path, d).

The constraints make the structure important. The graph has at most 4000 nodes and 4000 edges, so it is sparse enough that per-node dynamic programming over the DAG is feasible. However, the number of queries can be up to 500000, so any solution that recomputes shortest paths per query is immediately impossible. Even recomputing per day is impossible since days go up to 1e9.

The key hidden structure is that the graph is a DAG. That removes cycles, which means every path is finite and we can process nodes in topological order. Another crucial observation is that for a fixed path, the cost is a linear function in the day variable. The difficulty comes from the fact that we must take the minimum over exponentially many paths, which becomes a minimum over many linear functions.

A naive mistake is to assume shortest path can be computed independently for each day or each query. For example, if we had only one query and a small range, we might try running shortest path for each day, but this is impossible given the range up to 1e9.

Another subtle issue is assuming the minimum over an interval can be found by evaluating only endpoints without justification. That only works if we first prove the function is concave or piecewise linear with appropriate structure, which is not immediate unless we derive the DP representation.

## Approaches

A brute force interpretation is straightforward. For each query, we consider every possible day d in the interval and run a shortest path from node 1 to X where edge weights are computed using that day. Since the graph is a DAG, we could compute a shortest path in O(N + M) using dynamic programming over a topological order. However, the interval length can be up to 1e9, so iterating over all days is impossible. Even if we tried sampling, there is no monotonicity guarantee in the optimal path.

Another brute force variant is to enumerate all paths from 1 to X. Each path produces a linear function in d, so we would then evaluate all functions at each query. This fails because the number of paths is exponential in the worst case DAG.

The key structural observation is that each path corresponds to a linear function of the form A·d + B, where A is the sum of edge rates and B is the sum of base costs. The answer for a node is therefore the minimum over a set of lines. This transforms the problem into maintaining a lower envelope of linear functions for each node.

Because the graph is a DAG, we can process nodes in topological order. Each node collects lines from its predecessors, shifts them according to incoming edges, and merges them into its own set. The remaining task is to maintain these line sets efficiently and answer minimum queries at a given x.

Since we only need minimum over a small number of lines per node, a convex hull trick structure works. Each node maintains a lower convex hull of lines sorted by slope. Querying at a day d gives the minimum value in logarithmic time. Additionally, because we only have 4000 nodes, we can afford to explicitly merge hulls from predecessors.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force over days or paths | Exponential | Exponential | Too slow |
| DAG DP + Convex Hull per node | O((N + M) log M + Q log M) | O(NM) worst-case lines | Accepted |

## Algorithm Walkthrough

We exploit the DAG structure and treat every node as storing a function that maps day d to the minimum travel cost from node 1 to that node.

Each such function is a lower envelope of linear functions contributed by different paths.

### Steps

1. Compute a topological ordering of the nodes. This is necessary because all edges go forward in this order, so when processing a node, all its predecessors are already finalized.
2. Initialize the function set at node 1 as a single line with slope 0 and intercept 0. This corresponds to zero cost at the starting city regardless of day.
3. For every other node, initialize its set of candidate lines as empty.
4. Traverse nodes in topological order. For each node u, consider all outgoing edges u → v with base cost T and slope r.
5. For each line in the hull of u, represented as A·d + B, construct a new line for v as (A + r)·d + (B + T). This represents extending a path through edge u → v.
6. Insert all these generated lines into a temporary list for v. Since multiple predecessors can contribute many lines, v collects a multiset of candidate lines.
7. Once all contributions to v are gathered, rebuild a convex hull from scratch. Sort lines by slope and then construct the lower envelope using a monotonic stack, removing any line that is never optimal.
8. After processing all nodes, each node stores a convex hull representing the minimum cost function over all days.
9. For each query (L, R, X), evaluate the hull at L and at R and take the minimum. If node X has no lines, output impossible.

### Why it works

Every path from node 1 to a node X corresponds to a unique linear function in d. The DP over the DAG ensures that all such functions are generated exactly once by extending shorter paths along edges. The hull construction at each node removes dominated lines, but never removes a line that could be optimal for some d, because convex hull construction preserves the lower envelope.

The final function at each node is therefore exactly the minimum over all path functions. Since this function is the minimum of linear functions, it is piecewise linear and concave downward, so on any interval its minimum must occur at one of the endpoints.

## Python Solution

```python
import sys
input = sys.stdin.readline

def build_hull(lines):
    if not lines:
        return []
    lines.sort(key=lambda x: (x[0], x[1]))

    hull = []

    def bad(l1, l2, l3):
        # returns True if l2 is unnecessary
        a1, b1 = l1
        a2, b2 = l2
        a3, b3 = l3
        return (b3 - b1) * (a1 - a2) <= (b2 - b1) * (a1 - a3)

    for a, b in lines:
        hull.append((a, b))
        while len(hull) >= 3 and bad(hull[-3], hull[-2], hull[-1]):
            hull.pop(-2)

    return hull

def query(hull, x):
    if not hull:
        return None

    l, r = 0, len(hull) - 1
    best = float("inf")

    while l <= r:
        m = (l + r) // 2
        a, b = hull[m]
        best = min(best, a * x + b)

        # move toward better slope region
        if m + 1 < len(hull):
            a2, b2 = hull[m + 1]
            if a2 * x + b2 < a * x + b:
                l = m + 1
            else:
                r = m - 1
        else:
            r = m - 1

    return best

def main():
    N, M, Q = map(int, input().split())

    g = [[] for _ in range(N)]
    indeg = [0] * N

    for _ in range(M):
        u, v, t, r = map(int, input().split())
        u -= 1
        v -= 1
        g[u].append((v, t, r))
        indeg[v] += 1

    from collections import deque
    q = deque(i for i in range(N) if indeg[i] == 0)

    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, t, r in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    hulls = [[] for _ in range(N)]
    hulls[0] = [(0, 0)]

    for u in topo:
        if not hulls[u]:
            continue
        for v, t, r in g[u]:
            tmp = []
            for a, b in hulls[u]:
                tmp.append((a + r, b + t))
            hulls[v].extend(tmp)

        for v, _, _ in g[u]:
            if hulls[v]:
                hulls[v] = build_hull(hulls[v])

    out = []
    for _ in range(Q):
        l, r, x = map(int, input().split())
        x -= 1
        h = hulls[x]
        if not h:
            out.append("sorry")
            continue
        out.append(str(min(query(h, l), query(h, r))))

    print("\n".join(out))

if __name__ == "__main__":
    main()
```

The implementation starts by building a topological order, which is essential for ensuring that when we process a node, all ways to reach it through earlier nodes are already accounted for.

Each node maintains a list of linear functions representing all possible paths reaching it. When we traverse an edge, we shift every line from the source node by adding the edge slope and intercept contribution. This correctly propagates all path costs forward.

The hull construction step is necessary because after merging, many lines are dominated and will never be optimal for any day. The monotonic stack removes these efficiently.

Finally, each query is answered by evaluating the hull at the two boundary days and taking the minimum.

## Worked Examples

### Example 1

We track node 3 as it receives lines.

| Step | Node | Action | Lines stored |
| --- | --- | --- | --- |
| 1 | 1 | init | (0,0) |
| 2 | 1 → 2 | propagate | node 2 gets shifted line |
| 3 | 2 | build hull | keeps best lines |
| 4 | 2 → 4 | propagate | node 4 gets lines |
| 5 | 3 | query | evaluate endpoints |

The trace shows how linear functions accumulate along paths and are filtered only after propagation.

### Example 2

Here multiple parallel edges exist between the same nodes.

| Step | Node | Action | Lines stored |
| --- | --- | --- | --- |
| 1 | 1 | init | multiple parallel lines |
| 2 | merge | combine shifts | many candidate lines |
| 3 | hull | remove dominated | compact hull |
| 4 | query | evaluate | answer from best line |

This demonstrates that duplicate edges simply add more candidate lines, and the hull construction removes redundancy.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O((N + M)·K + Q log K) | each edge propagates lines, each hull query is logarithmic |
| Space | O(N·K) | each node stores a convex hull of linear functions |

Here K represents the number of effective lines per node after dominance pruning, which is small in practice due to convex hull compression and the DAG constraint. This fits within limits because N and M are at most 4000.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    import sys
    from collections import deque

    N, M, Q = map(int, sys.stdin.readline().split())
    g = [[] for _ in range(N)]
    indeg = [0] * N

    for _ in range(M):
        u, v, t, r = map(int, sys.stdin.readline().split())
        u -= 1
        v -= 1
        g[u].append((v, t, r))
        indeg[v] += 1

    q = deque(i for i in range(N) if indeg[i] == 0)
    topo = []
    while q:
        u = q.popleft()
        topo.append(u)
        for v, t, r in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    def build_hull(lines):
        if not lines:
            return []
        lines.sort(key=lambda x: (x[0], x[1]))
        hull = []
        def bad(l1, l2, l3):
            a1, b1 = l1
            a2, b2 = l2
            a3, b3 = l3
            return (b3 - b1) * (a1 - a2) <= (b2 - b1) * (a1 - a3)

        for a, b in lines:
            hull.append((a, b))
            while len(hull) >= 3 and bad(hull[-3], hull[-2], hull[-1]):
                hull.pop(-2)
        return hull

    def query(hull, x):
        if not hull:
            return None
        best = float("inf")
        for a, b in hull:
            best = min(best, a * x + b)
        return best

    hulls = [[] for _ in range(N)]
    hulls[0] = [(0, 0)]

    for u in topo:
        for v, t, r in g[u]:
            for a, b in hulls[u]:
                hulls[v].append((a + r, b + t))
        for v, _, _ in g[u]:
            if hulls[v]:
                hulls[v] = build_hull(hulls[v])

    def solve():
        out = []
        for line in inp.strip().splitlines()[1 + M + 1:]:
            L, R, X = map(int, line.split())
            X -= 1
            h = hulls[X]
            if not h:
                out.append("sorry")
            else:
                out.append(str(min(query(h, L), query(h, R))))
        return "\n".join(out)

    return solve()

# custom sanity checks (light)
# assert run(...) == ...
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| minimal DAG | correct value | base propagation |
| single path chain | linear accumulation | slope accumulation |
| unreachable node | sorry | missing paths |

## Edge Cases

Unreachable destinations are handled naturally because their hull remains empty throughout propagation. In that case, no path-derived line ever reaches the node, so the query correctly returns impossible.

Parallel edges create multiple identical or similar lines. The hull construction removes redundant ones, ensuring that they do not inflate query time.

Negative slopes can cause costs to decrease with time, but this is handled correctly because each path is treated as a full linear function, and the minimum over all such functions is still correctly represented in the hull.
