---
title: "CF 1593E - Gardener and Tree"
description: "We are given an unrooted tree and a repeated pruning process. In one operation, every vertex that currently has degree at most one is removed simultaneously."
date: "2026-06-10T09:08:16+07:00"
tags: ["codeforces", "competitive-programming", "brute-force", "data-structures", "dfs-and-similar", "greedy", "implementation", "trees"]
categories: ["algorithms"]
codeforces_contest: 1593
codeforces_index: "E"
codeforces_contest_name: "Codeforces Round 748 (Div. 3)"
rating: 1600
weight: 1593
solve_time_s: 95
verified: true
draft: false
---

[CF 1593E - Gardener and Tree](https://codeforces.com/problemset/problem/1593/E)

**Rating:** 1600  
**Tags:** brute force, data structures, dfs and similar, greedy, implementation, trees  
**Solve time:** 1m 35s  
**Verified:** yes  

## Solution
## Problem Understanding

We are given an unrooted tree and a repeated pruning process. In one operation, every vertex that currently has degree at most one is removed simultaneously. That means all leaves disappear, and in degenerate cases a single remaining vertex or a single edge also disappears because their endpoints are also considered leaves under the definition.

We repeat this operation exactly k times and want to know how many vertices remain after all rounds of simultaneous leaf removal.

The key observation from the constraints is that the total number of vertices across all test cases is up to 4 · 10^5. This immediately suggests that any solution doing repeated full graph traversals per operation is too slow, because k itself can be as large as 2 · 10^5 per test. A naive simulation would recompute leaves and remove them layer by layer, potentially touching all edges per step, which leads to O(nk) behavior in the worst case.

A subtle point is that the process is not about structural rearrangement of edges beyond deletion. Once a vertex is removed, it never comes back, and removals happen in layers from the outside toward the center.

Edge cases that break naive thinking are small trees:

A single node with k ≥ 1 should immediately become empty after the first operation, not stay at 1.

A two-node tree also becomes empty after the first operation, because both endpoints are leaves simultaneously.

A star-shaped tree collapses quickly: after one operation, only the center remains; after the second, it disappears.

These cases show that the process is fundamentally about distances to the “core” of the tree, not about dynamic degree updates alone.

## Approaches

A direct simulation maintains degrees, repeatedly collects all current leaves, removes them, and updates neighbors. This is correct because each operation matches the definition exactly. However, recomputing the leaf set up to k times can degenerate into repeatedly scanning large parts of the graph. In a long path, each round removes only two vertices, so the process takes O(n) rounds, and each round may cost O(n), giving O(n^2) overall.

The key structural insight is that a vertex survives exactly until all vertices within distance k from it are removed. In other words, each vertex has a “time of death” equal to how far it is from the nearest leaf, measured in layers of simultaneous removal.

If we reverse the process, instead of peeling leaves outward, we think of leaves as starting points and propagate inward. All leaves die at time 1, their neighbors at time 2, and so on. This is a multi-source BFS where all initial leaves start simultaneously with distance 1.

Thus, the problem becomes computing for every node its distance to the nearest leaf. After that, any node with distance strictly greater than k remains.

This transforms the problem from repeated structural updates into a single BFS over the tree.

| Approach | Time Complexity | Space Complexity | Verdict |
| --- | --- | --- | --- |
| Repeated leaf removal simulation | O(nk) worst-case | O(n) | Too slow |
| Multi-source BFS from leaves | O(n) | O(n) | Accepted |

## Algorithm Walkthrough

1. Compute the degree of every vertex. This is needed to identify initial leaves, since leaves are exactly nodes with degree ≤ 1.
2. Initialize a queue with all leaves and assign them distance 1. These represent vertices that are removed in the first operation.
3. Run a BFS from this queue. When processing a node u, propagate to neighbors v that have not yet been assigned a distance. Assign dist[v] = dist[u] + 1. This models that v becomes a leaf after all vertices in outer layers have been removed.
4. After BFS completes, every vertex has a value dist[v], which represents the round in which it gets removed.
5. Count how many vertices satisfy dist[v] > k. These are the vertices that survive k full pruning operations.

The reason this works is that each layer of BFS corresponds exactly to one round of leaf removal. Initially, only true leaves are removable. Once they are removed, some inner vertices become new leaves, which is precisely the next BFS frontier. Since all removals happen simultaneously per round, BFS correctly models parallel expansion of removal depth.

The invariant is that at the start of BFS level d, all vertices with dist ≤ d have already been identified as removable within d operations, and all remaining unvisited vertices are strictly deeper in the tree’s core. This ensures correctness because tree structure guarantees no alternative shorter removal path exists other than moving inward from a leaf.

## Python Solution

```python
import sys
input = sys.stdin.readline
from collections import deque

def solve():
    t = int(input())
    for _ in range(t):
        line = input().strip()
        while line == "":
            line = input().strip()
        n, k = map(int, line.split())

        adj = [[] for _ in range(n)]
        deg = [0] * n

        for _ in range(n - 1):
            u, v = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append(v)
            adj[v].append(u)
            deg[u] += 1
            deg[v] += 1

        dist = [-1] * n
        q = deque()

        for i in range(n):
            if deg[i] <= 1:
                dist[i] = 1
                q.append(i)

        remaining = n

        while q:
            u = q.popleft()
            if dist[u] > k:
                continue
            remaining -= 1
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)

        print(remaining)

if __name__ == "__main__":
    solve()
```

The adjacency list stores the tree structure, while degrees identify initial leaves. The BFS queue is seeded with all leaves at once, which ensures the first layer corresponds to the first pruning operation.

The distance array encodes the time of removal. A value of 1 means removed after the first operation, 2 after the second, and so on.

The remaining counter tracks how many vertices are still not removed after k operations. We only decrement it when we process nodes within the BFS up to time k.

One subtle point is handling empty lines between test cases; the input format includes them, so we explicitly skip blank lines before reading n and k.

## Worked Examples

We trace a small path tree: 1-2-3-4.

Initially, leaves are 1 and 4.

| Step | Queue | dist assignments | removed |
| --- | --- | --- | --- |
| init | [1,4] | 1:1, 4:1 | 0 |
| pop 1 | [4,2] | 2:2 | 1 |
| pop 4 | [2,3] | 3:2 | 2 |
| pop 2 | [3] | - | 3 |
| pop 3 | [] | - | 4 |

Here dist shows that 1 and 4 die in round 1, 2 and 3 in round 2. If k = 1, only 2 vertices remain.

Now consider a star with center 1 and leaves 2,3,4,5.

| Step | Queue | dist assignments | removed |
| --- | --- | --- | --- |
| init | [2,3,4,5] | all leaves dist=1 | 0 |
| pop leaves | [1] | 1 gets dist=2 | 4 |
| pop 1 | [] | - | 5 |

This confirms center survives exactly one round longer than leaves.

These traces show BFS layers correspond exactly to pruning rounds.

## Complexity Analysis

| Measure | Complexity | Explanation |
| --- | --- | --- |
| Time | O(n) per test case | Each vertex is enqueued and processed once, and each edge is visited a constant number of times |
| Space | O(n) | adjacency list, distance array, and queue |

Across all test cases, total n is bounded by 4 · 10^5, so the solution fits comfortably within limits. The linear BFS avoids repeated full scans of the tree.

## Test Cases

```python
import sys, io

def run(inp: str) -> str:
    sys.stdin = io.StringIO(inp)
    from collections import deque

    def solve():
        t = int(input())
        out = []
        for _ in range(t):
            line = input().strip()
            while line == "":
                line = input().strip()
            n, k = map(int, line.split())

            adj = [[] for _ in range(n)]
            deg = [0] * n

            for _ in range(n - 1):
                u, v = map(int, input().split())
                u -= 1
                v -= 1
                adj[u].append(v)
                adj[v].append(u)
                deg[u] += 1
                deg[v] += 1

            dist = [-1] * n
            q = deque()

            for i in range(n):
                if deg[i] <= 1:
                    dist[i] = 1
                    q.append(i)

            remaining = n

            while q:
                u = q.popleft()
                if dist[u] > k:
                    continue
                remaining -= 1
                for v in adj[u]:
                    if dist[v] == -1:
                        dist[v] = dist[u] + 1
                        q.append(v)

            out.append(str(remaining))
        return "\n".join(out)

    return solve()

# sample 1
assert run("""6

14 1
1 2
2 3
2 4
4 5
4 6
2 7
7 8
8 9
8 10
3 11
3 12
1 13
13 14

2 200000
1 2

3 2
1 2
2 3

5 1
5 1
3 2
2 1
5 4

6 2
5 1
2 5
5 6
4 2
3 4

7 1
4 3
5 1
1 3
6 1
1 7
2 1
""") == """7
0
0
3
1
2"""

# minimum size
assert run("""1

1 10
""") == "0"

# two nodes large k
assert run("""1

2 5
1 2
""") == "0"

# line
assert run("""1

4 1
1 2
2 3
3 4
""") == "2"

# star
assert run("""1

5 2
1 2
1 3
1 4
1 5
""") == "0"
```

| Test input | Expected output | What it validates |
| --- | --- | --- |
| single node | 0 | immediate removal in first operation |
| two nodes | 0 | both endpoints removed together |
| line tree | 2 | layered peeling in path structure |
| star | 0 | center survives exactly one round |

## Edge Cases

A single vertex tree shows the degenerate behavior of the operation. The BFS initializes that vertex as a leaf with distance 1, and since k ≥ 1, it is counted as removed immediately, producing output 0.

A two-vertex tree is similar: both nodes are leaves initially, both receive distance 1, and no vertices remain after the first operation. The BFS processes both simultaneously, ensuring no asymmetry between endpoints.

A long chain demonstrates the layered nature of the process. Leaves at both ends start with distance 1, their neighbors become distance 2, and so on until the center. The algorithm assigns increasing distances correctly without needing to explicitly simulate each pruning round.
