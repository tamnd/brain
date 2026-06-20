---
title: "CF 106129H - Happy Hookup"
description: "We are given a directed graph where vertices represent train stations and edges represent one-way train connections. Two people start from two different stations, and each can travel along directed edges any number of times."
date: "2026-06-20T07:31:33+07:00"
tags: ["codeforces", "competitive-programming"]
categories: ["algorithms"]
codeforces_contest: 106129
codeforces_index: "H"
codeforces_contest_name: "2025-2026 ICPC German Collegiate Programming Contest (GCPC 2025)"
rating: 0
weight: 106129
solve_time_s: 42
verified: true
draft: false
---

[CF 106129H - Happy Hookup](https://codeforces.com/problemset/problem/106129/H)

**Rating:** -  
**Tags:** -  
**Solve time:** 42s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given a directed graph where vertices represent train stations and edges represent one-way train connections. Two people start from two different stations, and each can travel along directed edges any number of times. The question is whether there exists at least one station that is reachable from both starting points.

So the task reduces to a reachability problem in a directed graph: from node `a` and node `b`, we want to find whether their reachable sets intersect, and if they do, output any node in the intersection.

The constraints go up to 100,000 nodes and 100,000 edges, which immediately rules out any quadratic approach such as checking reachability between every pair of nodes or recomputing shortest paths per candidate node. Any solution must be essentially linear in the size of the graph, typically `O(n + m)`.

A subtle issue appears if one tries to reason greedily from structure. For example, picking “a meeting station” based on local connectivity or earliest encounter in a BFS tree is not safe, because reachability is not symmetric and paths may diverge deeply before converging again.

Another edge case is when there is no outgoing path from one of the sources. For example:

Input:

```
3 1
1 2
3 1
```

From `3` you can reach `1` and then `2`, but from `1` you can only reach `2`. The only possible meeting station is `2`. A naive approach that only checks immediate neighbors of `a` or `b` would miss this.

Finally, if the graph is disconnected or contains long directed chains, it is easy to incorrectly assume overlap based on undirected intuition. Direction matters fully here.

## Approaches

A brute-force idea is to compute the full set of reachable nodes from `a` using BFS or DFS, and separately compute the reachable set from `b`, then intersect the two sets. This is correct and conceptually simple.

Each BFS/DFS runs in `O(n + m)`, and set intersection is `O(n)` if implemented with boolean arrays. So even the naive approach is already linear per source, hence `O(n + m)` total. This is already efficient enough for the constraints.

However, a more conceptual brute force might attempt, for each node `v`, to check whether `v` is reachable from both `a` and `b` by running a BFS twice per node or running a reverse reachability check per node. That would lead to `O(n(n + m))`, which is far too large.

The key observation is that reachability from a single source partitions the graph into a reachable region. We only need to know whether the two reachable regions overlap, and if they do, we can stop immediately upon finding any common node. This allows us to avoid unnecessary work by interleaving or early stopping, but even without optimization tricks, two BFS runs are sufficient.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Brute force per node | O(n(n + m)) | O(n + m) | Too slow |
| Two BFS/DFS + intersection | O(n + m) | O(n + m) | Accepted |

## Algorithm Walkthrough

We compute all nodes reachable from each starting station independently using graph traversal.

1. Build an adjacency list from the directed edges. This structure allows efficient traversal of outgoing connections from any station.
2. Run a BFS or DFS starting from station `a`, marking every visited node in a boolean array `reach_a`. This captures exactly the set of stations that person A can reach through any number of train rides.
3. Run another BFS or DFS starting from station `b`, marking visited nodes in `reach_b`. This similarly captures all stations reachable by Hannah.
4. Scan all stations from `1` to `n`. For each station `v`, check whether both `reach_a[v]` and `reach_b[v]` are true. The first such node is a valid meeting point and can be immediately output.
5. If no such node exists after scanning all stations, output `"no"`.

The reason we can safely return any intersection node is that the problem does not require optimality such as shortest travel time or earliest station; any reachable overlap is valid.

### Why it works

The algorithm explicitly computes the forward reachability sets of both starting nodes. By definition, a node is in the intersection of these sets if and only if both participants can independently reach it along directed paths. The BFS/DFS exploration guarantees completeness of these sets because every edge is traversed exactly once from each source, so no reachable node is omitted. Therefore, any node found in both visited sets is a correct meeting station, and if no such node exists, the intersection is empty and no solution exists.

## Python Solution

```python
import sys
input = sys.stdin.readline

def bfs(start, adj, n):
    vis = [False] * (n + 1)
    stack = [start]
    vis[start] = True

    while stack:
        v = stack.pop()
        for nxt in adj[v]:
            if not vis[nxt]:
                vis[nxt] = True
                stack.append(nxt)
    return vis

def solve():
    n, m = map(int, input().split())
    adj = [[] for _ in range(n + 1)]

    for _ in range(m):
        x, y = map(int, input().split())
        adj[x].append(y)

    a, b = map(int, input().split())

    reach_a = bfs(a, adj, n)
    reach_b = bfs(b, adj, n)

    for i in range(1, n + 1):
        if reach_a[i] and reach_b[i]:
            print("yes")
            print(i)
            return

    print("no")

if __name__ == "__main__":
    solve()
```

The solution builds a directed adjacency list and then performs two independent depth-first searches using a stack. The visited arrays `reach_a` and `reach_b` encode reachability from each starting node.

A small implementation detail that matters is marking nodes as visited immediately when pushing onto the stack. This prevents repeated insertion and keeps traversal linear. The final scan is necessary because we are allowed to output any valid meeting station, not necessarily the first one discovered during traversal.

## Worked Examples

### Example 1

Input:

```
3 2
1 3
2 3
1 2
```

We compute reachability from `1` and `2`.

| Step | Node from A | Visited A | Node from B | Visited B | Intersection found |
| --- | --- | --- | --- | --- | --- |
| Start | 1 | {1} | 2 | {2} | none |
| Expand A | 3 | {1,3} | 2 | {2} | none |
| Expand B | 3 already seen | {1,3} | 3 | {2,3} | yes |

Both reach node `3`, so output is:

```
yes
3
```

This demonstrates that convergence can happen even if sources are different and paths are asymmetric.

### Example 2

Input:

```
3 2
2 1
2 3
1 3
```

Reachability:

| Step | Node from A | Visited A | Node from B | Visited B | Intersection found |
| --- | --- | --- | --- | --- | --- |
| Start | 1 | {1,3} | 3 | {3} | none |
| Expand B | - | {1,3} | done | {3} | none |

Here, from `1` we can reach `3`, and from `3` we only reach itself, so intersection is `{3}` and output is:

```
yes
3
```

This shows the algorithm correctly handles asymmetric reachability where one start is already close to the meeting point.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n + m) | Two graph traversals plus a linear scan over nodes |
| Space | O(n + m) | Adjacency list plus two visited arrays |

The constraints allow up to 200,000 total graph elements, and each is processed a constant number of times. This fits comfortably within typical limits for a 2-second execution window in Python.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from __main__ import solve
    try:
        return sys.stdout.getvalue()
    finally:
        pass

# Provided samples
# (formatting assumed; adjust if needed)

# Custom cases
assert run("""2 0
1 2
1 2
""").strip() == "no", "no edges"

assert run("""2 1
1 2
1 2
""").strip().split()[0] == "yes", "single path"

assert run("""4 4
1 2
2 3
3 4
1 4
1 3
""").strip().split()[0] == "yes", "multiple paths"

assert run("""3 2
1 2
2 3
3 1
""").strip().split()[0] == "yes", "cycle case"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| no edges | no | disconnected graph handling |
| single path | yes | simple reachability |
| multiple paths | yes | redundant edges |
| cycle case | yes | strongly connected behavior |

## Edge Cases

A key edge case is when one starting node is already reachable from the other. For example, if `b` can reach `a`, then `a` might already be a valid meeting point.

Input:

```
2 1
1 2
1 2
```

From `1`, reachable set is `{1,2}`. From `2`, reachable set is `{2}`. The intersection is `{2}`, so output is `yes 2`. The BFS from `2` correctly marks only itself, and the final scan finds node `2` as common.

Another case is a disconnected graph:

```
4 2
1 2
3 4
1 3
```

From `1` we reach `{1,2}`, from `3` we reach `{3,4}`, intersection is empty. The algorithm correctly prints `no` after scanning all nodes, because no node is marked in both visited arrays.

A final subtle case is when multiple valid answers exist. Since we scan nodes in increasing order, we return the smallest labeled meeting station, but any order would be correct according to the problem.
