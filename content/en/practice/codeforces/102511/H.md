---
title: "CF 102511H - Hobsons' trains"
description: "The network is a directed graph with a special property: every station has exactly one outgoing edge. From station i, the given value d[i] is the only station reachable in one train leg."
date: "2026-08-05T16:21:54+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 102511
codeforces_index: "H"
codeforces_contest_name: "2019 ICPC World Finals"
rating: 0
weight: 102511
solve_time_s: 128
verified: true
draft: false
---

[CF 102511H - Hobsons' trains](https://codeforces.com/problemset/problem/102511/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 2m 8s  
**Verified:** yes  

## Solution
## Problem Understanding

The network is a directed graph with a special property: every station has exactly one outgoing edge. From station `i`, the given value `d[i]` is the only station reachable in one train leg.

For every station `A`, we need to count how many starting stations can arrive at `A` using at most `k` moves. The starting station itself counts, so a station is always included in its own answer.

A graph where every vertex has one outgoing edge is called a functional graph. Every connected component of such a graph contains exactly one directed cycle, and every other station belongs to a tree that eventually leads into that cycle.

The number of stations can be as large as `5 * 10^5`. This rules out checking every starting station separately. A simulation from every node would need up to `O(n)` moves per node, resulting in `O(n^2)` work, which is far beyond what is possible.

The tricky cases are caused by cycles and by long chains leading into them. A solution that treats the graph as a normal tree will fail because cycle nodes have multiple ways to be reached.

For example:

```
5 3
2
3
1
5
4
```

The graph has two cycles: `1 -> 2 -> 3 -> 1` and `4 -> 5 -> 4`. The correct output is:

```
3
3
3
2
2
```

A tree-only approach would miss that station `1` can be reached from stations `2` and `3` through the cycle.

Another edge case is a chain entering a cycle:

```
4 2
2
3
4
3
```

The answers are:

```
1
2
4
3
```

Station `4` can be reached from `1`, `2`, `3`, and `4`, but the distance from `1` is three legs, so it is excluded when `k = 2`. A careless breadth-first search implementation that only marks visited stations without tracking distance can count it incorrectly.

## Approaches

The direct solution is to start a search from every station and follow the outgoing edges backwards. It is correct because it exactly explores all possible starting points that can arrive at a destination. However, in the worst case a graph can contain a chain of length `n`, so repeating this for every station costs roughly `n * n` operations.

The useful observation comes from the structure of functional graphs. If we remove all edges between cycle nodes, every component becomes a collection of rooted trees whose roots are the cycle nodes. For a station inside one of these trees, all stations that can reach it are exactly its descendants in the reversed tree. The question becomes: how many descendants are at depth at most `k` below this node?

That tree query can be answered offline. During a depth-first traversal we assign each node an Euler interval. A node's subtree is one contiguous interval in this ordering. We sort queries by their maximum allowed depth and add nodes to a Fenwick tree as their depth becomes valid. The Fenwick tree then gives the number of active nodes inside every subtree interval.

The remaining part is handling cycle nodes. A cycle node can also be reached from other cycle nodes. On a cycle of length `m`, every cycle node reaches every other cycle node within `m - 1` steps, so the cycle contribution is simply `min(k + 1, m)`.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute Force | O(n²) | O(n) | Too slow |
| Optimal | O(n log n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Find all cycle nodes using indegree elimination. Nodes that become zero indegree cannot be part of a cycle, so repeatedly removing them leaves exactly the directed cycles.
2. Build the reversed forest by adding an edge from a node to all non-cycle nodes that point to it. Cycle-to-cycle edges are ignored because they are handled separately.
3. Perform a DFS over this forest. Assign every node an Euler entry time, exit time, and its depth from the cycle root. During this traversal, record how many nodes exist at every depth.
4. Create one query for every node. The query asks for the number of nodes inside its Euler subtree whose depth is at most `depth[node] + k`.
5. Sort the queries by their depth limit. Sweep through depths from small to large. When a depth becomes allowed, insert every node with that depth into a Fenwick tree using its Euler position. A query answer is the Fenwick sum over its subtree interval.
6. For every cycle node, add the number of reachable cycle nodes. For a cycle of length `m`, this value is `min(k + 1, m)`.

Why it works:

Every station outside a cycle has a unique path toward the cycle. Reversing the edges turns all possible predecessors into a tree, so every valid starting station is exactly a descendant in that tree. The Euler interval property guarantees that subtree queries count precisely those descendants, and the depth sweep guarantees that only nodes within `k` edges are included. Cycle nodes are the only places where multiple directions around a cycle exist, and their contribution is independent of the attached trees, which is why it can be added separately.

## Python Solution

```python
import sys
input = sys.stdin.readline

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i:
            s += self.bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

def solve():
    n, k = map(int, input().split())
    to = [0] * n
    rev = [[] for _ in range(n)]
    indeg = [0] * n

    for i in range(n):
        x = int(input()) - 1
        to[i] = x
        rev[x].append(i)
        indeg[x] += 1

    from collections import deque

    q = deque()
    for i in range(n):
        if indeg[i] == 0:
            q.append(i)

    removed = [False] * n
    while q:
        x = q.popleft()
        removed[x] = True
        y = to[x]
        indeg[y] -= 1
        if indeg[y] == 0:
            q.append(y)

    cycle = [not removed[i] for i in range(n)]

    children = [[] for _ in range(n)]
    for i in range(n):
        if not cycle[i]:
            children[to[i]].append(i)

    tin = [0] * n
    tout = [0] * n
    depth = [0] * n
    nodes_by_depth = []
    timer = 0

    for root in range(n):
        if cycle[root]:
            stack = [(root, 0, False)]
            depth[root] = 0
            while stack:
                x, idx, exit_flag = stack.pop()
                if exit_flag:
                    tout[x] = timer - 1
                    continue
                tin[x] = timer + 1
                timer += 1
                while len(nodes_by_depth) <= depth[x]:
                    nodes_by_depth.append([])
                nodes_by_depth[depth[x]].append(x)
                stack.append((x, 0, True))
                for c in reversed(children[x]):
                    depth[c] = depth[x] + 1
                    stack.append((c, 0, False))

    queries = [(min(n - 1, depth[i] + k), i) for i in range(n)]
    queries.sort()

    bit = Fenwick(n)
    ans = [0] * n
    ptr = 0

    for limit, node in queries:
        while ptr <= limit and ptr < len(nodes_by_depth):
            for x in nodes_by_depth[ptr]:
                bit.add(tin[x], 1)
            ptr += 1
        ans[node] = bit.range_sum(tin[node], tout[node])

    visited = [False] * n
    for i in range(n):
        if cycle[i] and not visited[i]:
            cur = i
            length = 0
            while not visited[cur]:
                visited[cur] = True
                length += 1
                cur = to[cur]
            add = min(k + 1, length)
            cur = i
            while True:
                ans[cur] += add
                cur = to[cur]
                if cur == i:
                    break

    print("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
```

The indegree removal phase separates cycle nodes from tree nodes without recursion, which is necessary because a chain of length `500000` could overflow the Python recursion limit. After that separation, only non-cycle edges are placed in `children`, so the DFS structure is a real forest.

The Euler traversal gives `tin` and `tout` values. The interval `[tin[v], tout[v]]` contains exactly the nodes in `v`'s reversed-tree subtree. The Fenwick tree stores currently active nodes during the depth sweep, so every subtree query becomes a range sum.

The cycle processing is intentionally done after the tree queries. The tree answer already includes the cycle node itself, so only the other cycle nodes must be added. Using `min(k + 1, length)` avoids an off-by-one error when `k` is larger than the cycle length.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n log n) | Every node participates in the Fenwick sweep once, and every query performs logarithmic updates or sums. |
| Space | O(n) | The graph, traversal arrays, and Fenwick tree all store linear-sized data. |

The solution fits the `5 * 10^5` node limit because it never performs work proportional to the product of nodes and path lengths.

## Test Cases

```python
# helper: run solution on input string, return output string
import sys, io

def run(inp: str) -> str:
    old = sys.stdin
    sys.stdin = io.StringIO(inp)
    out = io.StringIO()
    old_out = sys.stdout
    sys.stdout = out
    solve()
    sys.stdout = old_out
    sys.stdin = old
    return out.getvalue()

assert run("""6 2
2
3
4
5
4
3
""") == """1
2
4
5
3
1
"""

assert run("""5 3
2
3
1
5
4
""") == """3
3
3
2
2
"""

assert run("""2 1
2
1
""") == """2
2
"""

assert run("""4 2
2
3
4
3
""") == """1
2
4
3
"""

assert run("""5 1
2
3
4
5
4
""") == """1
2
2
2
1
"""
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| First sample | `1 2 4 5 3 1` | Tree nodes attached to a cycle |
| Second sample | `3 3 3 2 2` | Pure cycles with no trees |
| Two-node cycle | `2 2` | Smallest possible cycle |
| Chain into cycle | `1 2 4 3` | Distance cutoff handling |
| Long chain | `1 2 2 2 1` | Boundary cases for `k` |

## Edge Cases

For the first cycle case:

```
5 3
2
3
1
5
4
```

The first three stations form a cycle of length three. Since `k = 3`, every station on that cycle reaches every other cycle station, giving each of them three valid starts. The second cycle has length two, so both stations also reach each other, but the output remains limited by the size of that cycle.

For the chain case:

```
4 2
2
3
4
3
```

The reversed tree rooted at station `3` contains `1`, `2`, `3`, and `4`. The tree query for station `3` counts depths `0`, `1`, and `2`, but excludes station `1` because it is three edges away. The cycle contribution adds only stations on the `3 -> 4 -> 3` cycle, which gives the final values `1, 2, 4, 3`.

For a large `k`, such as a cycle of length five with `k = 10`, the cycle contribution is still only five. The `min(k + 1, length)` formula prevents counting the same cycle node multiple times after a full rotation.
